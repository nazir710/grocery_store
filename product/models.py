"""Модели продукта, подкатегории, категории и списка покупок."""


from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from product.constants import Constants

User = get_user_model()


class BaseModel(models.Model):

    name = models.CharField(
        max_length=Constants.category_name_max_length,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=Constants.slug_max_length,
        unique=True,
        null=True,
        verbose_name='Слаг'
    )
    image = models.ImageField(
        upload_to='product/images/',
        null=True,
        default=None,
        verbose_name='Картинка'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    """Категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategory(BaseModel):
    """Подкатегории."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Продукты."""

    price = models.FloatField(
        default=Constants.price_default_value,
        verbose_name='Цена',
        validators=[
            MinValueValidator(Constants.price_min_value)
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='subcategory'
    )
    image_small = ImageSpecField(
        source='image',
        processors=[ResizeToFill(150, 150)],
        format='JPEG',
        options={'quality': 85}
    )

    image_medium = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 85}
    )

    image_large = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={'quality': 85}
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    """Список покупок."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Автор'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Продукт'
    )
    amount = models.PositiveSmallIntegerField(
        default=Constants.amount_default_value,
        verbose_name='Количество',
        validators=[
            MaxValueValidator(Constants.product_max_amount),
            MinValueValidator(Constants.product_min_amount)
        ]
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name="unique_shopping_cart"
            )
        ]

    def __str__(self):
        return self.product.name
