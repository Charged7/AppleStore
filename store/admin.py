from django.contrib import admin
from .models import (
    Product, ProductImage,
    IPhoneSpec, IPadSpec, MacBookSpec, IMacSpec,
    AppleWatchSpec, AirPodsSpec, AppleKeyboardSpec, AppleMouseSpec,
)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(IPhoneSpec)
admin.site.register(IPadSpec)
admin.site.register(MacBookSpec)
admin.site.register(IMacSpec)
admin.site.register(AppleWatchSpec)
admin.site.register(AirPodsSpec)
admin.site.register(AppleKeyboardSpec)
admin.site.register(AppleMouseSpec)