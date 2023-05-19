from django.db import IntegrityError
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorites,
    Ingredients,
    IngredientsInRecipe,
    Recipes,
    ShoppingCart,
    Tags,
)
from rest_framework import exceptions, relations, serializers, status
from users.models import CustomUser, Follow


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Определение логики сериализации объектов кастомной модели пользователя.
    """

    is_subscribed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )


class TagsSerializer(serializers.ModelSerializer):
    """Определение логики сериализации объектов модели Тегов."""

    class Meta:
        model = Tags
        fields = ("id", "name", "color", "slug")


class IngredientsInRecipeReadSerializer(serializers.ModelSerializer):
    """
    Определение логики сериализации для чтения (отображения) объектов модели
    ингредиентов в рецепте.
    """

    name = serializers.SlugRelatedField(
        source="ingredient", slug_field="name", read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source="ingredient", slug_field="measurement_unit", read_only=True
    )

    class Meta:
        model = IngredientsInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipesReadSerializer(serializers.ModelSerializer):
    """
    Определение логики сериализации для чтения (отображения) объектов модели
    рецептов.
    """

    image = Base64ImageField()
    tags = TagsSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.BooleanField(default=False, read_only=True)
    is_in_shopping_cart = serializers.BooleanField(
        default=False, read_only=True
    )
    ingredients = IngredientsInRecipeReadSerializer(
        many=True, read_only=True, source="ingredient_list"
    )

    class Meta:
        model = Recipes
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Определение логики сериализации объектов модели Ингредиентов."""

    class Meta:
        model = Ingredients
        fields = ("id", "name", "measurement_unit")


class IngredientsInRecipeWriteSerializer(serializers.ModelSerializer):
    """
    Определение логики сериализации для записи объектов модели ингредиентов
    в рецепте.
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())

    class Meta:
        model = IngredientsInRecipe
        fields = ("id", "amount")


class RecipesWriteSerializer(serializers.ModelSerializer):
    """
    Определение логики сериализации для записи объектов модели рецептов.
    - Запись изображение осуществляется в кодированном (base64) формате.
    - Список тегов и ингредиетов устанавливается через идентификаторы ('id')
    объектов этих моделей.
    """

    tags = relations.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsInRecipeWriteSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipes
        fields = (
            "id",
            "image",
            "tags",
            "author",
            "ingredients",
            "name",
            "text",
            "cooking_time",
        )
        read_only_fields = ("author",)

    @atomic
    def create_bulk_ingredients(self, ingredients, recipe):
        """Запись ингредиентов и их количества в рецепт."""
        for ingredient in ingredients:
            IngredientsInRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            )

    @atomic
    def create(self, validated_data):
        """
        Переопределение метода записи рецепта с дополнительной проверкой
        на наличие уникальной записи (условие на уровне модели) и отображением
        соответствующего текста ошибки.
        """
        try:
            ingredients_list = validated_data.pop("ingredients")
            tags = validated_data.pop("tags")
            author = self.context.get("request").user
            recipe = Recipes.objects.create(author=author, **validated_data)
            recipe.save()
            recipe.tags.set(tags)
            self.create_bulk_ingredients(ingredients_list, recipe)
            return recipe
        except IntegrityError:
            error_message = (
                "Название рецепта с данным именем у Вас уже существует!"
            )
            raise serializers.ValidationError({"error": error_message})

    @atomic
    def update(self, instance, validated_data):
        """Переопределение метода обновления записи рецепта."""
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_bulk_ingredients(recipe=instance, ingredients=ingredients)
        return super().update(instance, validated_data)

    def validate_ingredients(self, data):
        """Метод проверки уникальности и количества ингредиентов в рецепте."""
        ingredients = self.initial_data.get("ingredients")
        if len(ingredients) <= 0:
            raise exceptions.ValidationError(
                {"ingredients": "Невозможно добавить рецепт без ингредиентов!"}
            )
        ingredients_list = []
        for item in ingredients:
            if item["id"] in ingredients_list:
                raise exceptions.ValidationError(
                    {"ingredients": "Ингредиенты не могут повторяться!"}
                )
            ingredients_list.append(item["id"])
            if int(item["amount"]) <= 0:
                raise exceptions.ValidationError(
                    {
                        "amount": (
                            "Количество ингредиентов не" " может быть меньше 0"
                        )
                    }
                )
        return data

    def validate_cooking_time(self, data):
        """Метод проверки параметра времени приготовления рецепта."""
        cooking_time = self.initial_data.get("cooking_time")
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                {
                    "cooking_time": (
                        "Время приготовления рецепта "
                        "не может меньше и равным 0!"
                    )
                }
            )
        return data

    def validate_tags(self, data):
        """Метод проверки уникальности и наличия тегов в рецепте."""
        tags = self.initial_data.get("tags", False)
        if not tags:
            raise exceptions.ValidationError(
                {"tags": "Рецепт не может быть создан без тегов!"}
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise exceptions.ValidationError(
                    {"tags": "Нельзя использовать повторяющиеся теги!"}
                )
            tags_list.append(tag)
        return data

    def to_representation(self, instance):
        """
        Переопределение перечня полей, возвращаемых эндпоинтом при успешном
        завершении операции добавления/обновления данных рецепта.
        """
        request = self.context.get("request")
        context = {"request": request}
        return RecipesReadSerializer(instance, context=context).data


class RecipeShortRepresentationSerializer(serializers.ModelSerializer):
    """
    Определение логики сериализации для отображения сокращенного набора
    полей для объектов модели рецептов.
    """

    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ("id", "name", "image", "cooking_time")


class FollowSerializer(CustomUserSerializer):
    """
    Определение логики сериализации для объектов модели подписок пользователя.
    Эндпоинт поддерживает ограничение количества отображаемых рецептов
    пользователя с помощью параметра эндпоинта 'recipes_limit'.
    """

    recipes_count = serializers.IntegerField(read_only=True)
    recipes = RecipeShortRepresentationSerializer(many=True, read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )
        read_only_fields = ("email", "username", "last_name", "first_name")

    def validate(self, data):
        """
        Метод проверки уникальности записи и ограничение возможности подписки
        на самого себя.
        """
        author = self.instance
        user = self.context.get("request").user
        if Follow.objects.filter(user=user, author=author).exists():
            raise exceptions.ValidationError(
                detail="Подписка на этого автора уже существует!",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise exceptions.ValidationError(
                detail="Нельзя подписывать на самого себя.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class BaseFavoritesAndShoppingWriteSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для добавления рецептов в список избранного и корзину.
    """

    class Meta:
        abstract = True
        fields = ("user", "recipe")

    def validate(self, attrs):
        user = attrs["user"]
        recipe = attrs["recipe"]

        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError({"errors": [self.Meta.message]})

        return attrs

    def to_representation(self, instance):
        request = self.context.get("request")
        return RecipeShortRepresentationSerializer(
            instance.recipe, context={"request": request}
        ).data


class FavoritesWriteSerializer(BaseFavoritesAndShoppingWriteSerializer):
    """
    Определение логики сериализации для добавления рецептов в список
    избранного.
    """

    class Meta(BaseFavoritesAndShoppingWriteSerializer.Meta):
        model = Favorites
        message = "Рецепт уже добавлен в список избранного!"


class ShoppingCartWriteSerializer(BaseFavoritesAndShoppingWriteSerializer):
    """
    Определение логики сериализации для добавления рецептов в корзину (список
    покупок).
    """

    class Meta(BaseFavoritesAndShoppingWriteSerializer.Meta):
        model = ShoppingCart
        message = "Рецепт уже добавлен в список покупок!"
