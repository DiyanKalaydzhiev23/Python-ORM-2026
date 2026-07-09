from decimal import Decimal

from django.contrib.postgres.search import SearchVectorField
from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator
from django.db import models

from main_app.mixins import RechargeEnergyMixin
from main_app.validators import validate_name, validate_name_2, NameValidator


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            # validate_name,
            # validate_name_2("Name can only contain letters and spaces"),
            NameValidator()
        ]
    )
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                limit_value=18,
                message="Age must be greater than or equal to 18",
            )
        ]
    )
    email = models.EmailField(
        error_messages={'invalid': 'Enter a valid email address'}
    )
    phone_number = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+359\d{9}$',
                message="Phone number must start with '+359' followed by 9 digits",
            )
        ],
    )
    website_url = models.URLField(
        error_messages={'invalid': "Enter a valid URL"}
    )


class BaseMedia(models.Model):
    title = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    genre = models.CharField(
        max_length=50,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']  # Happens on SELECT not in the DB


class Book(BaseMedia):
    AUTHOR_MAX_LENGTH_VALUE: int = 100
    AUTHOR_MIN_LENGTH_VALUE: int = 5
    ISBN_MAX_LENGTH_VALUE: int = 20
    ISBN_MIN_LENGTH_VALUE: int = 6

    author = models.CharField(
        max_length=AUTHOR_MAX_LENGTH_VALUE,
        validators=[
            MinLengthValidator(
                limit_value=AUTHOR_MIN_LENGTH_VALUE,
                message=f"Author must be at least {AUTHOR_MIN_LENGTH_VALUE} characters long"
            )
        ],
    )
    isbn = models.CharField(
        max_length=ISBN_MAX_LENGTH_VALUE,
        unique=True,
        validators=[
            MinLengthValidator(
                limit_value=ISBN_MIN_LENGTH_VALUE,
                message=f"ISBN must be at least {ISBN_MIN_LENGTH_VALUE} characters long"
            )
        ],
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Book"
        verbose_name_plural = "Models of type - Book"


class Movie(BaseMedia):
    DIRECTOR_MAX_LENGTH: int = 100
    DIRECTOR_MIN_LENGTH: int = 8

    director = models.CharField(
        max_length=DIRECTOR_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                limit_value=DIRECTOR_MIN_LENGTH,
                message=f"Director must be at least {DIRECTOR_MIN_LENGTH} characters long"
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"


class Music(BaseMedia):
    ARTIST_MAX_LENGTH: int = 100
    ARTIST_MIN_LENGTH: int = 9

    artist = models.CharField(
        max_length=ARTIST_MAX_LENGTH,
        validators=[
            MinLengthValidator(
                limit_value=ARTIST_MIN_LENGTH,
                message=f"Artist must be at least {ARTIST_MIN_LENGTH} characters long"
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"


class Product(models.Model):
    TAX_PERCENT: Decimal = Decimal('0.08')
    WEIGHT_MULTIPLIER: Decimal = Decimal('2')
    PRODUCT_NAME: str = "Product"

    name = models.CharField(
        max_length=100,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def calculate_tax(self) -> Decimal:
        return Decimal(str(self.price)) * self.TAX_PERCENT

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return self.WEIGHT_MULTIPLIER * weight

    def format_product_name(self) -> str:
        return f"{self.PRODUCT_NAME}: {self.name}"


class DiscountedProduct(Product):
    PRICE_WITHOUT_DISCOUNT_MULTIPLIER: Decimal = Decimal('0.20')
    TAX_PERCENT: Decimal = Decimal('0.05')
    WEIGHT_MULTIPLIER: Decimal = Decimal('1.50')
    PRODUCT_NAME: str = "Discounted Product"

    def calculate_price_without_discount(self) -> Decimal:
        return Decimal(str(self.price)) * (Decimal('1') + self.PRICE_WITHOUT_DISCOUNT_MULTIPLIER)

    class Meta:
        proxy = True


class Hero(models.Model, RechargeEnergyMixin):
    REQUIRED_ENERGY: int = 0

    name = models.CharField(
        max_length=100,
    )
    hero_title = models.CharField(
        max_length=100,
    )
    energy = models.PositiveIntegerField()

    @property
    def not_enough_energy_message(self) -> str:
        raise NotImplemented

    @property
    def successful_ability_usage_message(self) -> str:
        raise NotImplemented

    def use_ability(self) -> str:
        if self.energy < self.REQUIRED_ENERGY:
            return self.not_enough_energy_message

        self.energy = max(self.energy - self.REQUIRED_ENERGY, 1)

        return self.successful_ability_usage_message


class FlashHero(Hero):
    REQUIRED_ENERGY: int = 65

    @property
    def not_enough_energy_message(self) -> str:
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def successful_ability_usage_message(self) -> str:
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    def run_at_super_speed(self) -> str:
        return self.use_ability()

    class Meta:
        proxy = True


class SpiderHero(Hero):
    REQUIRED_ENERGY: int = 80

    @property
    def not_enough_energy_message(self) -> str:
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def successful_ability_usage_message(self) -> str:
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    def swing_from_buildings(self) -> str:
        return self.use_ability()

    class Meta:
        proxy = True


class Document(models.Model):
    title = models.CharField(
        max_length=200,
    )
    content = models.TextField()

    # The running brown dog is in a run
    # STEP 1 tokenization -> [The, running, brown, dog, is, in, a, run]
    # STEP 2 remove stop words -> [running, brown, dog, run]
    # STEP 3 create lexems -> [run, brown, dog] -> [run: 2, 8; brown: 3, dog: 4]

    search_vector = SearchVectorField(
        null=True,
        db_index=True,
    )



