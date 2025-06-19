# Resume-Elevate

Project: The Actionable Resume Optimizer
Resume Elevate is a website where a user can upload their resume, paste a job description, and receive a "match score" along with a list of crucial keywords missing from their resume. Suggestions will be applied to see whether they follow Codepath guidelines. More advance features which is in progress, is fine-tuning the SentenceTransformer model on a corpus of tech job descriptions and resumes. This would improve the relevance of similarity scores within the tech industry.

The following are the functionalities:
1. User can upload a resume in PDF format.
2. User can paste job description text into a text box.
3. User clicks an "Analyze" button.
4. The app displays a numerical match score and a list of suggested keywords.


python3 -m venv .venv
source .venv/bin/activate

pip install keybert
pip install sentence-transformers
pip install google-generativeai


