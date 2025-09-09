# quiz_app/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Category, Quiz, Question, QuizSubmission, SubmissionAnswer
from .serializers import (
    CategorySerializer, QuizSerializer, QuizListSerializer, QuestionSerializer,
    QuizSubmissionSerializer, QuizAttemptSerializer
)
from .permissions import IsAdminUser, IsAdminOrReadOnly, IsOwnerOrAdmin

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new category (admin only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category (admin only for update/delete)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

# Quiz Views
class QuizListCreateView(generics.ListCreateAPIView):
    """
    List all quizzes or create a new quiz
    Normal users see only active quizzes, admins see all
    """
    serializer_class = QuizListSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Quiz.objects.all().select_related('category', 'created_by')
        return Quiz.objects.filter(is_active=True).select_related('category', 'created_by')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a quiz
    Normal users can only view active quizzes, admins can do everything
    """
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Quiz.objects.all().prefetch_related('questions')
        return Quiz.objects.filter(is_active=True).prefetch_related('questions__quiz')

    def update(self, request, *args, **kwargs):
        # Only admin users can update quizzes
        if not request.user.is_admin:
            return Response(
                {"detail": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only admin users can delete quizzes
        if not request.user.is_admin:
            return Response(
                {"detail": "You don't have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

# Question Views
class QuestionListCreateView(generics.ListCreateAPIView):
    """
    List all questions for a specific quiz or create a new question (admin only)
    """
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        return Question.objects.filter(quiz_id=quiz_id)

    def perform_create(self, serializer):
        quiz_id = self.kwargs.get('quiz_id')
        quiz = get_object_or_404(Quiz, id=quiz_id)
        serializer.save(quiz=quiz)

    

class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a question (admin only)
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]

# Quiz Submission Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request, quiz_id):
    """
    Submit answers for a quiz
    Calculates score automatically and prevents duplicate submissions
    """
    # Check if user is admin - admins shouldn't submit quizzes
    if request.user.is_admin:
        return Response(
            {"detail": "Admin users cannot submit quiz attempts."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Get the quiz
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Check if user has already submitted this quiz
    if QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists():
        return Response(
            {"detail": "You have already submitted this quiz."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate submission data
    serializer = QuizAttemptSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    answers_data = serializer.validated_data['answers']
    
    # Get active questions for this quiz
    questions = quiz.questions.filter(is_active=True)
    question_ids = list(questions.values_list('id', flat=True))
    
    # Validate that all questions are answered
    submitted_question_ids = [int(ans['question_id']) for ans in answers_data]
    if set(submitted_question_ids) != set(question_ids):
        return Response(
            {"detail": "You must answer all questions."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Process submission
    try:
        with transaction.atomic():
            # Create quiz submission
            submission = QuizSubmission.objects.create(
                user=request.user,
                quiz=quiz,
                total_questions=len(questions)
            )
            
            correct_answers = 0
            
            # Create individual answers
            for answer_data in answers_data:
                question = get_object_or_404(Question, id=answer_data['question_id'])
                
                submission_answer = SubmissionAnswer.objects.create(
                    submission=submission,
                    question=question,
                    selected_answer=answer_data['selected_answer']
                )
                
                if submission_answer.is_correct:
                    correct_answers += 1
            
            # Update submission score
            submission.score = correct_answers
            submission.save()
            
            return Response(
                QuizSubmissionSerializer(submission).data,
                status=status.HTTP_201_CREATED
            )
            
    except Exception as e:
        return Response(
            {"detail": f"Error processing submission: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class UserSubmissionsView(generics.ListAPIView):
    """
    List all quiz submissions for the current user
    """
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizSubmission.objects.filter(user=self.request.user).select_related('quiz')

class AllSubmissionsView(generics.ListAPIView):
    """
    List all quiz submissions (admin only)
    """
    queryset = QuizSubmission.objects.all().select_related('user', 'quiz')
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAdminUser]

class SubmissionDetailView(generics.RetrieveAPIView):
    """
    Retrieve detailed submission with answers
    Users can only view their own submissions, admins can view all
    """
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return QuizSubmission.objects.all().prefetch_related('answers__question')
        return QuizSubmission.objects.filter(user=self.request.user).prefetch_related('answers__question')