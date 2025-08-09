from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from django.conf import settings
import environ
from pathlib import Path
import os
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import SystemMessage, trim_messages, AIMessage, HumanMessage, BaseMessage
from typing import Sequence
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from langchain_core.runnables import RunnableConfig
from langchain_core.chat_history import InMemoryChatMessageHistory
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

#import function
# from chatbot.schema import State
from .chatbot.graph_node import get_chat_history
from .chatbot.graph import app


# chats_by_session_id = {}
# Here, we'll create a unique session ID to identify the conversation
# session_id = uuid.uuid4()
# config = {"configurable": {"session_id": session_id}}
# print(config)

# # update application's state
# class State(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], add_messages]
#     # language: str

# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Take environment variables from .env file
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# # Create your views here.
# client = OpenAI(api_key=env("OPEN_API_KEY"))
# os.environ['OPENAI_API_KEY'] = env("OPEN_API_KEY")
# os.environ['LANGSMITH_TRACING'] = "true"
# os.environ['LANGSMITH_API_KEY'] = env('LANGSMITH_API_KEY')
# model = init_chat_model("gpt-4o-mini", model_provider="openai")

# managing list of messages
# trimmer = trim_messages( # reduce how many message send to model
#     max_tokens=91, # How many tokens we want to keep
#     strategy="last",
#     token_counter=model,
#     include_system=True,
#     allow_partial=False,
#     start_on="human",
# )
# messages = []

# Cross Site Request Forgery protection
# when malicious website contain a link/JS to perform action
# to website using credential of user who visit malicious website
# related: use login credential to verify in bank app and transfer funds
# @csrf_exempt
# def chat_view(request):
#     if(request.method == 'POST'):
#         user_message = request.POST.get('message', '')
#         print(user_message)
#         response = client.chat.completions.create(
#             model =  "gpt-3.5-turbo",
#             messages = [
#                 {"role": "system", "content":"You are a helpful assistant."},
#                 {"role": "user", "content": user_message},
#             ],
#             max_tokens=150
#         )
#         print(response)
#         ai_message = response.choices[0].message.content
#         return JsonResponse({'message': ai_message})
#     return render(request, 'chat/chat.html')

# ------------------------------------------------------------------------------
@never_cache
def check_user(request):
    request.session["test"] = "working"
    # post = User.objects.get(username=username) # query: get data from id
    if(not request.user.is_authenticated): # if user not authenticated
        if request.method == "POST":
            try:
                already_login = request.session['login']
            except KeyError:
                already_login = request.session.get('login', False)
            if(not already_login):
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if(user is not None):
                    login(request, user)
                    request.session['thread_id'] = str(username)+str(password)
                    request.session['login'] = True
                    chat_history = get_chat_history(request.session['thread_id'])
                    if(list(chat_history.messages) != 0):
                        format_history = [
                            {"sender": msg.type, "text": msg.content}
                            for msg in chat_history.messages
                        ]
                    else:
                        format_history = None
                    return render(request, 'chat/chat.html',{
                        'chat_history': format_history
                    })
                # else:
                messages.error(request, 'Wrong username or password')
        return render(request, 'chat/login.html')
    else:
        # return render(request, 'chat/login.html')
        # return render(request, 'chat/login.html')
        chat_history = get_chat_history(request.session['thread_id'])
        if(list(chat_history.messages) != 0):
            format_history = [
                {"sender": msg.type, "text": msg.content}
                for msg in chat_history.messages
            ]
        else:
            format_history = None
        return render(request, 'chat/chat.html',{
            'chat_history': format_history
        })
    
def log_out(request):
    logout(request)
    request.session['login'] = False
    return redirect('/')

def check_session_integrity(request):
    if request.user.is_authenticated and 'thread_id' not in request.session:
        logout(request)
        return redirect('/')

# ----------------------------------------------------------------------
@csrf_exempt
@login_required(login_url='/sign-in')
def chat_lang(request):
    # # Define a new graph
    # workflow = StateGraph(state_schema=State)
    # # Define the (single) node in the graph
    # workflow.add_edge(START, "model")
    # workflow.add_node("model", call_model)

    # # Add memory
    # memory = MemorySaver()
    # app = workflow.compile()

    print(request)
    config = {"configurable": {"session_id": request.session['thread_id']}}
    print(config)
    chat_history = get_chat_history(request.session['thread_id'])
    if(list(chat_history.messages) != 0):
        format_history = [
            {"sender": msg.type, "text": msg.content}
            for msg in chat_history.messages
        ]
    else:
        format_history = None
    print('get chat history')
    # return render(request, 'chat/chat.html',{
    #     'chat_history': format_history
    # })

    # input_message = HumanMessage(content="hi! I'm bob")
    # for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    #     event["messages"][-1].pretty_print()

    # # Here, let's confirm that the AI remembers our name!
    # input_message = HumanMessage(content="what was my name?")
    # for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    #     event["messages"][-1].pretty_print()
    if(request.method == 'POST'):
        user_message = request.POST.get('message', '')
        print(user_message)
        input_messages = [HumanMessage(user_message)]
        response = app.invoke({"messages": input_messages}, config)
        ai_message = response["messages"][-1]
        print(response["messages"])
        return JsonResponse({'message': ai_message.content})

    return render(request, 'chat/chat.html',{
                        'chat_history': format_history
                    })

