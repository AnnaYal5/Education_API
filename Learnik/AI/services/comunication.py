from google import genai
from google.genai.types import GenerateContentResponse
from google.genai.types import GenerateContentConfig, Tool, GoogleSearch

from app_config import config

class AICommunicator:
    def __init__(self):
        self.client = genai.Client(
            api_key=config.ai_api_key
        )

    async def __generate_anser(self, system_prompt: str, user_prompt: str) -> GenerateContentResponse:
        """
        Функція для генерації відповіді від AI-моделі на основі заданих системних та користувацьких підказок.

        Вхідні параметри:
        - system_prompt (str): Підказка, що визначає поведінку моделі.
        - user_prompt (str): Підказка, що містить запит користувача

        Вихідні дані:
        - GenerateContentResponse: Відповідь від AI-моделі.
        """

        tools = [
            Tool(
                google_search=GoogleSearch()
            )
        ]

        async with self.client.aio as client:
            response = await client.models.generate_content(
                model=config.ai_model,
                contents=user_prompt,
                config=GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                    tools=tools
                )
            )
        
        return response

    async def generate_conspect(self, theme: str, count_words: int, language: str, complexity: int, style: str, font: str, size_font: int) -> str:

        """
        Функція для генерації конспекту на задану тему з використанням AI-моделі.

        Вхідні параметри:
        - theme (str): Тема конспекту.
        - count_papers (int): Кількість сторінок конспекту.
        - language (str): Мова конспекту.
        - complexity (int): Рівень складності конспекту (1-5).
        - style (str): Стиль написання конспекту.
        - font (str): Шрифт для конспекту.
        - size_font (int): Розмір шрифту для конспекту.
        Вихідні дані:
        - str: Згенерований конспект у форматі HTML.
        """

        user_prompt = f"""Generate a complete academic paper in HTML format.

            Topic: {theme}
            Length: {count_words} words
            Language: {language} (ALL content must be in {language})
            Complexity: Level {complexity}
            Style: {style}
            Font: {font}
            Font Size: {size_font}pt

            Include all required sections (title page, abstract, table of contents, introduction, literature review, main content with 3-5 sections, discussion, conclusion, references with 10-15+ sources). Ensure proper HTML structure, appropriate depth for complexity level {complexity}, and consistent {style} writing style throughout. Output complete HTML ready for PDF conversion."""
        
        response = await self.__generate_anser(
            system_prompt=config.conspect_system_prompt,
            user_prompt=user_prompt
        )

        return response.text
    
    async def generate_test(self, theme: str, count_questions: int, difficulty: str, language: str, font: str, font_size: int) -> str:
        """
        Функція для генерації тесту на задану тему з використанням AI-моделі.

        Вхідні параметри:
        - topic (str): Тема тесту.
        - num_questions (int): Кількість питань у тесті.
        - difficulty (str): Рівень складності тесту (наприклад, "легкий", "середній", "важкий").
        - language (str): Мова тесту.

        Вихідні дані:
        - str: Згенерований тест у форматі тексту.
        """


        user_prompt = f"""
            Generate a test on the topic: {theme}
            Number of questions: {count_questions}
            Difficulty level: {difficulty} 
            Language: {language} (ALL content must be in {language})
            Font: {font}
            Font Size: {font_size}pt
            The test should include a variety of question types (multiple choice, true/false, short answer) and cover key concepts related to the topic. Provide clear instructions for each section and ensure the questions are appropriately challenging for the specified difficulty level.
        """

        response = await self.__generate_anser(
            system_prompt=config.test_system_prompt,
            user_prompt=user_prompt
        )

        return response.text
    
    async def generate_book(self, text: str, style: str, language: str, font: str, size_font: int) -> str:
        """
        Функція для генерації книги на основі заданого тексту з використанням AI-моделі.

        Вхідні параметри:
        - text (str): Текст для створення книги.
        - style (str): Стиль написання книги.
        - language (str): Мова книги.
        - font (str): Шрифт для книги.
        - size_font (int): Розмір шрифту для книги.

        Вихідні дані:
        - str: Згенерована книга у форматі тексту.
        """

        user_prompt = f"""
            Create a book based on the following text: {text}
            Writing Style: {style}
            language: {language} (ALL content must be in {language})
            Font: {font}
            Font Size: {size_font}pt
            """
        
        response = await self.__generate_anser(
            system_prompt=config.book_system_prompt,
            user_prompt=user_prompt
        )

        return response.text