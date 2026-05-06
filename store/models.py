from django.db import models
from django.utils.text import slugify


# ───────────────────────────────────────────
# БАЗОВИЙ ПРОДУКТ
# ───────────────────────────────────────────

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
    name = models.CharField(max_length=255, verbose_name="Назва")
    slug = models.SlugField(unique=True, max_length=255)
    sku = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True, verbose_name="Стара ціна"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Залишок")
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    description = models.TextField(blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="images", verbose_name="Товар"
    )
    image = models.ImageField(upload_to="products/%Y/%m/", verbose_name="Зображення")
    alt = models.CharField(max_length=255, blank=True, verbose_name="Alt текст")
    is_main = models.BooleanField(default=False, verbose_name="Головне")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order"]
        verbose_name = "Фото товару"


# ───────────────────────────────────────────
# CHOICES (спільні)
# ───────────────────────────────────────────

class StorageChoices(models.TextChoices):
    GB_64 = "64GB", "64 GB"
    GB_128 = "128GB", "128 GB"
    GB_256 = "256GB", "256 GB"
    GB_512 = "512GB", "512 GB"
    TB_1 = "1TB", "1 TB"
    TB_2 = "2TB", "2 TB"
    TB_4 = "4TB", "4 TB"


class RamChoices(models.TextChoices):
    GB_8 = "8GB", "8 GB"
    GB_16 = "16GB", "16 GB"
    GB_24 = "24GB", "24 GB"
    GB_32 = "32GB", "32 GB"
    GB_48 = "48GB", "48 GB"
    GB_64 = "64GB", "64 GB"
    GB_128 = "128GB", "128 GB"


# ───────────────────────────────────────────
# iPHONE
# ───────────────────────────────────────────

class IPhoneSpec(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE,
        related_name="iphone_spec"
    )
    model_name = models.CharField(max_length=100, verbose_name="Модель")  # iPhone 16 Pro Max
    color = models.CharField(max_length=100, verbose_name="Колір")
    storage = models.CharField(
        max_length=10, choices=StorageChoices,
        verbose_name="Накопичувач"
    )
    chip = models.CharField(max_length=50, verbose_name="Чіп")  # A18 Pro
    display_size = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name='Діагональ екрана (дюйм)'
    )
    display_type = models.CharField(max_length=100, verbose_name="Тип дисплею")  # Super Retina XDR OLED
    ram = models.CharField(max_length=10, choices=RamChoices, verbose_name="RAM")
    main_camera = models.CharField(max_length=100, verbose_name="Основна камера")
    front_camera = models.CharField(max_length=100, verbose_name="Фронтальна камера")
    battery_mah = models.PositiveIntegerField(verbose_name="Батарея (мАг)")
    has_5g = models.BooleanField(default=True, verbose_name="5G")
    has_esim = models.BooleanField(default=True, verbose_name="eSIM")

    class Meta:
        verbose_name = "Специфікація iPhone"


# ───────────────────────────────────────────
# iPAD
# ───────────────────────────────────────────

class IPadSpec(models.Model):
    class LineChoices(models.TextChoices):
        IPAD = "iPad", "iPad"
        IPAD_MINI = "iPad mini", "iPad mini"
        IPAD_AIR = "iPad Air", "iPad Air"
        IPAD_PRO = "iPad Pro", "iPad Pro"

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="ipad_spec"
    )
    line = models.CharField(
        max_length=20, choices=LineChoices, verbose_name="Лінійка"
    )
    model_name = models.CharField(max_length=100, verbose_name="Модель")
    color = models.CharField(max_length=100, verbose_name="Колір")
    storage = models.CharField(max_length=10, choices=StorageChoices, verbose_name="Накопичувач")
    chip = models.CharField(max_length=50, verbose_name="Чіп")
    display_size = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Діагональ (дюйм)')
    display_type = models.CharField(max_length=100, verbose_name="Тип дисплею")
    ram = models.CharField(max_length=10, choices=RamChoices, verbose_name="RAM")
    has_cellular = models.BooleanField(default=False, verbose_name="Cellular")
    has_pencil = models.BooleanField(default=True, verbose_name="Підтримка Apple Pencil")
    pencil_gen = models.CharField(max_length=50, blank=True, verbose_name="Покоління Pencil")
    battery_hours = models.PositiveSmallIntegerField(verbose_name="Батарея (год)")

    class Meta:
        verbose_name = "Специфікація iPad"


