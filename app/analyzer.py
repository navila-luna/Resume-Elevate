import os
import re
import PyPDF2
from PyPDF2 import PdfReader
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai
# Initialize open-source models once
try:
    KEYBERT_MODEL = KeyBERT()
    SENTENCE_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    print("[INFO] Open-source ML models loaded successfully.")
except Exception as e:
    print(f"[WARN]: Could not load open-source ML models. {e}")
    KEYBERT_MODEL = None
    SENTENCE_MODEL = None

# --- Gemini API Configuration ---
try:
    GEMINI_API_KEY = ""

    if not GEMINI_API_KEY or GEMINI_API_KEY == "":
        print("[WARN] GEMINI_API_KEY not found or not set. AI suggestions will be disabled.")
        GEMINI_MODEL = None
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_MODEL = genai.GenerativeModel('gemini-1.5-flash-latest')
        print("[INFO] Gemini API configured successfully.")
except Exception as e:
    print(f"[WARN]: Could not configure Gemini API. {e}")
    GEMINI_MODEL = None

# Extracts text content from a given PDF file.
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except FileNotFoundError:
        print(f"Error: The file at {pdf_path} was not found.")
        return ""
    return text.strip()

# Extracts relevant keywords from text, optionally guided by seed keywords.
def extract_keywords(text: str, seed_keywords: list[str] = None) -> list[str]:
    if not KEYBERT_MODEL: return []
    try:
        keywords = KEYBERT_MODEL.extract_keywords(
            text, keyphrase_ngram_range=(1, 3), stop_words='english',
            use_mmr=True, diversity=0.5, top_n=20, seed_keywords=seed_keywords
        )
        return [keyword for keyword, score in keywords]
    except Exception as e:
        print(f"An error occurred during keyword extraction: {e}")
        return []

# Calculates the semantic similarity between two texts.
def get_semantic_similarity(text1: str, text2: str) -> float:
    if not SENTENCE_MODEL: return 0.0
    try:
        embedding1 = SENTENCE_MODEL.encode(text1, convert_to_tensor=True)
        embedding2 = SENTENCE_MODEL.encode(text2, convert_to_tensor=True)
        cosine_score = util.cos_sim(embedding1, embedding2)
        return round(cosine_score.item(), 2)
    except Exception as e:
        print(f"An error occurred during semantic similarity calculation: {e}")
        return 0.0


"""
    Splits a job description into 'required' and 'preferred' sections
    based on common headings.
"""
def parse_job_description(jd_text: str) -> dict:
    required_text = jd_text
    preferred_text = ""

    # Define regex patterns for preferred/bonus sections at the start of a line
    preferred_patterns = r'^(preferred qualifications|nice to have|bonus points|desired skills)'
    
    # Find the start of a preferred section
    preferred_match = re.search(preferred_patterns, jd_text, re.IGNORECASE | re.MULTILINE)
    
    if preferred_match:
        # Everything before the match is considered part of the required/main block
        required_text = jd_text[:preferred_match.start()]
        # Everything after is the preferred block
        preferred_text = jd_text[preferred_match.start():]
        
    return {'required': required_text, 'preferred': preferred_text}

#  Codepath Student resume format

"""
    Checks the resume against CodePath's specific formatting guidelines for students.
    resume_text (str): The full text content of the resume.

    ret: list[str]: A list of feedback messages regarding the resume's format.
                   Returns a success message if all checks pass.
"""
def check_codepath_student_resume_format(resume_text: str) -> list[str]:
    feedback = []

    # -Contact Information Checks
    _check_contact_info(resume_text, feedback)

    # - Section Structure Checks
    _check_required_sections(resume_text, feedback)

    # --- Education Section Checks
    _check_education_details(resume_text, feedback)

    # --- CodePath Specific Mentions
    _check_codepath_mention(resume_text, feedback)

    # --- Experience/Projects Section Checks
    _check_bullet_point_quality(resume_text, feedback)

    return feedback if feedback else ["Your resume format aligns well with CodePath student guidelines! Great job!"]

