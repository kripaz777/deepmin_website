import difflib, os
from django.http import JsonResponse
from .models import QA
from django.views.decorators.csrf import csrf_exempt

# Optional Gemini integration (if GEMINI_API_KEY set)
USE_GEMINI = bool(os.getenv('GEMINI_API_KEY'))

def simple_gemini_fallback(prompt):
    # Placeholder for Gemini API call. In production replace with actual client usage.
    # Returns a short echo-like message as a fallback example.
    return 'AI fallback response: ' + (prompt[:300] + ('...' if len(prompt)>300 else ''))

@csrf_exempt
def chat_reply(request):
    user_msg = request.POST.get('message', '') if request.method=='POST' else request.GET.get('message','')
    user_msg = (user_msg or '').strip()
    if not user_msg:
        return JsonResponse({'response': "Please type a question."})

    all_qas = list(QA.objects.all())
    questions = [qa.question.lower() for qa in all_qas]

    if not questions:
        return JsonResponse({'response': "No knowledge base available. Please contact support."})

    match = difflib.get_close_matches(user_msg.lower(), questions, n=1, cutoff=0.65)
    if match:
        q = next((qa for qa in all_qas if qa.question.lower() == match[0]), None)
        if q:
            return JsonResponse({'response': q.answer})
    # fallback to Gemini if configured, otherwise simple fallback
    if USE_GEMINI:
        try:
            # Call Gemini API client here (user must configure GEMINI_API_KEY)
            return JsonResponse({'response': simple_gemini_fallback(user_msg)})
        except Exception:
            return JsonResponse({'response': "Sorry, couldn't fetch AI response."})
    else:
        return JsonResponse({'response': "Sorry, I couldn't find a close match. Try rephrasing or contact support."})
