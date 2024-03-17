from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from quizbotapp.constants import BOT_WELCOME_MESSAGE
from quizbotapp.bot import generate_bot_responses

def bot_interaction(request):
    message = request.POST.get('message')
    session = request.session

    bot_responses = generate_bot_responses(message, session)
    
    return JsonResponse({'responses': bot_responses})


def bot_view(request):
    session = request.session
    message = request.POST.get('message')

    if not session.session_key:
        session.create()

    # Ensure that the session contains a valid current_question_id
    current_question_id = session.get("current_question_id", 0)

    bot_responses = generate_bot_responses(message, session)
    context = {'bot_responses': bot_responses}
    
    return render(request, 'index.html', context)