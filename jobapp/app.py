import os
from dotenv import load_dotenv
import gradio as gr
from embeddings import get_embedding, get_embeddings
from utils import rank_resumes
from summarizer import generate_summary
from db import init_db, save_session, load_all_sessions, load_session, delete_session
from document_processor import process_uploaded_files

init_db()

def run_matching(session_name, job_desc, resume_files, top_k=5):
    if not resume_files:
        return gr.update(visible=True, value="Please upload resume files."), [], [], []
    
    # Process uploaded files
    resumes = process_uploaded_files(resume_files)
    if not resumes:
        return gr.update(visible=True, value="Could not extract text from uploaded files."), [], []
    
    # Filter out resumes that are too short or contain error messages
    filtered_resumes = []
    for i, resume in enumerate(resumes):
        # Skip if too short (less than 100 characters) or contains error messages
        if len(resume.strip()) < 100 or "No text found" in resume or "Error reading" in resume:
            print(f"Skipping resume {i+1} - too short or contains errors: {len(resume)} chars")
            continue
        filtered_resumes.append(resume)
    
    if not filtered_resumes:
        return gr.update(visible=True, value="No valid resumes found after filtering."), [], []
    
    resumes = filtered_resumes

    # Clean and normalize text
    job_desc_clean = job_desc.strip()
    resumes_clean = [resume.strip() for resume in resumes]
    
    # Debug: Print text lengths and previews
    print(f"Job description length: {len(job_desc_clean)}")
    print(f"Job description preview: {job_desc_clean[:200]}...")
    print()
    
    for i, resume in enumerate(resumes_clean):
        print(f"Resume {i+1} length: {len(resume)}")
        print(f"Resume {i+1} preview: {resume[:200]}...")
        print()
    
    job_emb = get_embedding(job_desc_clean)
    resumes_emb = get_embeddings(resumes_clean)
    top_candidates = rank_resumes(job_emb, resumes_emb, resumes_clean, top_k)
    
    # Debug: Print raw scores
    print("\nRaw similarity scores (ranked):")
    for i, candidate in enumerate(top_candidates):
        print(f"Rank {i+1}: Index {candidate['index']} -> Score {candidate['similarity']}")

    results = []
    for i, candidate in enumerate(top_candidates):
        # Get the original file index to match with filename
        original_index = candidate['index']
        filename = f"Resume {i+1}"  # Default name
        
        # Try to get actual filename if available
        if resume_files and original_index < len(resume_files):
            try:
                file_obj = resume_files[original_index]
                if hasattr(file_obj, 'name'):
                    filename = file_obj.name
                elif isinstance(file_obj, tuple) and len(file_obj) >= 1:
                    filename = file_obj[0]
                elif isinstance(file_obj, str):
                    filename = file_obj.split('/')[-1]  # Get just the filename
            except:
                pass
        
        summary = generate_summary(job_desc, candidate['resume'])
        
        # Format the summary with filename and better paragraph structure
        # Clean up the filename to remove path and extension
        clean_filename = filename.split('/')[-1].split('.')[0] if '/' in filename else filename.split('.')[0]
        formatted_summary = f"**📄 {clean_filename}**\n\n{summary}\n\n---"
        
        results.append({
            "resume": candidate['resume'],
            "similarity": round(candidate['similarity'], 4),
            "summary": formatted_summary
        })

    save_session(session_name, job_desc, resumes, results)

    # Format scores with file names
    similarity_display = []
    summary_display = []
    
    for i, r in enumerate(results):
        # Get filename for the score display
        original_index = r.get('index', i)  # Use 'index' if available, otherwise use loop index
        filename = f"Resume {original_index + 1}"  # Default name
        
        # Try to get actual filename if available
        if resume_files and original_index < len(resume_files):
            try:
                file_obj = resume_files[original_index]
                if hasattr(file_obj, 'name'):
                    filename = file_obj.name.split('/')[-1]  # Keep full filename with extension
                elif isinstance(file_obj, tuple) and len(file_obj) >= 1:
                    filename = file_obj[0].split('/')[-1]
                elif isinstance(file_obj, str):
                    filename = file_obj.split('/')[-1]
            except:
                pass
        
        # Format as "filename.pdf : 0.25"
        score_display = f"{filename} : {r['similarity']}"
        similarity_display.append([score_display])  # Wrap in list for Dataframe
        summary_display.append(r["summary"])

    return gr.update(visible=True, value=f"Found {top_k} best matches."), similarity_display, summary_display

def load_session_callback(session_name):
    if not session_name:
        return "", "", None, [], []

    data = load_session(session_name)
    if not data:
        return f"No session '{session_name}' found.", "", None, [], []

    results = data.get("results", [])

    # Format scores with file names (using default names for loaded sessions)
    similarity_display = []
    summary_display = []
    
    for i, r in enumerate(results):
        filename = f"Resume {i+1}"
        similarity_display.append([filename, r["similarity"]])
        summary_display.append(r["summary"])

    return f"Loaded session '{session_name}'", data["job_description"], None, similarity_display, summary_display

def delete_session_callback(session_name):
    if session_name:
        delete_session(session_name)
        return f"Deleted session '{session_name}'."
    return "No session name provided."

def go_to_main():
    return gr.update(visible=False), gr.update(visible=True)

def show_summary(summary):
    return summary

with gr.Blocks(theme=gr.themes.Base()) as demo:
    gr.Markdown("""<h1 style='text-align:center;'>CandyTracker 🎯</h1>
    <p style='text-align:center;font-size:20px;'>Give me the resumes and the job description — I'll pick the top candidates for you.</p>""")

    intro = gr.Column(visible=True)
    with intro:
        start_btn = gr.Button("🚀 Start Now", scale=2)

    main = gr.Column(visible=False)
    with main:
        with gr.Row():
            session_name = gr.Textbox(label="Session Name")
            top_k = gr.Slider(1, 10, value=5, step=1, label="Top K Candidates")
        job_desc = gr.Textbox(label="Job Description", lines=6)
        resume_files = gr.File(
            label="Upload Resume Files (PDF, DOCX, DOC)",
            file_count="multiple",
            file_types=[".pdf", ".docx", ".doc"],
            height=200
        )

        with gr.Row():
            run_btn = gr.Button("🎯 Match Candidates")

        status = gr.Textbox(label="Status", interactive=False)

        with gr.Row():
            with gr.Column():
                gr.Markdown("## Candidate Scores")
                similarity_output = gr.Dataframe(headers=["Score"])
            with gr.Column():
                gr.Markdown("## AI Summaries")
                summary_output = gr.Dataframe(headers=["Summary"], wrap=True)

    # Transitions
    start_btn.click(go_to_main, outputs=[intro, main])

    run_btn.click(run_matching, inputs=[session_name, job_desc, resume_files, top_k],
                  outputs=[status, similarity_output, summary_output])

if __name__ == "__main__":
    demo.launch()
