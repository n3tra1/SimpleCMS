from humps import camelize
from tortoise import fields, models


class PydanticConfig:
    orm_mode = True
    alias_generator = camelize
    allow_population_by_field_name = True


class MainModelMixin(models.Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(null=False, auto_now_add=True)
    modified_at = fields.DatetimeField(null=False, auto_now=True)

    class Meta:
        abstract = True
