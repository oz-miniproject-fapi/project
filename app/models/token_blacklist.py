from tortoise import fields, models

class TokenBlacklist(models.Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=512, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
