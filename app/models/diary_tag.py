from tortoise.models import Model
from tortoise import fields
from .diary import Diary
from .tag import Tag

class DiaryTag(Model):
    id = fields.IntField(pk=True)
    diary = fields.ForeignKeyField("models.Diary", related_name="diary_tags")
    tag = fields.ForeignKeyField("models.Tag", related_name="diary_tags")
