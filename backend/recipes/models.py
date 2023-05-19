from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser

from .validators import hex_validation


class BaseNameModel(models.Model):
    """Абстрактная модель. Добавляет названия."""

    name = models.CharField(
        verbose_name="Название",
        help_text="Введите название",
        max_length=settings.CONTENT_MAX_LENGTH,
        error_messages={"unique": settings.UNIQUE_VALUE},
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Tags(BaseNameModel):
    """
    Модель Тэгов для рецептов. Например: 'Завтрак', 'Обед'.
    В модель добавлена функция автоматического присваивания SLUG при
    сохранении Тега, если поле оставлено пустым.
    """

    color = models.CharField(
        verbose_name="HEX код цвета",
        help_text="Введите HEX код цвета (например: #49B64E)",
        unique=True,
        max_length=settings.HEX_CODE_MAX_LENGTH,
        error_messages={"unique": settings.UNIQUE_VALUE},
        validators=[
            hex_validation,
        ],
    )
    slug = models.SlugField(
        verbose_name="Название slug",
        help_text="Введите название slug",
        unique=True,
        max_length=settings.CONTENT_MAX_LENGTH,
        error_messages={"unique": settings.UNIQUE_VALUE},
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        default_related_name = "tags"

    def __str__(self):
        return f"{self.name}"


class Ingredients(BaseNameModel):
    """
    Модель названий ингредиентов и соответствующим им единицам измерения.
    Единица измерения выбираются из пресета значений класса MeasurementUnit.
    """

    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        help_text="Введите единицу измерения ингредиента.",
        max_length=settings.CONTENT_MAX_LENGTH,
    )

    def __str__(self):
        return f"""{self.name} ({self.measurement_unit})"""

    class Meta:
        ordering = ("-id",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        indexes = [
            models.Index(fields=["name"], name="name_index"),
        ]


class Recipes(BaseNameModel):
    """Модель рецептов. Дата публикации присваивается автоматически."""

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        help_text="Введите дату публикации поста",
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name="Автор рецепта",
        help_text="Введите автора рецепта",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    text = models.TextField(
        verbose_name="Описание приготовления блюда",
        help_text="Введите описание приготовления блюда",
    )
    tags = models.ManyToManyField(Tags, related_name="tags")
    ingredients = models.ManyToManyField(
        Ingredients,
        through="IngredientsInRecipe",
        related_name="ingredients",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="recipes/images/",
    )
    cooking_time = models.IntegerField(
        verbose_name="Время приготовления (в минутах)",
        help_text="Введите время приготовления блюда в минутах",
        validators=[MinValueValidator(1, settings.LESS_THAN_ONE)],
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("-id",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        constraints = (
            models.UniqueConstraint(
                fields=("name", "author"),
                name="unique_for_author",
            ),
        )


class IngredientsInRecipe(models.Model):
    """Модель для связи рецепта и соответствующих ему ингредиентов."""

    recipe = models.ForeignKey(
        Recipes,
        verbose_name="Рецепт",
        on_delete=models.CASCADE,
        related_name="ingredient_list",
    )
    ingredient = models.ForeignKey(
        Ingredients,
        verbose_name="Ингредиент",
        on_delete=models.CASCADE,
        related_name="ingredient_list",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        help_text="Введите количество ингредиентов",
        validators=[
            MinValueValidator(
                settings.INGREDIENT_MIN_AMOUNT, settings.LESS_THAN_ONE
            )
        ],
    )

    def __str__(self):
        return f"{self.ingredient} {self.amount}"

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"],
                name="unique_ingredient_recipe",
            )
        ]


class FavoritesAndShopping(models.Model):
    """
    Абстрактная модель для формирования наследуемых моделей Favorites и
    ShoppingCart.
    """

    user = models.ForeignKey(
        CustomUser, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes, verbose_name="Рецепт", on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user} - {self.recipe}"


class Favorites(FavoritesAndShopping):
    """
    Модель для добавления рецептов в список избранного для формирования
    списка любимых рецептов на сайте.
    """

    class Meta(FavoritesAndShopping.Meta):
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        default_related_name = "favorites"
        constraints = (
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe",
            ),
        )


class ShoppingCart(FavoritesAndShopping):
    """
    Модель для добавления рецептов в корзину, для последующего формирования
    списка ингредиентов для покупки.
    """

    class Meta(FavoritesAndShopping.Meta):
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        default_related_name = "shopping_list"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping"
            )
        ]
