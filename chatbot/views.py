import difflib
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import QA, Document, DocumentChunk, ChatBotConfig
from .utils import (
    generate_query_embedding,
    find_relevant_chunks,
    generate_answer_with_gemini
)

def get_gemini_api_key():
    config = ChatBotConfig.objects.filter(is_active=True).last()
    return config.gemini_api_key if config else None


@csrf_exempt
def chat_reply(request):
    """Handle chat messages with RAG retrieval"""
    user_msg = request.POST.get('message', '') if request.method == 'POST' else request.GET.get('message', '')
    user_msg = (user_msg or '').strip()
    
    if not user_msg:
        return JsonResponse({'response': "Please type a question."})
    
    
    # Try RAG first if available
    api_key = get_gemini_api_key()
    if api_key:
        try:
            # Get all completed documents
            completed_docs = Document.objects.filter(status='completed')
            
            if completed_docs.exists():
                # Generate query embedding
                query_embedding = generate_query_embedding(user_msg, api_key)
                
                # Get all chunks from completed documents
                all_chunks = DocumentChunk.objects.filter(document__in=completed_docs)
                
                # Find relevant chunks
                relevant_chunks = find_relevant_chunks(query_embedding, all_chunks, top_k=3)
                
                # If we have relevant chunks with good similarity (>0.5)
                if relevant_chunks and relevant_chunks[0][1] > 0.5:
                    # Extract chunk texts
                    context_chunks = [chunk.chunk_text for chunk, score in relevant_chunks]
                    
                    # Generate answer with Gemini
                    answer = generate_answer_with_gemini(user_msg, context_chunks, api_key)
                    
                    # Add source information
                    sources = list(set([chunk.document.original_filename for chunk, _ in relevant_chunks]))
                    source_info = f"\n\n📚 Sources: {', '.join(sources)}"
                    
                    return JsonResponse({
                        'response': answer + source_info,
                        'sources': sources,
                        'method': 'rag'
                    })
        
        except Exception as e:
            print(f"RAG error: {e}")
            # Fall through to Q&A matching
    
    # Fallback to traditional Q&A matching
    all_qas = list(QA.objects.all())
    questions = [qa.question.lower() for qa in all_qas]
    
    if not questions:
        return JsonResponse({
            'response': "No knowledge base available. Please upload documents or contact support.",
            'method': 'none'
        })
    
    match = difflib.get_close_matches(user_msg.lower(), questions, n=1, cutoff=0.65)
    if match:
        q = next((qa for qa in all_qas if qa.question.lower() == match[0]), None)
        if q:
            return JsonResponse({
                'response': q.answer,
                'method': 'qa'
            })
    
    # Final fallback
    return JsonResponse({
        'response': "Sorry, I couldn't find an answer. Try uploading relevant documents or rephrasing your question.",
        'method': 'none'
    })
