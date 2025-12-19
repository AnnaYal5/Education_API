from pydantic import BaseModel

class AIResponseModel(BaseModel):
    text: str


# ============ Конспекти =================
class AICreateConspectModel(BaseModel):
    topic: str
    words_count: int
    language: str
    complexity: int
    style: str
    font: str
    font_size: int

# ============ Тести =================
class AICreateTestModel(BaseModel):
    topic: str
    questions_count: int
    difficulty: str
    language: str
    font: str
    font_size: int

# ============ Книги =================
class AICreateBookModel(BaseModel):
    text: str
    style: str
    font: str
    font_size: int
    language: str