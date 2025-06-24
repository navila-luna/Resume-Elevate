import pandas as pd
import spacy
import re
from spacy.matcher import Matcher

#  Dataset Source For Training: https://www.kaggle.com/datasets/kshitizregmi/jobs-and-job-description
class JobDescriptionParser:
    def __init__(self, spacy_model='en_core_web_sm'):
        self.nlp = spacy.load(spacy_model)
        # TO DO: Extend with custom NER or rule-based matching for better accuracy
        #        enhance the lists for skills and qualifications.
       
        self.skill_keywords = self._load_keywords('skills.txt') 
        self.qualification_keywords = self._load_keywords('qualifications.txt')

        self.matcher = Matcher(self.nlp.vocab)
        # Note to self-- Example pattern for "X+ years of experience"
        pattern_experience = [{"LOWER": {"REGEX": r"\d+"}}, {"LOWER": {"IN": ["year", "years"]}}, {"LOWER": {"IN": ["of", ""]}}, {"LOWER": {"IN": ["experience", "exp"]}}]
        self.matcher.add("EXPERIENCE", [pattern_experience])
        

    # Helper to load keywords from a text file, one per line."""
    def _load_keywords(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return [line.strip().lower() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Using an empty list for this category.")
            return []


    
    # Parses a single job description to extract skills, experience levels, and qualifications.
    def parse_job_description(self, job_description_text):
        doc = self.nlp(job_description_text.lower())

        extracted_skills = self._extract_skills(doc)
        experience_level = self._extract_experience(doc)
        extracted_qualifications = self._extract_qualifications(doc)

        return {
            "skills": {"required": list(extracted_skills['required']), "preferred": list(extracted_skills['preferred'])},
            "experience_level": experience_level,
            "qualifications": list(extracted_qualifications)
        }


    """
        Extracts skills from the document. This is a simplified approach.
        A more robust solution would involve:
        - Custom NER training for skills
        - More sophisticated keyword matching with context
        - Distinguishing required vs. preferred based on surrounding text (e.g., "must have", "ideally")
    """
    def _extract_skills(self, doc):
        required_skills = set()
        preferred_skills = set()

        # Simple keyword matching
        for skill in self.skill_keywords:
            if skill in doc.text:
                # Basic attempt to distinguish required vs. preferred
                # TODO: This needs significant improvement for accuracy
                if "required" in doc.text or "must have" in doc.text or "mandatory" in doc.text:
                    if skill in doc.text.split("required")[0] or skill in doc.text.split("must have")[0]: # Simplified
                        required_skills.add(skill)
                    else:
                        preferred_skills.add(skill)
                elif "preferred" in doc.text or "nice to have" in doc.text or "plus" in doc.text:
                     if skill in doc.text.split("preferred")[0] or skill in doc.text.split("nice to have")[0]: # Simplified
                        preferred_skills.add(skill)
                     else: # If not explicitly preferred, assume required for simplicity, or refine
                         required_skills.add(skill)
                else: # Default to required if no clear indicator
                    required_skills.add(skill)

        return {"required": required_skills, "preferred": preferred_skills}

    """
      Extracts experience level (e.g., "3-5 years", "junior", "senior").
      Uses regex and spaCy's Matcher.
    """
    def _extract_experience(self, doc):
        experience_text = []
        # check first numerical years of experience
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            experience_text.append(span.text)

        # now check common experience level keywords
        level_keywords = {
            "junior": ["junior", "entry-level", "0-2 years", "less than 2 years"],
            "mid-level": ["mid-level", "intermediate", "2-5 years"],
            "senior": ["senior", "lead", "staff", "principal", "5+ years", "over 5 years", "10+ years"],
            "manager": ["manager", "managing"]
        }

        found_levels = []
        for level, keywords in level_keywords.items():
            for keyword in keywords:
                if keyword in doc.text:
                    found_levels.append(level)
                    break

        if experience_text:
            return ", ".join(experience_text + list(set(found_levels)))
        elif found_levels:
            return ", ".join(list(set(found_levels)))
        else:
            return "Not specified"

    """
        Extracts qualifications (e.g., degrees, certifications).
        Similar to skills, this will benefit from more comprehensive lists and context.
    """
    def _extract_qualifications(self, doc):
        found_qualifications = set()
        for qual in self.qualification_keywords:
            if qual in doc.text:
                found_qualifications.add(qual)
        return found_qualifications

    """
        Reads a CSV, parses each job description, and saves the results to a new CSV.
    """
    def process_csv(self, csv_filepath, output_filepath='parsed_job_descriptions.csv'):
        try:
            df = pd.read_csv(csv_filepath)
        except FileNotFoundError:
            print(f"Error: CSV file not found at {csv_filepath}")
            return

        if 'job_description' not in df.columns:
            print("Error: 'job_description' column not found in the CSV.")
            return

        parsed_data = []
        for index, row in df.iterrows():
            job_description = str(row['job_description'])
            job_role = str(row['job_role'])
            parsed_info = self.parse_job_description(job_description)
            parsed_data.append({
                "job_role": job_role,
                "original_description": job_description,
                "parsed_skills_required": ", ".join(parsed_info["skills"]["required"]),
                "parsed_skills_preferred": ", ".join(parsed_info["skills"]["preferred"]),
                "parsed_experience_level": parsed_info["experience_level"],
                "parsed_qualifications": ", ".join(parsed_info["qualifications"])
            })

        parsed_df = pd.DataFrame(parsed_data)
        parsed_df.to_csv(output_filepath, index=False)
        print(f"Parsed job descriptions saved to {output_filepath}")
        
    if __name__ == "__main__":
        # for self testing purposes
        dummy_data = {
            'job_role': ['Software Engineer', 'Data Scientist', 'DevOps Engineer', 'Project Manager'],
            'job_description': [
                "We are looking for a Software Engineer with a strong background in Python and Java. Must have 3+ years of experience with REST APIs and microservices. Bachelor's degree in Computer Science is required. AWS experience is a plus. Agile development knowledge preferred.",
                "Exciting opportunity for a Data Scientist. Requires 5 years of experience in machine learning and NLP. Familiarity with TensorFlow or PyTorch is mandatory. PhD preferred. Strong SQL skills are a must. Experience with Azure is nice to have.",
                "Seeking a Senior DevOps Engineer with extensive Docker and Kubernetes experience (7+ years). Proficient in cloud computing (AWS/Azure). Communication skills essential. CISSP certification preferred.",
                "Project Manager with 10+ years of experience. PMP certification required. Experience with Scrum methodology. Excellent problem-solving and teamwork skills."
            ]
        }
        dummy_df = pd.DataFrame(dummy_data)
        dummy_df.to_csv('job_postings.csv', index=False)
        print("Created dummy 'job_postings.csv'")

        parser = JobDescriptionParser()
        parser.process_csv('job_postings.csv', 'parsed_job_descriptions.csv')

        # parsed_df = pd.read_csv('parsed_job_descriptions.csv')
        # print(parsed_df.head())