from rest_framework import serializers
from .models import Image, Location, WasteCategory


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('__all__')


class WasteCategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(WasteCategorySerializer, self).__init__(*args, **kwargs)

        if remove_fields:
            for field in remove_fields:
                self.fields.pop(field)

    class Meta:
        model = WasteCategory
        fields = ('__all__')


class LocationSerializer(serializers.ModelSerializer):
    category = WasteCategorySerializer(many=True, read_only=True, remove_fields=['id', 'desc', 'recyclable'])

    class Meta:
        model = Location
        fields = ('__all__')
