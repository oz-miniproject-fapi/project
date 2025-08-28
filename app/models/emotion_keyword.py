from tortoise.models import Model
from tortoise import fields

class EmotionKeyword(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    emotion = fields.CharField(max_length=50)

    diary_emotion_keywords: fields.ReverseRelation["DiaryEmotionKeyword"]
