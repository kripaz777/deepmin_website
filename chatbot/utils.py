import os
import re
import numpy as np
from typing import List, Tuple
import google.generativeai as genai

# Document parsing imports
# Document parsing imports
import PyPDF2
from docx import Document as DocxDocument


def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Extract text from uploaded file based on type"""
    
    if file_type == 'txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    elif file_type == 'pdf':
        text = []
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)
    
    elif file_type == 'docx':
        doc = DocxDocument(file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks for better context preservation.
    
    Args:
        text: The text to chunk
        chunk_size: Approximate number of words per chunk
        overlap: Number of words to overlap between chunks
    
    Returns:
        List of text chunks
    """
    # Clean and normalize text
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into words
    words = text.split()
    
    if len(words) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(' '.join(chunk_words))
        
        # Move start position with overlap
        start = end - overlap
        
        # Prevent infinite loop
        if start >= len(words):
            break
    
    return chunks


def generate_embedding(text: str, api_key: str) -> List[float]:
    """
    Generate embedding for text using Gemini API.
    
    Args:
        text: Text to embed
        api_key: Gemini API key
    
    Returns:
        Embedding vector as list of floats
    """
    genai.configure(api_key=api_key)
    
    # Use Gemini's embedding model
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    
    return result['embedding']


def generate_query_embedding(query: str, api_key: str) -> List[float]:
    """
    Generate embedding for a query using Gemini API.
    
    Args:
        query: Query text
        api_key: Gemini API key
    
    Returns:
        Embedding vector as list of floats
    """
    genai.configure(api_key=api_key)
    
    result = genai.embed_content(
        model="models/embedding-001",
        content=query,
        task_type="retrieval_query"
    )
    
    return result['embedding']


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))


def find_relevant_chunks(query_embedding: List[float], chunks, top_k: int = 3) -> List[Tuple[any, float]]:
    """
    Find most relevant chunks using cosine similarity.
    
    Args:
        query_embedding: Query embedding vector
        chunks: QuerySet of DocumentChunk objects
        top_k: Number of top results to return
    
    Returns:
        List of (chunk, similarity_score) tuples
    """
    results = []
    
    for chunk in chunks:
        chunk_embedding = chunk.get_embedding()
        if chunk_embedding:
            similarity = cosine_similarity(query_embedding, chunk_embedding)
            results.append((chunk, similarity))
    
    # Sort by similarity (highest first)
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:top_k]


def generate_answer_with_gemini(query: str, context_chunks: List[str], api_key: str) -> str:
    """
    Generate answer using Gemini with retrieved context.
    
    Args:
        query: User's question
        context_chunks: List of relevant text chunks
        api_key: Gemini API key
    
    Returns:
        Generated answer
    """
    genai.configure(api_key=api_key)
    
    # Prepare context
    context = "\n\n".join([f"[Context {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks)])
    
    # Create prompt
    prompt = f"""Based on the following context, answer the user's question. If the context doesn't contain enough information to answer the question, say so.

Context:
{context}

Question: {query}

Answer:"""
    
    # Generate response
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    return response.text
