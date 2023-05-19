from urllib.parse import unquote

from django.conf import settings
from django.db.models import Count, Exists, OuterRef, Sum, Value
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from recipes.models import (
    Favorites,
    Ingredients,
    IngredientsInRecipe,
    Recipes,
    ShoppingCart,
    Tags,
)
from users.models import CustomUser, Follow

from .filters import RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import AuthorOrReadOnly
from .serializers import (
    CustomUserSerializer,
    FavoritesWriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeShortRepresentationSerializer,
    RecipesReadSerializer,
    RecipesWriteSerializer,
    ShoppingCartWriteSerializer,
    TagsSerializer,
)
from .utils import (
    ingredients_export,
    prihibited_method_response,
    serializer_add_delete,
)


class CustomUserViewSet(UserViewSet):
    """
    Представление данных модели пользователя на основе измененной модели
    Djoser.
    """

    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, *args, **kwargs):
        return prihibited_method_response(request)

    def partial_update(self, request, *args, **kwargs):
        return prihibited_method_response(request)

    @action(detail=False, methods=["post"], url_path="set_email")
    def set_email(self, request):
        return prihibited_method_response(request)

    def get_queryset(self):
        """
        Переопределение запроса набора объектов пользователей (по умолчанию
        "list" запрос djoser отображает данные только одного пользователя).
        Добавление поля is_subscribed для определения наличия подписки
        на других авторов.
        """

        return CustomUser.objects.annotate(
            is_subscribed=Exists(
                self.request.user.follower.filter(author=OuterRef("pk"))
            )
            if self.request.user.is_authenticated
            else Value(False)
        )

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, **kwargs):
        """
        Энедпоинт для добавления / удаления подписки на пользователя.
        Доступно только авторизованным пользователям.
        """
        user = request.user
        author_id = self.kwargs.get("id")
        author = get_object_or_404(CustomUser, id=author_id)
        if request.method == "POST":
            serializer = FollowSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        get_object_or_404(Follow, user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=["GET"], permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        """
        Эндпоинт для отображения списка авторов на которых подписан
        пользователь. Сериализатор дополнительно отображает список рецептов
        пользователей и их общее количество для каждого автора в списке.
        Количество рецептов в эндпоинте может быть ограничено запросом
        'recipes_limit=<integer>'.
        """
        queryset = (
            CustomUser.objects.filter(following__user=request.user)
            .prefetch_related("recipes")
            .annotate(is_subscribed=Value(True))
            .annotate(recipes_count=Count("recipes"))
            .order_by("-id")
        )
        serializer = FollowSerializer(
            self.paginate_queryset(queryset),
            many=True,
            context={"request": request},
        )
        serialized_data = serializer.data

        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit:
            recipes_limit = int(recipes_limit)
            for data in serialized_data:
                user = get_object_or_404(CustomUser, id=data["id"])
                recipe_serializer = RecipeShortRepresentationSerializer(
                    user.recipes.all()[:recipes_limit],
                    many=True,
                    read_only=True,
                )
                data["recipes"] = recipe_serializer.data

        return self.get_paginated_response(serialized_data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление данных модели тегов. Для внесения изменений в
    модель данных, воспользуйтесь панелью администратора.
    """

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление данных модели ингредиентов."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        """
        Переопределение запроса набора объектов ингредиентов в соответствии
        с параметрами запроса.
        """
        name = self.request.query_params.get("name")
        queryset = super().queryset()
        if name:
            if name[0] == "%":
                name = unquote(name)
            else:
                name = name.translate(settings.INCORRECT_LAYOUT)
            name = name.lower()
            start_queryset = list(queryset.filter(name__istartswith=name))
            ingredients_set = set(start_queryset)
            cont_queryset = queryset.filter(name__icontains=name)
            start_queryset.extend(
                [ing for ing in cont_queryset if ing not in ingredients_set]
            )
            queryset = start_queryset
        return queryset


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Представление данных модели рецептов. В представлении используются
    два отдельных серилизатора для чтения и записи объектов модели.
    """

    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        """
        Добавление поля is_favorited для определения добавления рецепта
        в избранное.
        Добавление поля is_in_shopping_cart для определения добавления рецепта
        в список покупок.
        """
        return Recipes.objects.annotate(
            is_favorited=Exists(
                self.request.user.favorites.filter(recipe=OuterRef("pk"))
            )
            if self.request.user.is_authenticated
            else Value(False),
            is_in_shopping_cart=Exists(
                self.request.user.shopping_list.filter(recipe=OuterRef("pk"))
            )
            if self.request.user.is_authenticated
            else Value(False),
        )

    def get_serializer_class(self):
        """
        Изменение типа вызываемого сериализатора, в зависимости от метода
        запроса.
        """
        if self.request.method in ("POST", "PUT", "PATCH"):
            return RecipesWriteSerializer
        return RecipesReadSerializer

    def get_permissions(self):
        """
        Дополнительные условия на определение прав доступа для изначального
        создания объекта модели и изменение уже созданных объектов.
        """
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        """Эндпоинт для добавления / удаления рецепта в список избранного."""
        return serializer_add_delete(
            FavoritesWriteSerializer, Favorites, request, pk
        )

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        """Эндпоинт для добавления / удаления рецепта в корзину."""
        return serializer_add_delete(
            ShoppingCartWriteSerializer, ShoppingCart, request, pk
        )

    @action(
        detail=False, methods=["GET"], permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """
        Эндпоинт для выгрузки списка ингредиентов всех рецептов, находящихся
        в корзине (списке покупок) пользователей. Одинаковые ингредиенты
        суммируются по количеству.
        """
        ingredients = (
            IngredientsInRecipe.objects.filter(
                recipe__shopping_list__user=self.request.user
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .order_by("ingredient__name")
            .annotate(amount=Sum("amount"))
        )
        return ingredients_export(self, request, ingredients)
