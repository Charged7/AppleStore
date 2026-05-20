from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# ─────────────────────────────────────
# БАЗОВИЙ ТОВАР
# ─────────────────────────────────────

class Product(models.Model):
    class CategoryChoices(models.TextChoices):
        IPHONE = "iphone", "iPhone"
        IPAD = "ipad", "iPad"
        MACBOOK = "macbook", "MacBook"
        IMAC = "imac", "iMac"
        WATCH = "watch", "Apple Watch"
        AIRPODS = "airpods", "AirPods"
        KEYBOARD = "keyboard", "Клавіатура"
        MOUSE = "mouse", "Мишка"

    category = models.CharField(
        max_length=20,
        choices=CategoryChoices,
        verbose_name="Категорія"
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Назва"
    )

    slug = models.SlugField(
        unique=True,
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=True,
        verbose_name="Опис"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активний"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ─────────────────────────────────────
# ВАРІАНТ ТОВАРУ
# (колір / пам'ять / ціна / залишок)
# ─────────────────────────────────────

class ProductVariant(models.Model):
    class StorageChoices(models.TextChoices):
        GB_64 = "64GB", "64 GB"
        GB_128 = "128GB", "128 GB"
        GB_256 = "256GB", "256 GB"
        GB_512 = "512GB", "512 GB"
        TB_1 = "1TB", "1 TB"
        TB_2 = "2TB", "2 TB"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Товар"
    )

    color = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Колір"
    )

    storage = models.CharField(
        max_length=20,
        choices=StorageChoices,
        blank=True,
        verbose_name="Пам'ять"
    )

    slug = models.SlugField(
        unique=True,
        max_length=255,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="Ціна"
    )

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="Стара ціна"
    )

    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Залишок"
    )

    is_new = models.BooleanField(
        default=False,
        verbose_name="Новинка"
    )

    new_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Новинка до"
    )

    class Meta:
        verbose_name = "Варіант товару"
        verbose_name_plural = "Варіанти товару"

    def __str__(self):
        return f"{self.product.name} | {self.color} | {self.storage}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(
                " ".join(
                    part
                    for part in [self.product.name, self.storage, self.color]
                    if part
                )
            )
            slug = base_slug
            counter = 2

            while ProductVariant.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0

    @property
    def is_new_active(self):
        return self.is_new and (
            self.new_until is None or self.new_until >= timezone.now()
        )


# ─────────────────────────────────────
# АТРИБУТИ
# (діагональ / RAM / chip / камера / батарея)
# ─────────────────────────────────────

class ProductAttribute(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attributes",
        verbose_name="Варіант товару"
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Назва атрибута"
    )

    value = models.CharField(
        max_length=255,
        verbose_name="Значення"
    )

    class Meta:
        verbose_name = "Атрибут товару"
        verbose_name_plural = "Атрибути товарів"

    def __str__(self):
        return f"{self.name}: {self.value}"


# ─────────────────────────────────────
# ФОТО
# ─────────────────────────────────────

class ProductImage(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Варіант товару"
    )

    image = models.ImageField(
        upload_to="products/%Y/%m/",
        verbose_name="Зображення"
    )

    alt = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Alt текст"
    )

    is_main = models.BooleanField(
        default=False,
        verbose_name="Головне фото"
    )

    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Порядок"
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Фото товару"
        verbose_name_plural = "Фото товарів"

    def __str__(self):
        return f"Фото {self.variant}"
