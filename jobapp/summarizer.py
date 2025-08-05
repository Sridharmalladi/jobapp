import os
from openai import OpenAI

def generate_summary(job_description: str, candidate_resume: str) -> str:
    """
    Generate a summary explaining why the candidate fits the job.

    Args:
        job_description (str): The job description text
        candidate_resume (str): The candidate's resume text

    Returns:
        str: A short AI-generated summary
    """
    # Check if API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Summary not available - OpenAI API key not configured."
    
    # Prepare the prompt to guide the model
    prompt = (
        f"Job Description:\n{job_description}\n\n"
        f"Candidate Resume:\n{candidate_resume}\n\n"
        "In 2-3 sentences, explain why this candidate is a good fit for the job."
    )

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        # Extract the assistant's reply text
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        # Handle API errors gracefully
        print(f"OpenAI API error: {e}")
        return "Summary not available due to an error."
