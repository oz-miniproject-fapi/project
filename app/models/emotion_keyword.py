from tortoise import fields, models
from app.models.diary import Diary

class EmotionKeyword(models.Model):
    id = fields.IntField(pk=True)
    diary: fields.ForeignKeyRelation[Diary] = fields.ForeignKeyField(
        "models.Diary", related_name="emotion_keywords", on_delete=fields.CASCADE
    )
    word = fields.CharField(max_length=50)
    emotion = fields.CharField(max_length=10)  # 긍정, 부정, 중립

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
