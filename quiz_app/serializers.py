# quiz_app/serializers.py
from rest_framework import serializers
from .models import Category, Quiz, Question, QuizSubmission, SubmissionAnswer

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for Question model
    For admin users - includes correct answer
    """
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'quiz') 

class QuestionUserSerializer(serializers.ModelSerializer):
    """
    Serializer for Question model for normal users
    Excludes correct answer
    """
    class Meta:
        model = Question
        exclude = ('correct_answer',)
        read_only_fields = ('created_at', 'updated_at')

class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for Quiz model - detailed view with questions
    """
    questions = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_questions = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def get_questions(self, obj):
        # Return questions based on user type
        request = self.context.get('request')
        if request and request.user.is_admin:
            questions = obj.questions.all()
            return QuestionSerializer(questions, many=True).data
        else:
            # For normal users, only return active questions without correct answers
            questions = obj.questions.filter(is_active=True)
            return QuestionUserSerializer(questions, many=True).data

class QuizListSerializer(serializers.ModelSerializer):
    """
    Serializer for Quiz list view - without questions
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    total_questions = serializers.ReadOnlyField()
    
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'category', 'category_name', 'created_by', 'is_active', 'total_questions', 'created_at')

class SubmissionAnswerSerializer(serializers.ModelSerializer):
    """
    Serializer for individual submission answers
    """
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    correct_answer = serializers.CharField(source='question.correct_answer', read_only=True)
    
    class Meta:
        model = SubmissionAnswer
        fields = ('question', 'question_text', 'selected_answer', 'correct_answer', 'is_correct')
        read_only_fields = ('is_correct',)

class QuizSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz submissions
    """
    answers = SubmissionAnswerSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    percentage_score = serializers.ReadOnlyField()
    
    class Meta:
        model = QuizSubmission
        fields = '__all__'
        read_only_fields = ('user', 'score', 'submitted_at')

class QuizAttemptSerializer(serializers.Serializer):
    """
    Serializer for quiz attempt submission
    """
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(),
            required=True
        ),
        allow_empty=False
    )

    def validate_answers(self, value):
        """
        Validate that answers contain question_id and selected_answer
        """
        for answer in value:
            if 'question_id' not in answer or 'selected_answer' not in answer:
                raise serializers.ValidationError(
                    "Each answer must contain 'question_id' and 'selected_answer'"
                )
            if answer['selected_answer'] not in ['A', 'B', 'C', 'D']:
                raise serializers.ValidationError(
                    "Selected answer must be one of: A, B, C, D"
                )
        return value
    

