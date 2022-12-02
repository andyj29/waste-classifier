from django.db import models
from django.contrib import admin
from .constants import Label, Area


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_url(self):
        return self.image.url


class WasteCategory(models.Model):
    type = models.CharField(max_length=50, choices=Label.choices())
    desc = models.CharField(max_length=1024, blank=True, null=True)
    recyclable = models.BooleanField(default=False)


class Location(models.Model):
    address = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(WasteCategory)
    area = models.CharField(max_length=50, choices=Area.choices())


admin.site.register(Image)
admin.site.register(WasteCategory)
admin.site.register(Location)