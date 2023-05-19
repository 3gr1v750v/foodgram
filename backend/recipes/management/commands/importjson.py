import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredients

JSON_FILE_PATH = settings.DATABASE_FILE_UPLOAD_FOLDER / "ingredients.json"


class Command(BaseCommand):
    help = "Импорт данных из файла JSON в таблицу Ingredients."

    def handle(self, *args, **kwargs):
        if not JSON_FILE_PATH.exists():
            raise FileNotFoundError(
                f"JSON файл по адресу {JSON_FILE_PATH} не был найден."
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

        except json.JSONDecodeError as e:
            raise CommandError(
                f"Ошибка выполнения команды importjson. "
                f"Ошибка разбора JSON: {str(e)}"
            ) from e

        self.stdout.write(
            self.style.SUCCESS(f"Фаил {file.name} успешно импортирован.")
        )
