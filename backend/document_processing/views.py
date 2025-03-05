from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import os
from .serializers import ResumeSerializer
from .groq_api import query_groq
from .utils import parse_resume, extract_text_from_pdf, extract_text_from_docx
from .models import PersonalInfo, Education, Skill, WorkExperience, Certification, Resume, ChatMessage, ChatSession
import uuid
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from cacheops import cached_as
from django.db.models import Q, Count
from django.http import JsonResponse

class ResumeListView(APIView):
    def get(self, request):
        resumes = Resume.objects.all()
        candidates = []

        for resume in resumes:
            personal_info = getattr(resume, "personal_info", None)
            name = personal_info.name if personal_info and personal_info.name else "Unknown Candidate"
            candidates.append({"id": resume.id, "name": name})

        return JsonResponse(candidates, safe=False)

class ResumeQueryView(APIView):
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request, *args, **kwargs):
        session_id = request.data.get("session_id")
        resume_id = request.data.get("resume_id")
        query_text = request.data.get("query")  # Single query
        queries = request.data.get("queries")  # List of queries

        if not resume_id:
            return Response({"error": "resume_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not query_text and not queries:
            return Response({"error": "Either 'query' (single query) or 'queries' (list of queries) is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            ChatSession.objects.create(session_id=session_id)

        try:
            resume = Resume.objects.get(id=resume_id)
            resume_text = resume.extracted_text

            responses = {}

            # Handle Single Query
            if query_text:
                llm_response = query_groq(session_id, resume_text, query_text)
                responses[query_text] = llm_response

                # Save chat history
                chat_session, _ = ChatSession.objects.get_or_create(session_id=session_id)
                ChatMessage.objects.create(session=chat_session, role="user", content=query_text)
                ChatMessage.objects.create(session=chat_session, role="assistant", content=llm_response)

            # Handle Batch Queries
            if queries and isinstance(queries, list):
                for q in queries:
                    llm_response = query_groq(session_id, resume_text, q)
                    responses[q] = llm_response

                    # Save chat history
                    chat_session, _ = ChatSession.objects.get_or_create(session_id=session_id)
                    ChatMessage.objects.create(session=chat_session, role="user", content=q)
                    ChatMessage.objects.create(session=chat_session, role="assistant", content=llm_response)

            return Response({
                "message": "Query processed successfully.",
                "session_id": session_id,
                "responses": responses
            }, status=status.HTTP_200_OK)

        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class ResumeUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file_serializer = ResumeSerializer(data=request.data)
        if file_serializer.is_valid():
            resume = file_serializer.save()
            file_path = os.path.join(settings.MEDIA_ROOT, resume.file.name)

            # Extract text from file
            if file_path.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(file_path)
            elif file_path.endswith(".docx"):
                extracted_text = extract_text_from_docx(file_path)
            else:
                return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

            resume.extracted_text = extracted_text
            resume.save()

            # Parse structured data
            parsed_data = parse_resume(extracted_text)

            # Save Personal Info
            personal_info = parsed_data["personal_info"]
            PersonalInfo.objects.create(
                resume=resume,
                name=personal_info["name"],
                email=personal_info["email"],
                phone=personal_info["phone"]
            )

            # Save Education
            for edu in parsed_data["education"]:
                Education.objects.create(resume=resume, **edu)

            # Save Skills
            for skill_name in parsed_data["skills"]:
                Skill.objects.create(resume=resume, name=skill_name)

            # Save Work Experience
            for exp in parsed_data["work_experience"]:
                WorkExperience.objects.create(resume=resume, **exp)

            # Save Certifications
            for cert_name in parsed_data["certifications"]:
                Certification.objects.create(resume=resume, name=cert_name)

            return Response({
                "message": "Resume uploaded & structured data saved successfully.",
                "resume_id": resume.id,
                "parsed_data": parsed_data
            }, status=status.HTTP_201_CREATED)

        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeSearchView(APIView):
    """Search for candidates based on skills, experience, education, and certifications."""

    def post(self, request, *args, **kwargs):
        skills = request.data.get("skills", [])  # List of required skills
        min_experience = request.data.get("min_experience", 0)  # Minimum years of experience
        education_level = request.data.get("education_level", None)  # Degree level (e.g., "Master")
        certifications = request.data.get("certifications", [])  # Required certifications

        # Ensure min_experience is a valid integer
        try:
            min_experience = int(min_experience) if str(min_experience).strip() else 0
        except ValueError:
            min_experience = 0  # Default to 0 if conversion fails

        # Debugging: Check stored skills
        stored_skills = Skill.objects.values_list("name", flat=True)

        # Build search query
        query = Q()

        if skills:
            skill_query = Q()
            for skill in skills:
                skill_query |= Q(skills__name__iexact=skill)  # Exact match to ensure filtering works
            query &= skill_query


        if min_experience > 0:
            query &= Q(work_experience__start_date__lte=f"{2025 - min_experience}") 

        if education_level:
            query &= Q(education__degree__icontains=education_level)

        if certifications:
            query &= Q(certifications__name__in=certifications)
        
        # Filter and rank candidates
        candidates = Resume.objects.filter(query).distinct().annotate(
            skill_count=Count("skills"),
            experience_count=Count("work_experience"),
            education_count=Count("education"),
            certification_count=Count("certifications"),
        ).order_by("-skill_count", "-experience_count")

        results = []
        for candidate in candidates:
            # Show all of the fields this candidate have
            personal_info = getattr(candidate, "personal_info", None)

            results.append({
                "resume_id": candidate.id,
                "name": personal_info.name,
                "skills": list(candidate.skills.values_list("name", flat=True)),
                "experience": list(candidate.work_experience.values_list("job_title", flat=True)),
                "education": list(candidate.education.values_list("degree", flat=True)),
                "certifications": list(candidate.certifications.values_list("name", flat=True)),
            })

        return Response({
            "message": "Resume search completed successfully.",
            "results": results
        }, status=status.HTTP_200_OK)
