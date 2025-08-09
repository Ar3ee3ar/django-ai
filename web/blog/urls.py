from django.urls import path
from .views import home, post_detail

urlpatterns = [
    path('', home),
    path('blog/<int:post_id>', post_detail, name="post_detail")
]