# ───────────────────────────────────────────
# MacBook
# ───────────────────────────────────────────

class MacBookSpec(models.Model):
    class LineChoices(models.TextChoices):
        AIR = "MacBook Air", "MacBook Air"
        PRO = "MacBook Pro", "MacBook Pro"

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="macbook_spec"
    )
    line = models.CharField(max_length=20, choices=LineChoices, verbose_name="Лінійка")
    color = models.CharField(max_length=100, verbose_name="Колір")
    chip = models.CharField(max_length=50, verbose_name="Чіп")  # M4 Pro
    cpu_cores = models.PositiveSmallIntegerField(verbose_name="CPU ядра")
    gpu_cores = models.PositiveSmallIntegerField(verbose_name="GPU ядра")
    ram = models.CharField(max_length=10, choices=RamChoices, verbose_name="RAM")
    storage = models.CharField(max_length=10, choices=StorageChoices, verbose_name="Накопичувач")
    display_size = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Діагональ (дюйм)')
    display_type = models.CharField(max_length=100, verbose_name="Тип дисплею")  # Liquid Retina XDR
    battery_hours = models.PositiveSmallIntegerField(verbose_name="Батарея (год)")
    has_touch_id = models.BooleanField(default=True, verbose_name="Touch ID")

    class Meta:
        verbose_name = "Специфікація MacBook"


# ───────────────────────────────────────────
# iMac
# ───────────────────────────────────────────

class IMacSpec(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="imac_spec"
    )
    color = models.CharField(max_length=100, verbose_name="Колір")
    chip = models.CharField(max_length=50, verbose_name="Чіп")
    cpu_cores = models.PositiveSmallIntegerField(verbose_name="CPU ядра")
    gpu_cores = models.PositiveSmallIntegerField(verbose_name="GPU ядра")
    ram = models.CharField(max_length=10, choices=RamChoices, verbose_name="RAM")
    storage = models.CharField(max_length=10, choices=StorageChoices, verbose_name="Накопичувач")
    display_size = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Діагональ (дюйм)')
    resolution = models.CharField(max_length=50, verbose_name="Роздільна здатність")  # 4480 x 2520
    camera_mp = models.PositiveSmallIntegerField(verbose_name="Камера (Мп)")

    class Meta:
        verbose_name = "Специфікація iMac"


# ───────────────────────────────────────────
# Apple Watch
# ───────────────────────────────────────────

class AppleWatchSpec(models.Model):
    class LineChoices(models.TextChoices):
        SERIES = "Series", "Apple Watch Series"
        SE = "SE", "Apple Watch SE"
        ULTRA = "Ultra", "Apple Watch Ultra"

    class CaseChoices(models.TextChoices):
        ALUMINUM = "Aluminum", "Алюміній"
        STEEL = "Steel", "Нержавіюча сталь"
        TITANIUM = "Titanium", "Титан"

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="watch_spec"
    )
    line = models.CharField(max_length=20, choices=LineChoices, verbose_name="Лінійка")
    generation = models.CharField(max_length=50, verbose_name="Покоління")  # Series 10
    color = models.CharField(max_length=100, verbose_name="Колір корпусу")
    band_color = models.CharField(max_length=100, verbose_name="Колір ремінця")
    band_material = models.CharField(max_length=100, verbose_name="Матеріал ремінця")
    case_size_mm = models.PositiveSmallIntegerField(verbose_name="Розмір корпусу (мм)")
    case_material = models.CharField(max_length=20, choices=CaseChoices, verbose_name="Матеріал корпусу")
    has_cellular = models.BooleanField(default=False, verbose_name="Cellular")
    chip = models.CharField(max_length=50, verbose_name="Чіп")
    battery_hours = models.PositiveSmallIntegerField(verbose_name="Батарея (год)")
    water_resist = models.CharField(max_length=50, verbose_name="Захист від води")  # WR50 / 100m

    class Meta:
        verbose_name = "Специфікація Apple Watch"


