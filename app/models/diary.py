from tortoise.models import Model
from tortoise import fields
from .user import User

class Diary(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="diaries")
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    emotion_summary = fields.TextField(null=True)
    emotion = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    diary_tags: fields.ReverseRelation["DiaryTag"]
    diary_emotion_keywords: fields.ReverseRelation["DiaryEmotionKeyword"]
    transactions: fields.ReverseRelation["TransactionHistory"]
