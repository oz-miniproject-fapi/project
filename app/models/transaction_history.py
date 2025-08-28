from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.user import User
from app.models.diary import Diary  # Diary 모델 존재 시

class TransactionHistory(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="transactions")
    diary = fields.ForeignKeyField("models.Diary", related_name="transactions", null=True)
    type = fields.CharField(max_length=50)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

# Pydantic 모델 생성
TransactionHistory_Pydantic = pydantic_model_creator(TransactionHistory, name="TransactionHistory")
TransactionHistoryIn_Pydantic = pydantic_model_creator(
    TransactionHistory, name="TransactionHistoryIn", exclude_readonly=True
)
