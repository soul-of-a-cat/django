import django.db.models


def normalize_name(name):
    name = name.lower()
    similar_chars = {
        "а": "a",
        "о": "o",
        "у": "y",
        "е": "e",
        "с": "c",
        "м": "m",
        "р": "p",
        "т": "t",
        "х": "x",
        "в": "b",
        "к": "k",
        "н": "h",
        "г": "r",
    }
    for word, replacement in similar_chars.items():
        name = name.replace(word, replacement)
    return name


class BaseModel(django.db.models.Model):
    normalized_name = django.db.models.CharField(
        unique=True,
        editable=False,
        max_length=150,
        validators=[
            django.core.validators.MaxLengthValidator(150),
        ],
    )

    def clean(self) -> None:
        normalized = normalize_name(self.name)
        existing = self.__class__.objects.filter(
            normalized_name=normalized,
        )
        if existing:
            raise django.core.exceptions.ValidationError({
                self.__class__.name.field.name: "Такое имя уже имеется",
            })
        self.normalized_name = normalized


class AbstractModel(BaseModel):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="max 150 символов",
        unique=True,
    )

    class Meta:
        abstract = True
