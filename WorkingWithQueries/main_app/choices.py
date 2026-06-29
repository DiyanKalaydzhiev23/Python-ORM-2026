from django.db import models

class LaptopChoice(models.TextChoices):
    ASUS = "Asus", "Asus"
    ACER = "Acer", "Acer"
    APPLE = "Apple", "Apple"
    LENOVO = "Lenovo", "Lenovo"
    DELL = "Dell", "Dell"


class OSChoice(models.TextChoices):
    WINDOWS = "Windows", "Windows"
    MACOS = "macOS", "macOS"
    LINUX = "Linux", "Linux"
    CHROME_OS = "Chrome OS", "Chrome OS"

