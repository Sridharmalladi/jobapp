import PyPDF2
import docx
import io
from typing import List, Tuple

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file_content (bytes): PDF file content as bytes
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        result = text.strip()
        return result if result else "No text found in PDF"
    except Exception as e:
        print(f"PDF extraction error: {str(e)}")
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from a Word document.
    
    Args:
        file_content (bytes): DOCX file content as bytes
        
    Returns:
        str: Extracted text from the Word document
    """
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
        result = text.strip()
        return result if result else "No text found in Word document"
    except Exception as e:
        print(f"DOCX extraction error: {str(e)}")
        return f"Error reading Word document: {str(e)}"

def process_uploaded_files(files) -> List[str]:
    """
    Process uploaded files and extract text from them.
    
    Args:
        files: Gradio File component output (list of file objects)
        
    Returns:
        List[str]: List of extracted text from each file
    """
    extracted_texts = []
    
    if not files:
        return extracted_texts
    
    print(f"Processing {len(files)} files...")
    
    for i, file_obj in enumerate(files):
        try:
            print(f"Processing file {i+1}...")
            
            # Try different ways to get filename and content
            filename = None
            file_content = None
            
            # Method 1: Direct attributes
            if hasattr(file_obj, 'name'):
                filename = file_obj.name
            
            # For Gradio NamedString objects, we need to read the actual file
            if hasattr(file_obj, 'read'):
                file_content = file_obj.read()
            elif hasattr(file_obj, 'name') and isinstance(file_obj.name, str):
                # This is a Gradio NamedString - try to read the file from the path
                try:
                    with open(file_obj.name, 'rb') as f:
                        file_content = f.read()
                    print(f"Successfully read file from path: {filename}")
                except Exception as e:
                    print(f"Failed to read file from path: {e}")
                    file_content = None
            
            # Method 2: Tuple format
            if filename is None and isinstance(file_obj, tuple) and len(file_obj) >= 2:
                filename = file_obj[0]
                file_content = file_obj[1]
            
            # Method 3: Dictionary format
            if filename is None and isinstance(file_obj, dict):
                filename = file_obj.get('name', 'unknown')
                file_content = file_obj.get('content', file_obj)
            
            # Method 4: String path (try to read file)
            if filename is None and isinstance(file_obj, str):
                filename = file_obj
                try:
                    with open(file_obj, 'rb') as f:
                        file_content = f.read()
                except Exception as e:
                    print(f"Failed to read file from path: {e}")
            
            if filename is None:
                filename = f"file_{i+1}"
            
            if file_content is None:
                file_content = file_obj
            
            # Extract text based on file extension
            if filename.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file_content)
            elif filename.lower().endswith(('.docx', '.doc')):
                text = extract_text_from_docx(file_content)
            else:
                text = f"Unsupported file format: {filename}"
            
            print(f"Successfully extracted {len(text) if text else 0} characters from {filename}")
            
            # Accept any text that was extracted, but filter out error messages
            if text and len(text.strip()) > 0 and not text.startswith("Error") and not text.startswith("Could not extract"):
                extracted_texts.append(text)
            else:
                # Skip this file instead of showing error
                print(f"⚠️  Skipping {filename} - extraction failed")
                continue
                
        except Exception as e:
            print(f"❌ Error processing file {i+1}: {str(e)}")
            # Skip this file instead of showing error
            continue
    
    print(f"✅ Successfully processed {len(extracted_texts)} files")
    return extracted_texts 