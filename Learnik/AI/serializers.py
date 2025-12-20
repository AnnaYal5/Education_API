from rest_framework import serializers

# ============ Конспект Serializer ============
class AICreateConspectSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=200, help_text="Тема для конспекту")
    text = serializers.CharField(required=False, allow_blank=True, help_text="Текст матеріалу")
    words_count = serializers.IntegerField(min_value=1, help_text="Кількість слів")
    language = serializers.CharField(max_length=50, help_text="Мова (uk, en, etc.)")
    complexity = serializers.CharField(max_length=50, help_text="Складність (easy, middle, hard)")
    style = serializers.CharField(max_length=50, help_text="Стиль тексту")
    font = serializers.CharField(max_length=50, help_text="Шрифт тексту")
    font_size = serializers.IntegerField(min_value=8, help_text="Розмір шрифту")

# ============ Тест Serializer ============
class AICreateTestSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=200, help_text="Тема для тесту")
    text = serializers.CharField(required=False, allow_blank=True, help_text="Текст матеріалу")
    questions_count = serializers.IntegerField(min_value=1, help_text="Кількість питань")
    difficulty = serializers.CharField(max_length=50, help_text="Рівень складності (easy, medium, hard)")
    language = serializers.CharField(max_length=50, help_text="Мова (uk, en, etc.)")
    font_size = serializers.IntegerField(min_value=8, help_text="Розмір шрифту")
    font = serializers.CharField(max_length=50, help_text="Шрифт тексту")

# ============ Книга Serializer ============
class AICreateBookSerializer(serializers.Serializer):
    text = serializers.CharField(help_text="Текст книги для аналізу")
    language = serializers.CharField(max_length=50, help_text="Мова (uk, en, etc.)")
    style = serializers.CharField(max_length=50, help_text="Стиль тексту")
    font_size = serializers.IntegerField(min_value=8, help_text="Розмір шрифту")
    font = serializers.CharField(max_length=50, help_text="Шрифт тексту")

# ============ Відповідь Serializer ============
class AIResponseSerializer(serializers.Serializer):
    text = serializers.CharField(help_text="HTML контент конспекту")