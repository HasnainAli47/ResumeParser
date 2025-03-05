from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from document_processing.models import (
    Resume, PersonalInfo, Education, Skill, WorkExperience, Certification, ChatSession, ChatMessage
)
from django.utils.timezone import now
import json


class ResumeModelTests(TestCase):
    """Test suite for Resume and related models."""

    def setUp(self):
        """Set up a test resume and associated data."""
        self.resume = Resume.objects.create(extracted_text="Sample Resume Text")
        self.personal_info = PersonalInfo.objects.create(
            resume=self.resume, name="John Doe", email="john@example.com", phone="1234567890"
        )
        self.education = Education.objects.create(
            resume=self.resume, degree="BSc Computer Science", university="MIT", start_year="2018", end_year="2022"
        )
        self.skill = Skill.objects.create(resume=self.resume, name="Python", level="Expert")
        self.experience = WorkExperience.objects.create(
            resume=self.resume, company="Google", job_title="Software Engineer",
            start_date="2022", end_date="Present", responsibilities="Developed AI systems."
        )
        self.certification = Certification.objects.create(
            resume=self.resume, name="AWS Certified Solutions Architect", issued_by="Amazon", year="2021"
        )

    def test_resume_creation(self):
        """Test if a resume object is created properly."""
        self.assertEqual(Resume.objects.count(), 1)

    def test_personal_info(self):
        """Test if personal info is linked correctly."""
        self.assertEqual(self.personal_info.resume, self.resume)
        self.assertEqual(self.personal_info.name, "John Doe")

    def test_education_entry(self):
        """Test if education details are stored correctly."""
        self.assertEqual(self.education.degree, "BSc Computer Science")
        self.assertEqual(self.education.university, "MIT")

    def test_skill_entry(self):
        """Test if skills are saved correctly."""
        self.assertEqual(self.skill.name, "Python")
        self.assertEqual(self.skill.level, "Expert")

    def test_experience_entry(self):
        """Test if work experience is stored correctly."""
        self.assertEqual(self.experience.company, "Google")
        self.assertEqual(self.experience.job_title, "Software Engineer")

    def test_certification_entry(self):
        """Test if certifications are saved correctly."""
        self.assertEqual(self.certification.name, "AWS Certified Solutions Architect")


class ChatSessionModelTests(TestCase):
    """Test suite for ChatSession and ChatMessage models."""

    def setUp(self):
        """Set up a chat session and messages."""
        self.session = ChatSession.objects.create(session_id="12345")
        self.message = ChatMessage.objects.create(
            session=self.session, role="user", content="Hello AI!", timestamp=now()
        )

    def test_chat_session_creation(self):
        """Test if chat sessions are created properly."""
        self.assertEqual(ChatSession.objects.count(), 1)

    def test_chat_message_creation(self):
        """Test if chat messages are saved correctly."""
        self.assertEqual(ChatMessage.objects.count(), 1)
        self.assertEqual(self.message.content, "Hello AI!")


class CandidateAPITests(TestCase):
    """Test suite for candidate API endpoints."""

    def setUp(self):
        self.client = Client()
        self.resume = Resume.objects.create(extracted_text="Python Developer at Google")
        self.personal_info = PersonalInfo.objects.create(resume=self.resume, name="Alice")

    def test_get_candidates(self):
        """Test retrieving candidates list."""
        response = self.client.get(reverse("resume-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Alice")

    def test_candidate_creation(self):
        response = self.client.post(
            reverse("resume-list"),
            {"name": "Jane Doe", "resume": self.resume.id}, 
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class QueryAPITests(TestCase):
    """Test suite for AI query endpoint."""

    def setUp(self):
        self.client = Client()
        self.resume = Resume.objects.create(extracted_text="Software Engineer at Facebook")
        self.personal_info = PersonalInfo.objects.create(resume=self.resume, name="Bob")

    def test_query_without_resume(self):
        """Test error handling when no resume ID is provided."""
        response = self.client.post(reverse("resume-query"), {"query": "What is the experience?"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
