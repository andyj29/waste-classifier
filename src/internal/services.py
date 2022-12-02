import numpy as np
from geopy.geocoders import Nominatim
from src.config.__init__ import model
from src.config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from PIL import Image
from .constants import Label, Area
import io
import boto3

REGION_NAME = 'ca-central-1'
BUCKET = '2022hacks'

labels = Label.to_list()

areas = Area.to_list()

geolocator = Nominatim(user_agent="geoapiExercises")

class S3BUCKET:
    def __init__(self,
                 aws_access_key_id,
                 aws_secret_access_key,
                 region_name):

        self.s3 = boto3.resource('s3',
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key = aws_secret_access_key,
                               region_name=region_name)

    def get_img(self, bucket, key):
        return self.s3.Object(bucket, key)

s3 = S3BUCKET(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME)

def load_pic(path):
    s3_path = path.split('.com/')
    data = s3.get_img(BUCKET, s3_path[1])
    file_stream = io.BytesIO()
    data.download_fileobj(file_stream)
    with Image.open(file_stream) as i:
        resized_img = np.resize(i, (300, 300, 3))
        matrix = np.array(resized_img)/255

    matrix = np.reshape(matrix, (1, 300, 300, 3))

    return matrix


def classify_image(img_path):
    data = load_pic(img_path)
    prediction = model.predict(data)
    label = labels[np.argmax(prediction)]
    probability = prediction[0][np.argmax(prediction)]
    response = {
        'label': label,
        'prob': probability
    }

    return response


def get_area_from_lat_long(lat, long):
    location = geolocator.reverse(lat+","+long)
    address = location.raw['address']
    area = address['city']

    return area


def is_in_gta(area):
    return area in areas
