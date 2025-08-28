from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    nickname = fields.CharField(max_length=50, null=True)
    name = fields.CharField(max_length=50, null=True)
    phone_number = fields.CharField(max_length=20, null=True)
    last_login = fields.DatetimeField(null=True)
    is_staff = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    diaries: fields.ReverseRelation["Diary"]
    emotion_stats: fields.ReverseRelation["EmotionStats"]
    alert_logs: fields.ReverseRelation["AlertLog"]
    transactions: fields.ReverseRelation["TransactionHistory"]
