import os
from keras.models import load_model
from .settings import BASE_DIR

print('loading model ...')
model = load_model(os.path.join(BASE_DIR,'config','saved_model.h5'))
