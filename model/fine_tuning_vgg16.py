from tensorflow.keras.applications import VGG16
from keras.layers import Flatten, Dense, Dropout, BatchNormalization, Input
from keras.models import Model
from tensorflow.keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint
from utils import Generator, Utils

train_data_flow = Generator.generate_train_data_flow()
test_data_flow = Generator.generate_test_data_flow()


labels = (train_data_flow.class_indices)
labels = dict((v,k) for k,v in labels.items())

VGG16_base_model = VGG16(weights="imagenet", include_top=False, input_tensor=Input(shape=(224,224,3)))

head = VGG16_base_model.output

head = Flatten(name="flatten")(head)

head = Dense(4096, activation='relu')(head)

head = Dropout(0.3)(head)
head = BatchNormalization()(head)

head = Dense(4096, activation='relu')(head)

head = Dropout(0.3)(head)
head = BatchNormalization()(head)

head = Dense(12, activation='softmax')(head)

model = Model(inputs=VGG16_base_model.input, outputs=head)

for layer in VGG16_base_model.layers:
    layer.trainable = False

opt = SGD(learning_rate=1e-4, momentum=0.9)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['acc'])

es = EarlyStopping(monitor='val_acc', mode='max', verbose=1, patience=20)

checkpoint = ModelCheckpoint('fine_tuning_model.h5', monitor='val_acc', mode='max', save_best_only=True, save_weights_only=False)

model.fit(train_data_flow, epochs=1, validation_data=test_data_flow, callbacks=[checkpoint,es])

test_x, test_y = test_data_flow.__getitem__(1)

preds = model.predict(test_x)

Utils.plot_results((16,16), 16, labels, preds, test_x, test_y)
