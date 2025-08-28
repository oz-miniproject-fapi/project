from tortoise.models import Model
from tortoise import fields
from .user import User

class AlertLog(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="alert_logs")
    message = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
