from django.urls import include, path
from rest_framework import routers

from .views import (CustomUserViewSet, IngredientViewSet, RecipesViewSet,
                    TagViewSet)

router = routers.DefaultRouter()
router.register("users", CustomUserViewSet, basename="users")
router.register("tags", TagViewSet, basename="tags")
router.register("recipes", RecipesViewSet, basename="recipes")
router.register("ingredients", IngredientViewSet, basename="ingredients")

app_name = "api"


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
