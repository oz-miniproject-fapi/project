# app/models/user.py
from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    nickname = fields.CharField(max_length=50, null=True)
    name = fields.CharField(max_length=50, null=True)
    phone_number = fields.CharField(max_length=20, null=True)
    is_active = fields.BooleanField(default=False)  # 이메일 인증 전 False
    is_staff = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def set_password(self, raw_password: str):
        self.password = bcrypt.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return bcrypt.verify(raw_password, self.password)
