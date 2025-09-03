from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    nickname = fields.CharField(max_length=50, null=True)
    name = fields.CharField(max_length=50, null=True)
    phone = fields.CharField(max_length=20, null=True)
    is_verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    diaries: fields.ReverseRelation["Diary"]
