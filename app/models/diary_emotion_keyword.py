from tortoise.models import Model
from tortoise import fields
from .diary import Diary
from .emotion_keyword import EmotionKeyword

class DiaryEmotionKeyword(Model):
    id = fields.IntField(pk=True)
    diary = fields.ForeignKeyField("models.Diary", related_name="diary_emotion_keywords")
    emotion_keyword = fields.ForeignKeyField("models.EmotionKeyword", related_name="diary_emotion_keywords")
