from tortoise import fields, models

class EmotionKeyword(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    # Diary 모델과 다대다 관계 (backward relation 이름 충돌 방지)
    diaries: fields.ManyToManyRelation["Diary"]
