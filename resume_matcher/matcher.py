from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeJobMatcher:
    def __init__(self):
        print("Loading AI model")
        self.model=SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded successfully!")

    def extract_job_skills(self,job_description):
        skills_keywords = [
            'python', 'java', 'javascript', 'html', 'css', 'react', 'angular',
            'sql', 'mysql', 'postgresql', 'mongodb', 'machine learning',
            'data science', 'artificial intelligence', 'deep learning',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'git', 'github', 'docker', 'kubernetes', 'aws', 'azure',
            'project management', 'leadership', 'communication', 'teamwork'
        ]
        job_text_lower=job_description.lower()
        found_skills=[]
        for skill in skills_keywords:
            if skill.lower() in job_text_lower:
                found_skills.append(skill)
        return found_skills
    
    def calculate_semantic_similarity(self,resume_text,job_description):
        try:
            embedding=self.model.encode([resume_text,job_description])
            similarity=cosine_similarity([embedding[0]],[embedding[1]])[0][0]
            return similarity*100
        except Exception as e:
            print(f"Error in semantic similarity:{e}")
            return 0

    def calculate_keyword_similarity(self,resume_text,job_description):
        try:
            vectorizer=TfidfVectorizer(stop_words="english",max_features=1000)
            tfidf_matrix=vectorizer.fit_transform([resume_text,job_description])
            similarity=cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:2])[0][0]
            return similarity*100
        except Exception as e:
            print(f"Error in keyword similarity:{e}")
            return 0
        
    def match_skills(self,resume_skills,job_skills):
        resume_skills_lower=[skill.lower() for skill in resume_skills]
        job_skills_lower=[skill.lower() for skill in job_skills]
        matched_skills=[]
        missing_skills=[]
        for job_skill in job_skills_lower:
            if job_skill in resume_skills_lower:
                matched_skills.append(job_skill)
            else:
                missing_skills.append(job_skill)
        if len(job_skills)>0:
            skill_match_percentage=(len(matched_skills)/len(job_skills))*100
        else:
            skill_match_percentage=0
        return{
            "matched_skills":matched_skills,
            "missing_skills":missing_skills,
            "skill_match_percentage":skill_match_percentage
        }
    
    def calculate_overall_match(self,resume_data,job_description):
        resume_text=resume_data["raw_text"]
        resume_skills=resume_data["skills"]
        job_skills=self.extract_job_skills(job_description)
        semantic_score=self.calculate_semantic_similarity(resume_text,job_description)
        keyword_score=self.calculate_keyword_similarity(resume_text,job_description)
        skill_match=self.match_skills(resume_skills,job_skills)
        overall_score=(
            semantic_score*0.4+
            keyword_score*0.3+
            skill_match["skill_match_percentage"]*0.3
        )
        return{
            "overall_score":float(round(overall_score,2)),
            "semantic_score": f"{round(semantic_score, 2):.2f}",
            "keyword_score":float(round(keyword_score,2)),
            "skill_match":skill_match,
            "resume_skills":resume_skills,
            "job_skills":job_skills
        }