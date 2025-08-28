from tortoise.models import Model
from tortoise import fields
from .user import User
from .diary import Diary

class TransactionHistory(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="transactions")
    diary = fields.ForeignKeyField("models.Diary", null=True, related_name="transactions")
    type = fields.CharField(max_length=50)
    amount = fields.DecimalField(max_digits=12, decimal_places=2)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
