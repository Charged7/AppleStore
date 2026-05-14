from django.db import migrations, models
from django.utils.text import slugify


def build_variant_slug(variant):
    base_slug = slugify(
        " ".join(
            part
            for part in [
                variant.product.name if variant.product_id else "",
                variant.storage,
                variant.color,
            ]
            if part
        )
    )
    return base_slug or f"variant-{variant.pk}"


def populate_variant_slugs(apps, schema_editor):
    ProductVariant = apps.get_model("store", "ProductVariant")
    used_slugs = set()

    for variant in ProductVariant.objects.select_related("product").order_by("pk"):
        base_slug = build_variant_slug(variant)[:240]
        slug = base_slug
        counter = 2

        while slug in used_slugs:
            suffix = f"-{counter}"
            slug = f"{base_slug[:255 - len(suffix)]}{suffix}"
            counter += 1

        used_slugs.add(slug)
        variant.slug = slug
        variant.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_product_variants_attributes"),
    ]

    operations = [
        migrations.AddField(
            model_name="productvariant",
            name="slug",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.RunPython(
            populate_variant_slugs,
            migrations.RunPython.noop,
        ),
        migrations.RunSQL(
            sql=(
                "DROP INDEX IF EXISTS store_productvariant_slug_90bc56ed; "
                "DROP INDEX IF EXISTS store_productvariant_slug_90bc56ed_like;"
            ),
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AlterField(
            model_name="productvariant",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
