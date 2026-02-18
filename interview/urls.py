from django import views
from django.urls import path
from .views import home, question_page, question_page, start_interview_by_language, submit_answer, result

urlpatterns = [
    path("", home, name="home"),
    path("interview/<str:language>/", start_interview_by_language, name="language_interview"),
    path('question/', question_page, name='question_page'),
    path("submit/", submit_answer, name="submit_answer"),
    path("result/", result, name="result"),
]