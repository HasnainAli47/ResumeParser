import os
import requests
from .models import ChatSession, ChatMessage

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def query_groq(session_id, resume_text, user_query):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Retrieve previous chat history
    chat_history = ChatMessage.objects.filter(session__session_id=session_id).order_by("timestamp")
    past_messages = [{"role": msg.role, "content": msg.content} for msg in chat_history]

    # Add system instructions + resume data
    system_message = {
        "role": "system",
        "content": f"""
            You are an advanced AI specializing in resume analysis and candidate profiling. Your role is to extract and present structured insights from the provided resume text with maximum accuracy.  

            ### **Resume Processing Guidelines**:
            1. **Extract all available details** from the resume text while maintaining strict accuracy.
            2. **Do not infer or assume information**—only use what is explicitly stated in the text.
            3. **If a detail is missing**, respond with "This information is not mentioned in resume by the candidate" instead of making assumptions.
            4. **Categorize the extracted details** into the following sections:
            - **Personal Information**: Name, Email, Phone, Location, LinkedIn, Portfolio.
            - **Education History**: Degree(s), Institution(s), Year(s) of Graduation.
            - **Work Experience**: Company name, Job title, Duration, Key responsibilities.
            - **Technical Skills**: Programming languages, frameworks, tools, and technologies.
            - **Projects**: Project names, descriptions, technologies used, outcomes.
            - **Certifications**: Name, Issuing authority, Year obtained.
            - **Awards & Achievements**: Any recognitions or notable accomplishments.
            - **Publications & Research**: Papers, articles, or research contributions.
            - **Soft Skills**: Mentioned skills like leadership, teamwork, or problem-solving.
            - **Languages**: Any spoken languages if specified.
            5. **For list-based data**, format the response using bullet points for clarity.  

            ### **Resume Text**:
            --------------------
            {resume_text}
            --------------------

            ### **User Query**:
            {user_query}

            ### **Response Guidelines**:
            - **Strictly answer based on the resume text**—do not generate or assume any information.
            - **Format responses clearly**, ensuring readability and structured presentation.
            - **Use bullet points** for multiple items and structured information.
            - **Do not provide responses outside the domain of resume analysis**.
            - If a question is unrelated to resumes or candidates, respond with:  
            _"I specialize in resume analysis. Please ask questions related to candidate profiles."_

            ### **Extracted Information / Answer**:
            """

    }

    # Include past messages + new user message
    messages = [system_message] + past_messages + [{"role": "user", "content": user_query}]

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 1024
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except requests.exceptions.RequestException as e:
        return f"Error querying LLM: {str(e)}"

def query_groq_resume_extraction(resume_text):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
    You are an AI specialized in extracting structured resume information.
    Given a raw resume text, extract the following sections:
    
    - Personal Information (Name, Email, Phone)
    - Education (Degree, Field, University, Start Year, End Year)
    - Work Experience (Company, Job Title, Start Date, End Date, Responsibilities)
    - Skills (List of relevant skills) ("Python", "Java", "Machine Learning")
    - Certifications (List of certifications)
    
    Format the output in a structured JSON format.
    """

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": resume_text}
        ],
        "temperature": 0.3,
        "max_tokens": 2048
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
    except requests.exceptions.RequestException as e:
        return f"Error querying Groq API: {str(e)}"