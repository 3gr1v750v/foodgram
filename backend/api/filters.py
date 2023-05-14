from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipes
from users.models import CustomUser


class RecipeFilter(FilterSet):
    """
    Набор фильтров, которые можно применить к запросам, чтобы фильтровать
    объекты модели Recipe:

    - tags: фильтр ищет объекты рецептов, у которых значение поля "slug"
    совпадает с указанными значениями.
    - author: фильтр позволяет выбрать объекты рецептов, у которых поле
    "author" (автор) совпадает с выбранным значением.
    """

    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )

    def filter_is_favorited(self, queryset, name, value):
        """
        Фильтр возвращает объекты рецептов, которые находятся в избранном
        для данного пользователя.
        """
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """
        Фильтр возвращает объекты рецептов, которые находятся в корзине
        для данного пользователя.
        """
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_list__user=self.request.user)
        return queryset

    class Meta:
        model = Recipes
        fields = ("tags", "author", "is_favorited", "is_in_shopping_cart")
