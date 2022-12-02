from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import LocationSerializer, WasteCategorySerializer
from .models import Image, Location, WasteCategory
from .services import classify_image, get_area_from_lat_long, is_in_gta


class ClassifyImage(APIView):
    def post(self, request, *args, **kwargs):
        try:
            file = self.request.data['file']
            if len(file) != 0:
                image = Image.objects.create(image=file)
            prediction = classify_image(image.get_url)
        except KeyError: 
            raise ParseError('This field is required: file')
        except UnboundLocalError:
            raise ParseError('Server can not read the image')

        category = WasteCategory.objects.filter(type=prediction['label']).first()
        category_serializer = WasteCategorySerializer(category)

        try:
            latitude = self.request.data['lat']
            longitude = self.request.data['long']
            location = get_area_from_lat_long(latitude, longitude)
        except (KeyError, ValueError):
            raise ParseError({
                'prediction': prediction,
                'category': category_serializer.data,
                'locations': 'Request has no or invalid longitude/latitude. Include it for our location service'
            })

        if is_in_gta(location):
            queryset = Location.objects.filter(area=location, category=category)
            loc_list = LocationSerializer(queryset, many=True)
        else:
            raise ParseError({
                'prediction': prediction,
                'category': category_serializer.data,
                'locations': 'Our location service only works inside the GTA'
            })

        data = {
            'prediction': prediction,
            'category': category_serializer.data,
            'locations': loc_list.data
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)


class LocationListCreate(generics.ListAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Location.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            category_list = self.request.data['category']
        except (KeyError, ValueError):
            raise ParseError('Request has no category field')

        queryset = WasteCategory.objects.filter(type__in=category_list)
        serializer = LocationSerializer(data=self.request.data)

        if serializer.is_valid():
            serializer.save(category=queryset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WasteCategoryListCreate(generics.ListCreateAPIView):
    serializer_class = WasteCategorySerializer
    
    def get_queryset(self):
        return WasteCategory.objects.all()


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializer

    def get_object(self):
        obj = get_object_or_404(Location, pk=self.kwargs['id'])
        return obj

    def put(self, request, *args, **kwargs):
        try:
            category_list = self.request.data['category']
        except (KeyError, ValueError):
            raise ParseError('Request has no category field')

        queryset = WasteCategory.objects.filter(type__in=category_list)
        obj = self.get_object()
        serializer = LocationSerializer(obj, data=request.data)

        if serializer.is_valid():
            serializer.save(category=queryset)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        update_category = True

        try:
            category_list = self.request.data['category']
            queryset = WasteCategory.objects.filter(type__in=category_list)
        except (KeyError, ValueError):
            update_category = False

        obj = self.get_object()
        serializer = LocationSerializer(obj, data=request.data, partial=True)

        if serializer.is_valid():
            if update_category:
                serializer.save(category=queryset)
            else:
                serializer.save()

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WasteCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WasteCategorySerializer
    
    def get_object(self):
        obj = get_object_or_404(WasteCategory, pk=self.kwargs['id'])
        return obj
