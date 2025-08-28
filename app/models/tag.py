from tortoise.models import Model
from tortoise import fields

class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    diary_tags: fields.ReverseRelation["DiaryTag"]
