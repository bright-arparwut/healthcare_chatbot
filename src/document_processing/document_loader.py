import fitz  # PyMuPDF
from typing import List, Dict
from langchain.schema import Document

def load_pdf(file_path: str) -> List[Document]:
    """
    Load a PDF file and extract text from each page.
    
    Args:
    file_path (str): Path to the PDF file.
    
    Returns:
    List[Document]: A list of Document objects, each containing the text of a page.
    """
    documents = []
    
    try:
        with fitz.open(file_path) as pdf:
            for page_num, page in enumerate(pdf):
                text = page.get_text()
                metadata = {
                    "source": file_path,
                    "page": page_num + 1,
                }
                documents.append(Document(page_content=text, metadata=metadata))
        
        return documents
    
    except Exception as e:
        print(f"Error loading PDF {file_path}: {str(e)}")
        return []

def load_documents(file_paths: List[str]) -> List[Document]:
    """
    Load multiple PDF files.
    
    Args:
    file_paths (List[str]): List of paths to PDF files.
    
    Returns:
    List[Document]: A list of Document objects from all PDFs.
    """
    all_documents = []
    for file_path in file_paths:
        all_documents.extend(load_pdf(file_path))
    return all_documents