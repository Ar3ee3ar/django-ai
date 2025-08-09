from django.urls import path
from .views import chat_lang, check_user, log_out 

urlpatterns = [
    # path('', chat_view, name='chat')
    path('', check_user, name='sign-in'),
    path('log-out', log_out, name='log-out'),
    path('chat', chat_lang, name='chat')
]