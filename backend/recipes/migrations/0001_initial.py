# Generated by Django 4.2.1 on 2023-05-15 10:42

import django.core.validators
import django.db.models.deletion
import recipes.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Favorites",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Избранный рецепт",
                "verbose_name_plural": "Избранные рецепты",
                "abstract": False,
                "default_related_name": "favorites",
            },
        ),
        migrations.CreateModel(
            name="Ingredients",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={
                            "unique": "Такое значение уже существует!"
                        },
                        help_text="Введите название",
                        max_length=200,
                        verbose_name="Название",
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(
                        help_text="Введите единицу измерения ингредиента.",
                        max_length=200,
                        verbose_name="Единица измерения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="IngredientsInRecipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveSmallIntegerField(
                        help_text="Введите количество ингредиентов",
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, "Значение должно быть больше 0!"
                            )
                        ],
                        verbose_name="Количество",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиент в рецепте",
                "verbose_name_plural": "Ингредиенты в рецепте",
            },
        ),
        migrations.CreateModel(
            name="Recipes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={
                            "unique": "Такое значение уже существует!"
                        },
                        help_text="Введите название",
                        max_length=200,
                        verbose_name="Название",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Введите дату публикации поста",
                        verbose_name="Дата публикации",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Введите описание приготовления блюда",
                        verbose_name="Описание приготовления блюда",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="recipes/images/",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "cooking_time",
                    models.IntegerField(
                        help_text="Введите время приготовления блюда в минутах",
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, "Значение должно быть больше 0!"
                            )
                        ],
                        verbose_name="Время приготовления (в минутах)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рецепт",
                "verbose_name_plural": "Рецепты",
                "ordering": ("-id",),
            },
        ),
        migrations.CreateModel(
            name="Tags",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        error_messages={
                            "unique": "Такое значение уже существует!"
                        },
                        help_text="Введите название",
                        max_length=200,
                        verbose_name="Название",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        error_messages={
                            "unique": "Такое значение уже существует!"
                        },
                        help_text="Введите HEX код цвета (например: #49B64E)",
                        max_length=7,
                        unique=True,
                        validators=[recipes.validators.hex_validation],
                        verbose_name="HEX код цвета",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        error_messages={
                            "unique": "Такое значение уже существует!"
                        },
                        help_text="Введите название slug",
                        max_length=200,
                        unique=True,
                        verbose_name="Название slug",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тэг",
                "verbose_name_plural": "Тэги",
                "ordering": ("id",),
                "default_related_name": "tags",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipes.recipes",
                        verbose_name="Рецепт",
                    ),
                ),
            ],
            options={
                "verbose_name": "Покупка",
                "verbose_name_plural": "Покупки",
                "abstract": False,
                "default_related_name": "shopping_list",
            },
        ),
    ]