#  Helper to check for essential contact information.
def _check_contact_info(resume_text: str, feedback: list[str]):
    contact_checks = {
        "Email Address": r'[\w\.-]+@[\w\.-]+',
        "Phone Number": r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        "LinkedIn URL": r'linkedin.com/in/[\w-]+',
        "GitHub URL": r'github.com/[\w-]+'
    }
    for item, pattern in contact_checks.items():
        if not re.search(pattern, resume_text, re.IGNORECASE):
            feedback.append(f"Contact Info: Consider adding your {item}.")

# Helper to check for the presence of standard resume sections.
def _check_required_sections(resume_text: str, feedback: list[str]):
    required_sections = ['education', 'experience', 'projects', 'skills']
    for section in required_sections:
        if not re.search(r'\b' + section + r'\b', resume_text, re.IGNORECASE):
            feedback.append(f"Structure: Missing a standard '{section.capitalize()}' section, which is required.")


# Helper to check for specific details within the education section.
def _check_education_details(resume_text: str, feedback: list[str]):
    # Check for when GPA is below 3.5
    gpa_pattern = r'\b(gpa)\b.*([12]\.\d|3\.[0-4])'
    if re.search(gpa_pattern, resume_text, re.IGNORECASE):
        feedback.append("Education: Your GPA is below 3.5. It's recommended to remove it.")
    
    # Check for full degree name
    degree_pattern = r'\b(bachelor|master|b\.s|m\.s)\b'
    if not re.search(degree_pattern, resume_text, re.IGNORECASE):
        feedback.append("Education: Ensure you list your full degree name (e.g., Bachelor of Science in Computer Science).")
        
    dates_pattern = r'\b(january|february|march|april|may|june|july|august|september|october|november|december|expected|grad)\b.*\d{4}'
    # Checks for planned graduation month and year
    if not re.search(dates_pattern, resume_text, re.IGNORECASE):
        feedback.append("Education: Include your planned graduation month and year (e.g., May 2025).")

# Helper to check if CodePath courses are mentioned.
def _check_codepath_mention(resume_text: str, feedback: list[str]):
    if not re.search(r'codepath', resume_text, re.IGNORECASE):
        feedback.append("Skills/Education: Mention your CodePath course(s).")

# check bullet points for action verbs and quantitative details.
def _check_bullet_point_quality(resume_text: str, feedback: list[str]):
    # TODO: attach data/technicalVerbAnalysis/actionWords.py csv action_verbs file once done refining
    action_verbs = [
        'developed', 'engineered', 'created', 'led', 'managed', 'implemented', 
        'designed', 'architected', 'built', 'optimized', 'improved', 'increased', 
        'reduced', 'launched', 'spearheaded', 'analyzed', 'collaborated', 'contributed',
        'debugged', 'deployed', 'executed', 'generated', 'maintained', 'mentored',
        'programmed', 'researched', 'solved', 'tested', 'transformed', 'upgraded'
    ]
    bullet_points = re.findall(r'[\n\r]\s*[\*•-]\s*(.*)', resume_text)

    if bullet_points:
        # Check for strong action verbs
        if any(p.strip().split(' ')[0].lower() not in action_verbs for p in bullet_points if p.strip()):
            feedback.append("Experience/Projects: Some bullet points may not start with a strong action verb.")
        
        # Check for quantitative details (numbers/percentages)
        total_words = len(re.findall(r'\b\w+\b', resume_text))
        # Updated regex to capture numbers and common quantifiers like "thousand", "million"
        quantifiable_terms = re.findall(r'\d+(\.\d+)?%?|\b(thousand|million|billion)\b', resume_text, re.IGNORECASE)
        number_density = len(quantifiable_terms) / total_words if total_words > 0 else 0
        
        # Threshold for low quantitative detail (can be adjusted)
        if number_density < 0.005:
             feedback.append("Experience/Projects: Add more quantitative details (numbers, percentages, etc.) to show impact.")
             
