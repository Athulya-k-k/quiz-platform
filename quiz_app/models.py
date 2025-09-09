# quiz_app/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    """
    Quiz categories - only admins can create/edit categories
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Quiz(models.Model):
    """
    Quiz model - contains multiple questions
    Only active quizzes are visible to normal users
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"

    @property
    def total_questions(self):
        return self.questions.filter(is_active=True).count()

class Question(models.Model):
    """
    Question model - belongs to a quiz
    Has 4 options and one correct answer
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quiz.title} - Q{self.id}"

class QuizSubmission(models.Model):
    """
    User quiz submissions with answers and score
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_submissions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField()

    class Meta:
        # Prevent multiple submissions of same quiz by same user
        unique_together = ['user', 'quiz']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.total_questions})"

    @property
    def percentage_score(self):
        if self.total_questions == 0:
            return 0
        return (self.score / self.total_questions) * 100

class SubmissionAnswer(models.Model):
    """
    Individual answers for each question in a quiz submission
    """
    submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')]
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submission.user.username} - Q{self.question.id} - {self.selected_answer}"

    def save(self, *args, **kwargs):
        # Automatically check if answer is correct
        self.is_correct = self.selected_answer == self.question.correct_answer
        super().save(*args, **kwargs)