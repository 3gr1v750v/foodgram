from pathlib import Path


def delete_image(instance):
    """Удаление картинки, связанной с рецептом."""
    image = Path(instance.image.path)
    if image.exists():
        image.unlink()
