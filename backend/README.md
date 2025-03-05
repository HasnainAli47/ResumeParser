# CV Analysis System - Backend

## 🚀 Project Overview
The **CV Analysis System** is a powerful AI-driven resume processing backend built with **Django, NLP, and Groq's LLaMA-3.3-70B model**. This system processes multiple resume documents, extracts structured information using **OCR and NLP**, and allows advanced **LLM-powered querying** via a chatbot interface. It also includes an **advanced resume search engine** for filtering candidates based on skills, experience, education, and certifications.

### ✨ **Key Features**
✅ **Resume Upload & Parsing**: Supports **PDF & DOCX** formats, extracts text via **OCR** and organizes details into structured data.
✅ **Advanced Regex + NLP Extraction**: Extracts **Personal Information, Education, Work Experience, Skills, Projects, and Certifications**.
✅ **Groq API Integration**: Uses **LLaMA-3.3-70B** for **intelligent resume querying**.
✅ **Multi-Turn Conversational AI**: Tracks chat history for **context-aware resume queries**.
✅ **Optimized API Performance**: Implements **rate limiting, caching, and batch query processing**.
✅ **Advanced Resume Search**: Find candidates by **skills, experience, education, and certifications**.

---

## 📂 **Project Structure**
```
backend/
│── document_processing/   # Core resume parsing & query processing
│   ├── models.py         # Database models (Resume, PersonalInfo, Education, etc.)
│   ├── views.py          # API views (upload, query, search, etc.)
│   ├── groq_api.py       # LLM Query Handler
│   ├── utils.py          # NLP & regex parsing functions
│── backend/
│   ├── settings.py       # Django settings (DB, API Keys, Cache, etc.)
│── requirements.txt      # Dependencies
│── README.md             # Documentation
```

---

## 🛠 **Setup & Installation**

### **2️⃣ Set Up a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate    # For Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**
Create a `.env` file and add the following:
```env
GROQ_API_KEY=your_groq_api_key
```

### **5️⃣ Apply Database Migrations**
```bash
python manage.py makemigrations document_processing
python manage.py migrate
```

### **6️⃣ Run the Server**
```bash
python manage.py runserver
```

---

## 🔥 **How to Use the API**
### **1️⃣ Upload a Resume**
**Endpoint:** `/api/document_processing/upload/`  
**Method:** `POST`  
**Payload:**
```json
{
    "file": "your_resume.pdf"
}
```
**Response:**
```json
{
    "message": "File uploaded successfully",
    "resume_id": 5
}
```

---

### **2️⃣ Query a Resume (LLM-Powered)**
**Endpoint:** `/api/document_processing/query/`  
**Method:** `POST`  
**Payload (Single Query):**
```json
{
    "resume_id": 5,
    "query": "What programming languages does the candidate know?"
}
```
**Payload (Batch Queries):**
```json
{
    "resume_id": 5,
    "queries": [
        "What programming languages does the candidate know?",
        "What is the candidate's most recent job experience?"
    ]
}
```

---

### **3️⃣ Search Candidates by Criteria**
**Endpoint:** `/api/document_processing/search/`  
**Method:** `POST`  
**Payload:**
```json
{
    "skills": ["Python", "Django"],
    "min_experience": 3,
    "education_level": "Master",
    "certifications": ["AWS Certified"]
}
```
