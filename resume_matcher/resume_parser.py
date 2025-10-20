import PyPDF2
import docx
import re

def extract_text_from_pdf(pdf_path):
    text=""
    try:
        with open (pdf_path,"rb") as file:
            pdf_reader=PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text+=page.extract_text()
    except Exception as e:
        print(f"Error in reading pdf:{e}")
    return text

def extract_text_from_docx(docx_path):
    text=""
    try:
        doc=docx.Document(docx_path)
        for paragraph in doc.paragraphs:
            text+=paragraph.text+"\n"
    except Exception as e:
        print(f"Error in reading docx:{e}")
    return text

def extract_skills_simple(text):
    skills_list=[
        'python', 'java', 'javascript', 'html', 'css', 'react', 'angular',
        'sql', 'mysql', 'postgresql', 'mongodb', 'machine learning',
        'data science', 'artificial intelligence', 'deep learning',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'git', 'github', 'docker', 'kubernetes', 'aws', 'azure',
        'project management', 'leadership', 'communication', 'teamwork'
    ]
    text_lower=text.lower()
    found_skills=[]
    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return found_skills

def extract_email(text):
    email_pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails=re.findall(email_pattern,text)
    return emails[0] if emails else None

def extract_phone(text):
    phone_pattern=r'[\+]?[0-9]?[0-9]{7,15}'
    phones=re.findall(phone_pattern,text)
    return phones[0] if phones else None

def parse_resume(file_path):
    if file_path.endswith('.pdf'):
        text=extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text=extract_text_from_docx(file_path)
    else:
        return {"error":"unsupported file format"}
    
    skills=extract_skills_simple(text)
    email=extract_email(text)
    phone=extract_phone(text)

    return{
        "raw_text":text,
        "skills":skills,
        "email":email,
        "phone":phone,
        "text_length":len(text)
    }