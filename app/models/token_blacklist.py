# app/models/token_blacklist.py
from tortoise.models import Model
from tortoise import fields

class TokenBlacklist(Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=512, unique=True)  # <- 수정
    created_at = fields.DatetimeField(auto_now_add=True)