# ───────────────────────────────────────────
# AirPods
# ───────────────────────────────────────────

class AirPodsSpec(models.Model):
    class LineChoices(models.TextChoices):
        AIRPODS = "AirPods", "AirPods"
        AIRPODS_PRO = "AirPods Pro", "AirPods Pro"
        AIRPODS_MAX = "AirPods Max", "AirPods Max"

    class ConnectionChoices(models.TextChoices):
        LIGHTNING = "Lightning", "Lightning"
        USB_C = "USB-C", "USB-C"
        MAGSAFE = "MagSafe", "MagSafe"

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="airpods_spec"
    )
    line = models.CharField(max_length=20, choices=LineChoices, verbose_name="Лінійка")
    generation = models.CharField(max_length=50, verbose_name="Покоління")
    color = models.CharField(max_length=100, verbose_name="Колір")
    has_anc = models.BooleanField(default=False, verbose_name="Активне шумоподавлення (ANC)")
    has_transparency = models.BooleanField(default=False, verbose_name="Режим прозорості")
    chip = models.CharField(max_length=50, verbose_name="Чіп")
    battery_earbuds = models.PositiveSmallIntegerField(verbose_name="Батарея навушників (год)")
    battery_case = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Батарея кейсу (год)"
    )
    case_connector = models.CharField(
        max_length=20, choices=ConnectionChoices,
        verbose_name="Роз'єм кейсу"
    )
    is_wireless_charge = models.BooleanField(default=True, verbose_name="Бездротова зарядка")

    class Meta:
        verbose_name = "Специфікація AirPods"


# ───────────────────────────────────────────
# Клавіатура Apple
# ───────────────────────────────────────────

class AppleKeyboardSpec(models.Model):
    class LayoutChoices(models.TextChoices):
        UA = "UA", "Українська"
        EN = "EN", "Англійська"
        RU = "RU", "Російська"

    class ConnectionChoices(models.TextChoices):
        WIRELESS = "Wireless", "Бездротова (Bluetooth)"
        USB_C = "USB-C", "USB-C"

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="keyboard_spec"
    )
    model_name = models.CharField(max_length=100, verbose_name="Модель")  # Magic Keyboard
    color = models.CharField(max_length=100, verbose_name="Колір")
    layout = models.CharField(max_length=5, choices=LayoutChoices, verbose_name="Розкладка")
    connection = models.CharField(
        max_length=20, choices=ConnectionChoices, verbose_name="Підключення"
    )
    has_touch_id = models.BooleanField(default=False, verbose_name="Touch ID")
    has_numpad = models.BooleanField(default=False, verbose_name="Цифровий блок")
    battery_months = models.PositiveSmallIntegerField(verbose_name="Батарея (міс)")

    class Meta:
        verbose_name = "Специфікація клавіатури Apple"


# ───────────────────────────────────────────
# Мишка Apple
# ───────────────────────────────────────────

class AppleMouseSpec(models.Model):
    class ConnectionChoices(models.TextChoices):
        WIRELESS = "Wireless", "Бездротова (Bluetooth)"
        USB_C = "USB-C", "USB-C"

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="mouse_spec"
    )
    model_name = models.CharField(max_length=100, verbose_name="Модель")  # Magic Mouse
    color = models.CharField(max_length=100, verbose_name="Колір")
    connection = models.CharField(
        max_length=20, choices=ConnectionChoices, verbose_name="Підключення"
    )
    has_multi_touch = models.BooleanField(default=True, verbose_name="Multi-Touch поверхня")
    battery_months = models.PositiveSmallIntegerField(verbose_name="Батарея (міс)")
    charge_port = models.CharField(max_length=20, verbose_name="Роз'єм зарядки")  # USB-C / Lightning

    class Meta:
        verbose_name = "Специфікація мишки Apple"
