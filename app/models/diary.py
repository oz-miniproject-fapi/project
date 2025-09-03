from tortoise import fields, models

class Diary(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="diaries")
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Tag와 다대다
    tags: fields.ManyToManyRelation["Tag"] = fields.ManyToManyField(
        "models.Tag",
        related_name="diaries",   # Tag에서 접근할 때 diaries
        through="diary_tag"
    )

    # EmotionKeyword와 다대다
    emotion_keywords: fields.ManyToManyRelation["EmotionKeyword"] = fields.ManyToManyField(
        "models.EmotionKeyword",
        related_name="diaries",   # EmotionKeyword에서 접근할 때 diaries
        through="diary_emotion"
    )
