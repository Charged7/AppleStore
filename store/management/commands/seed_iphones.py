from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from store.models import Product, ProductAttribute, ProductVariant


IPHONE_PRODUCTS = [
    {
        "name": "iPhone X",
        "year": 2017,
        "capacities": ["64GB", "256GB"],
        "colors": ["Silver", "Space Gray"],
        "ram": "3GB",
        "sim": "Nano-SIM",
    },
    {
        "name": "iPhone XR",
        "year": 2018,
        "capacities": ["64GB", "128GB", "256GB"],
        "colors": ["Black", "White", "Blue", "Yellow", "Coral", "PRODUCT(RED)"],
        "ram": "3GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone XS",
        "year": 2018,
        "capacities": ["64GB", "256GB", "512GB"],
        "colors": ["Silver", "Space Gray", "Gold"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone XS Max",
        "year": 2018,
        "capacities": ["64GB", "256GB", "512GB"],
        "colors": ["Silver", "Space Gray", "Gold"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 11",
        "year": 2019,
        "capacities": ["64GB", "128GB", "256GB"],
        "colors": ["Black", "Green", "Yellow", "Purple", "PRODUCT(RED)", "White"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 11 Pro",
        "year": 2019,
        "capacities": ["64GB", "256GB", "512GB"],
        "colors": ["Gold", "Space Gray", "Silver", "Midnight Green"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 11 Pro Max",
        "year": 2019,
        "capacities": ["64GB", "256GB", "512GB"],
        "colors": ["Gold", "Space Gray", "Silver", "Midnight Green"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone SE (2nd generation)",
        "year": 2020,
        "capacities": ["64GB", "128GB", "256GB"],
        "colors": ["Black", "White", "PRODUCT(RED)"],
        "ram": "3GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 12 mini",
        "year": 2020,
        "capacities": ["64GB", "128GB", "256GB"],
        "colors": ["Black", "White", "PRODUCT(RED)", "Green", "Blue", "Purple"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 12",
        "year": 2020,
        "capacities": ["64GB", "128GB", "256GB"],
        "colors": ["Black", "White", "PRODUCT(RED)", "Green", "Blue", "Purple"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 12 Pro",
        "year": 2020,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Silver", "Graphite", "Gold", "Pacific Blue"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 12 Pro Max",
        "year": 2020,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Silver", "Graphite", "Gold", "Pacific Blue"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 13 mini",
        "year": 2021,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["PRODUCT(RED)", "Starlight", "Midnight", "Blue", "Pink", "Green"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 13",
        "year": 2021,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["PRODUCT(RED)", "Starlight", "Midnight", "Blue", "Pink", "Green"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 13 Pro",
        "year": 2021,
        "capacities": ["128GB", "256GB", "512GB", "1TB"],
        "colors": ["Graphite", "Gold", "Silver", "Sierra Blue", "Alpine Green"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 13 Pro Max",
        "year": 2021,
        "capacities": ["128GB", "256GB", "512GB", "1TB"],
        "colors": ["Graphite", "Gold", "Silver", "Sierra Blue", "Alpine Green"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone SE (3rd generation)",
        "year": 2022,
        "capacities": ["64GB", "128GB", "256GB"],
        "colors": ["Midnight", "Starlight", "PRODUCT(RED)"],
        "ram": "4GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 14",
        "year": 2022,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Midnight", "Starlight", "PRODUCT(RED)", "Blue", "Purple", "Yellow"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 14 Plus",
        "year": 2022,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Midnight", "Starlight", "PRODUCT(RED)", "Blue", "Purple", "Yellow"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 14 Pro",
        "year": 2022,
        "capacities": ["128GB", "256GB", "512GB", "1TB"],
        "colors": ["Silver", "Gold", "Space Black", "Deep Purple"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 14 Pro Max",
        "year": 2022,
        "capacities": ["128GB", "256GB", "512GB", "1TB"],
        "colors": ["Silver", "Gold", "Space Black", "Deep Purple"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 15",
        "year": 2023,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Black", "Blue", "Green", "Yellow", "Pink"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 15 Plus",
        "year": 2023,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Black", "Blue", "Green", "Yellow", "Pink"],
        "ram": "6GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 15 Pro",
        "year": 2023,
        "capacities": ["128GB", "256GB", "512GB", "1TB"],
        "colors": ["Black Titanium", "White Titanium", "Blue Titanium", "Natural Titanium"],
        "ram": "8GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 15 Pro Max",
        "year": 2023,
        "capacities": ["256GB", "512GB", "1TB"],
        "colors": ["Black Titanium", "White Titanium", "Blue Titanium", "Natural Titanium"],
        "ram": "8GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 16",
        "year": 2024,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Black", "White", "Pink", "Teal", "Ultramarine"],
        "ram": "8GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 16 Plus",
        "year": 2024,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Black", "White", "Pink", "Teal", "Ultramarine"],
        "ram": "8GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 16 Pro",
        "year": 2024,
        "capacities": ["128GB", "256GB", "512GB", "1TB"],
        "colors": ["Black Titanium", "White Titanium", "Natural Titanium", "Desert Titanium"],
        "ram": "8GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 16 Pro Max",
        "year": 2024,
        "capacities": ["256GB", "512GB", "1TB"],
        "colors": ["Black Titanium", "White Titanium", "Natural Titanium", "Desert Titanium"],
        "ram": "8GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone 16e",
        "year": 2025,
        "capacities": ["128GB", "256GB", "512GB"],
        "colors": ["Black", "White"],
        "ram": "8GB",
        "sim": "Nano-SIM + eSIM",
    },
    {
        "name": "iPhone Air",
        "year": 2025,
        "capacities": ["256GB", "512GB", "1TB"],
        "colors": ["Space Black", "Cloud White", "Light Gold", "Sky Blue"],
        "ram": "12GB",
        "sim": "eSIM",
    },
    {
        "name": "iPhone 17",
        "year": 2025,
        "capacities": ["256GB", "512GB"],
        "colors": ["Black", "White", "Mist Blue", "Sage", "Lavender"],
        "ram": "8GB",
        "sim": "eSIM",
    },
    {
        "name": "iPhone 17 Pro",
        "year": 2025,
        "capacities": ["256GB", "512GB", "1TB"],
        "colors": ["Silver", "Cosmic Orange", "Deep Blue"],
        "ram": "12GB",
        "sim": "eSIM",
    },
    {
        "name": "iPhone 17 Pro Max",
        "year": 2025,
        "capacities": ["256GB", "512GB", "1TB", "2TB"],
        "colors": ["Silver", "Cosmic Orange", "Deep Blue"],
        "ram": "12GB",
        "sim": "eSIM",
    },
]


def build_variant_slug(product_name, storage, color):
    return slugify(
        " ".join(
            part
            for part in [product_name, storage, color]
            if part
        )
    )


class Command(BaseCommand):
    help = "Seed iPhone products, variants, and filter attributes."

    @transaction.atomic
    def handle(self, *args, **options):
        products_created = 0
        products_updated = 0
        variants_to_create = []

        for item in IPHONE_PRODUCTS:
            description = (
                f"Apple {item['name']}. "
                f"Year introduced: {item['year']}. "
                f"Capacities: {', '.join(item['capacities'])}. "
                f"Colors: {', '.join(item['colors'])}. "
                "Prices, stock, images, and concrete variants are managed in Django Admin."
            )
            _, was_created = Product.objects.update_or_create(
                slug=slugify(item["name"]),
                defaults={
                    "category": Product.CategoryChoices.IPHONE,
                    "name": item["name"],
                    "description": description,
                    "is_active": True,
                },
            )

            if was_created:
                products_created += 1
            else:
                products_updated += 1

        seeded_slugs = [slugify(item["name"]) for item in IPHONE_PRODUCTS]
        products = {
            product.slug: product
            for product in Product.objects.filter(slug__in=seeded_slugs)
        }

        for item in IPHONE_PRODUCTS:
            product = products[slugify(item["name"])]
            existing_variants = {
                (variant.color, variant.storage)
                for variant in ProductVariant.objects.filter(product=product)
            }

            for color in item["colors"]:
                for storage in item["capacities"]:
                    if (color, storage) not in existing_variants:
                        variants_to_create.append(
                            ProductVariant(
                                product=product,
                                color=color,
                                storage=storage,
                                slug=build_variant_slug(
                                    product.name,
                                    storage,
                                    color,
                                ),
                                price="0.00",
                                stock=0,
                            )
                        )

        ProductVariant.objects.bulk_create(variants_to_create)

        items_by_slug = {
            slugify(item["name"]): item
            for item in IPHONE_PRODUCTS
        }
        variants = list(
            ProductVariant.objects
            .filter(product__slug__in=seeded_slugs)
            .select_related("product")
        )
        existing_attributes = {}
        duplicate_attributes = set()

        for attribute in ProductAttribute.objects.filter(
            variant__in=variants,
            name__in=["ram", "sim"],
        ):
            key = (attribute.variant_id, attribute.name)
            if key in existing_attributes:
                duplicate_attributes.add(key)
                continue
            existing_attributes[key] = attribute

        attributes_to_create = []
        attributes_to_update = []

        for variant in variants:
            item = items_by_slug[variant.product.slug]
            for name in ["ram", "sim"]:
                key = (variant.id, name)
                value = item[name]
                attribute = existing_attributes.get(key)

                if attribute is None:
                    attributes_to_create.append(
                        ProductAttribute(
                            variant=variant,
                            name=name,
                            value=value,
                        )
                    )
                elif attribute.value != value:
                    attribute.value = value
                    attributes_to_update.append(attribute)

        ProductAttribute.objects.bulk_create(attributes_to_create)
        ProductAttribute.objects.bulk_update(attributes_to_update, ["value"])

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded iPhone catalog: "
                f"{products_created} products created, "
                f"{products_updated} products updated, "
                f"{len(variants_to_create)} variants created, "
                f"{len(variants)} variants total, "
                f"{len(attributes_to_create)} attributes created, "
                f"{len(attributes_to_update)} attributes updated, "
                f"{len(duplicate_attributes)} duplicate attributes ignored."
            )
        )
