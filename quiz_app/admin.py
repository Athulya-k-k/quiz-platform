# quiz_app/admin.py
from django.contrib import admin
from .models import Category, Quiz, Question, QuizSubmission, SubmissionAnswer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model
    """
    list_display = ('name', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

class QuestionInline(admin.TabularInline):
    """
    Inline admin for Questions within Quiz admin
    """
    model = Question
    extra = 1
    fields = ('question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'is_active')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """
    Admin configuration for Quiz model
    """
    list_display = ('title', 'category', 'created_by', 'is_active', 'total_questions', 'created_at')
    list_filter = ('is_active', 'category', 'created_at', 'created_by')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'total_questions')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Question model
    """
    list_display = ('quiz', 'question_text', 'correct_answer', 'is_active', 'created_at')
    list_filter = ('is_active', 'correct_answer', 'created_at', 'quiz')
    search_fields = ('question_text', 'quiz__title')
    readonly_fields = ('created_at', 'updated_at')

class SubmissionAnswerInline(admin.TabularInline):
    """
    Inline admin for SubmissionAnswers within QuizSubmission admin
    """
    model = SubmissionAnswer
    extra = 0
    readonly_fields = ('question', 'selected_answer', 'is_correct')

@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    """
    Admin configuration for QuizSubmission model
    """
    list_display = ('user', 'quiz', 'score', 'total_questions', 'percentage_score', 'submitted_at')
    list_filter = ('submitted_at', 'quiz', 'score')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('submitted_at', 'percentage_score')
    inlines = [SubmissionAnswerInline]

@admin.register(SubmissionAnswer)
class SubmissionAnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for SubmissionAnswer model
    """
    list_display = ('submission', 'question', 'selected_answer', 'is_correct')
    list_filter = ('is_correct', 'selected_answer')
    search_fields = ('submission__user__username', 'question__question_text')