# --- Main Analysis Logic ---
# Generates resume improvement suggestions using the Gemini API.
def generate_improvement_suggestions(resume_text, jd_text, matched_keywords, missing_keywords, format_feedback, weighted_score, semantic_score):
    if not GEMINI_MODEL:
        return "AI suggestions are disabled. Please set your GEMINI_API_KEY."
    print("\n[INFO] Generating AI suggestions with Gemini API...")
    
    prompt = f"""
    You are an expert career coach specializing in helping CodePath computer science students optimize their resumes for tech job applications. 
    Your goal is to provide highly actionable, empathetic, and constructive feedback based on the provided resume and job description.
    
    Below is the data for your analysis:
    - **Resume Text:**
    {resume_text}
    - **Job Description Text:**
    {jd_text}
    - **Keywords Matched from JD to Resume:** {', '.join(matched_keywords)}
    - **Keywords Missing from JD in Resume:** {', '.join(missing_keywords)}
    - **CodePath Format Feedback:** {'; '.join(format_feedback)}
    - **Weighted Keyword Score (0-1.0):** {weighted_score:.2f}
    - **Semantic Similarity Score (0-1.0):** {semantic_score:.2f}

    Please provide comprehensive suggestions in the following structured format, covering all aspects of a strong tech resume for a CodePath student. 
    Focus on how a CodePath student can best present their skills and experience.

    **Overall Fit & Key Takeaways:**
    * Summarize the candidate's general fit for the role based on the scores and keywords.
    * Highlight 1-2 most crucial areas for immediate improvement.

    **1. Enhancing Keyword Relevance:**
    * For each 'Missing Keyword', explain why it's important for this job and suggest specific sections 
    (e.g., Experience, Projects, Skills) where the candidate could potentially integrate it, providing examples of how to phrase it if applicable.
    * Suggest synonyms or related terms the candidate could use for matched keywords to broaden their impact.

    **2. Strengthening Experience & Projects:**
    * Based on the job description, suggest which projects or experiences from the resume could be expanded upon or rephrased to better align with the job requirements.
    * Emphasize adding quantifiable achievements (e.g., "Increased X by Y%", "Reduced Z by A"). Provide 1-2 examples of how to quantify a generic bullet point from
    the resume (if possible).
    * Recommend incorporating more strong action verbs if the current ones are weak.

    **3. Optimizing Skills Section:**
    * Advise on prioritizing skills based on the job description (e.g., move highly relevant skills to the top).
    * Suggest adding any related technologies or tools often associated with the job's requirements that might be missing but implied by other skills.

    **4. CodePath Specific Recommendations:**
    * Provide personalized advice drawing from the `codepath_format_feedback`. For instance, if GPA is low, specifically advise removing it. If CodePath mention is missing, 
    suggest where and how to add it effectively (e.g., "Under Education" or "Under Skills").
    * Recommend specific CodePath courses or projects that align with the missing skills/experience if the student has taken them or could consider them.

    **5. General Resume Best Practices:**
    * Briefly touch upon general ATS-friendliness, formatting (if not covered by CodePath feedback), and proofreading.

    Ensure your suggestions are concise, actionable, and encouraging.
    """
    try:
        response = GEMINI_MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during Gemini API call: {e}")
        return "Could not generate AI suggestions due to an API error."


"""
    Calculates a weighted score based on keyword matches.
    'Required' keywords are weighted more heavily than 'preferred' keywords.
"""
def score_resume(resume_keywords: list[str], required_keywords: list[str], preferred_keywords: list[str]) -> dict:

    resume_set = set(resume_keywords)
    required_set = set(required_keywords)
    preferred_set = set(preferred_keywords)

    jd_set = required_set.union(preferred_set)
    matched_skills = list(resume_set.intersection(jd_set))
    missing_skills = list(jd_set.difference(resume_set))

    score = 0
    total_weight = 0

    # Calculate score for required keywords (weight of 2)
    for keyword in required_set:
        total_weight += 2
        if keyword in resume_set:
            score += 2

    # Calculate score for preferred keywords (weight of 1)
    for keyword in preferred_set:
        total_weight += 1
        if keyword in resume_set:
            score += 1

    final_score = score / total_weight if total_weight > 0 else 0
    return {
        "weighted_score": round(final_score, 2),
        "matched_keywords": matched_skills,
        "missing_keywords": missing_skills
    }

