from tortoise.models import Model
from tortoise import fields
from .user import User

class EmotionStats(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="emotion_stats")
    period = fields.CharField(max_length=50)
    emotion = fields.CharField(max_length=50)
    count = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
