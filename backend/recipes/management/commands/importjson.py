import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredients

FILE_DIR = Path(settings.BASE_DIR).parent / "data"
JSON_FILE_PATH = FILE_DIR / "ingredients.json"


class Command(BaseCommand):
    help = "Импорт данных из файла JSON в таблицу Ingredients."

    def handle(self, *args, **kwargs):
        if not JSON_FILE_PATH.exists():
            raise CommandError(
                f"JSON файл по адресу {FILE_DIR} - {JSON_FILE_PATH} не был найден."
            )

        if Ingredients.objects.exists():
            raise CommandError("Очистите базу перед загрузкой JSON файла.")

        try:
            with open(JSON_FILE_PATH, encoding="utf-8") as file:
                ingredient_data = json.load(file)
                ingredients = [
                    Ingredients(**ingredient) for ingredient in ingredient_data
                ]
                Ingredients.objects.bulk_create(
                    ingredients, ignore_conflicts=True
                )

        except Exception as e:
            raise CommandError(
                "Ошибка выполнения команды importjson. Проверьте целостность "
                "JSON файла."
            ) from e

        self.stdout.write(
            self.style.SUCCESS(f"Фаил {file.name} успешно импортирован.")
        )