# Orchestrates the full resume analysis pipeline.
def run_full_analysis(resume_pdf_path: str, job_description_text: str) -> dict:
    resume_text = extract_text_from_pdf(resume_pdf_path)
    if not resume_text: return {"error": "Could not extract text from the resume PDF."}
    
    # Parses the job description into sections
    jd_sections = parse_job_description(job_description_text)
    required_keywords = extract_keywords(jd_sections['required'])
    preferred_keywords = extract_keywords(jd_sections['preferred'])
    
    all_jd_keywords = list(set(required_keywords + preferred_keywords))

    # Will use all JD keywords to guide resume keyword extraction
    resume_keywords = extract_keywords(resume_text, seed_keywords=all_jd_keywords)
    
    # Scores based on the new weighted logic
    scoring_result = score_resume(resume_keywords, required_keywords, preferred_keywords)
    
    semantic_score = get_semantic_similarity(resume_text, job_description_text)
    format_feedback = check_codepath_student_resume_format(resume_text)
    
    suggestions = generate_improvement_suggestions(
        resume_text, job_description_text,
        scoring_result["matched_keywords"], scoring_result["missing_keywords"], format_feedback
    )
    
    return {
        "weighted_score": scoring_result["weighted_score"],
        "semantic_score": semantic_score,
        "codepath_format_feedback": format_feedback,
        "matched_keywords": scoring_result["matched_keywords"],
        "missing_keywords": scoring_result["missing_keywords"],
        "suggestions": suggestions
    }

# --- NOTE: Below is example usage for self testing purposes ---
if __name__ == '__main__':
    if not os.path.exists('data'): os.makedirs('data')
    try:
        writer = PyPDF2.PdfWriter()
        writer.add_blank_page(width=300, height=500)
        with open("data/sample_resume.pdf", "wb") as f: writer.write(f)
    except Exception: pass

    mock_resume_text = """
    Jane Doe
    San Francisco, CA | (123) 456-7890 | jane.doe@email.com
    github.com/janedoe | linkedin.com/in/janedoe
    Education: University of California, Berkeley. B.S. Computer Science, Expected December 2025.
    Experience: - Developed backend API.
    Projects: - Portfolio Website: A personal site. Built with React and deployed to Netlify.
    Skills: Python, JavaScript, Java, Django, React
    """
    original_extractor = extract_text_from_pdf
    extract_text_from_pdf = lambda path: mock_resume_text

    # Updated sample JD to test the new parser
    sample_jd = """
    We are seeking a Python Software Engineer.

    Minimum Qualifications:
    - Solid background in web development using Django.
    - Experience with CI/CD is required.

    Preferred Qualifications:
    - Knowledge of Agile methodologies and test-driven development is a huge plus.
    - Experience with React on the frontend.
    """
    results = run_full_analysis("data/sample_resume.pdf", sample_jd)

    if "error" in results:
        print(f"\nError: {results['error']}")
    else:
        print("\n--- ***Resume Analysis Report** ---")
        print(f"Weighted Keyword Score: {results['weighted_score'] * 100:.0f}%")
        print(f" Semantic Similarity Score: {results['semantic_score'] * 100:.0f}%")
        print("\n--- **CodePath Format Checklist** ---")
        for feedback in results['codepath_format_feedback']: print(f"• {feedback}")
        print("\n--- **Content & Keyword Analysis** ---")
        print(f"Matched Keywords: {results['matched_keywords']}")
        print(f"Missing Keywords: {results['missing_keywords']}")
        print(f"\nSuggestions:\n{results['suggestions']}")
