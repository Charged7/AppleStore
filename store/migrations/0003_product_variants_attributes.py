# Generated after switching store models to Product + Variant + Attribute.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_alter_product_category_delete_category"),
    ]

    operations = [
        migrations.DeleteModel(
            name="AirPodsSpec",
        ),
        migrations.DeleteModel(
            name="AppleKeyboardSpec",
        ),
        migrations.DeleteModel(
            name="AppleMouseSpec",
        ),
        migrations.DeleteModel(
            name="AppleWatchSpec",
        ),
        migrations.DeleteModel(
            name="IMacSpec",
        ),
        migrations.DeleteModel(
            name="IPadSpec",
        ),
        migrations.DeleteModel(
            name="IPhoneSpec",
        ),
        migrations.DeleteModel(
            name="MacBookSpec",
        ),
        migrations.DeleteModel(
            name="ProductImage",
        ),
        migrations.RemoveField(
            model_name="product",
            name="old_price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="sku",
        ),
        migrations.RemoveField(
            model_name="product",
            name="stock",
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name="ProductVariant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Колір",
                    ),
                ),
                (
                    "storage",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("64GB", "64 GB"),
                            ("128GB", "128 GB"),
                            ("256GB", "256 GB"),
                            ("512GB", "512 GB"),
                            ("1TB", "1 TB"),
                            ("2TB", "2 TB"),
                        ],
                        max_length=20,
                        verbose_name="Пам'ять",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        verbose_name="Ціна",
                    ),
                ),
                (
                    "old_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="Стара ціна",
                    ),
                ),
                (
                    "stock",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="Залишок",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variants",
                        to="store.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Варіант товару",
                "verbose_name_plural": "Варіанти товару",
            },
        ),
        migrations.CreateModel(
            name="ProductAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        verbose_name="Назва атрибута",
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        max_length=255,
                        verbose_name="Значення",
                    ),
                ),
                (
                    "variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attributes",
                        to="store.productvariant",
                        verbose_name="Варіант товару",
                    ),
                ),
            ],
            options={
                "verbose_name": "Атрибут товару",
                "verbose_name_plural": "Атрибути товарів",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="products/%Y/%m/",
                        verbose_name="Зображення",
                    ),
                ),
                (
                    "alt",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name="Alt текст",
                    ),
                ),
                (
                    "is_main",
                    models.BooleanField(
                        default=False,
                        verbose_name="Головне фото",
                    ),
                ),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=0,
                        verbose_name="Порядок",
                    ),
                ),
                (
                    "variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="store.productvariant",
                        verbose_name="Варіант товару",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
                "verbose_name": "Фото товару",
                "verbose_name_plural": "Фото товарів",
            },
        ),
    ]
