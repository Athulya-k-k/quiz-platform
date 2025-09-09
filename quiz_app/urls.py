# quiz_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    
    # Quiz URLs
    path('quizzes/', views.QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', views.QuizRetrieveUpdateDestroyView.as_view(), name='quiz-detail'),
    
    # Question URLs
    path('quizzes/<int:quiz_id>/questions/', views.QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', views.QuestionRetrieveUpdateDestroyView.as_view(), name='question-detail'),
    
    # Quiz Submission URLs
    path('quizzes/<int:quiz_id>/submit/', views.submit_quiz, name='submit-quiz'),
    path('my-submissions/', views.UserSubmissionsView.as_view(), name='user-submissions'),
    path('all-submissions/', views.AllSubmissionsView.as_view(), name='all-submissions'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission-detail'),
]