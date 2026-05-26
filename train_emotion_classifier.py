# Description: Train emotion classification model

import os

try:
    from tensorflow.keras.callbacks import CSVLogger, ModelCheckpoint, EarlyStopping
    from tensorflow.keras.callbacks import ReduceLROnPlateau
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
except ImportError:
    from keras.callbacks import CSVLogger, ModelCheckpoint, EarlyStopping
    from keras.callbacks import ReduceLROnPlateau
    from keras.preprocessing.image import ImageDataGenerator
from models.cnn import mini_XCEPTION

# parameters
batch_size = 32
num_epochs = 10000
input_shape = (64, 64, 1)
verbose = 1
num_classes = 7
patience = 50
base_path = 'models/'
train_dir = 'data/train'
validation_dir = 'data/validation'

# Keep class order aligned with model output expectations.
emotion_classes = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# data generator
data_generator = ImageDataGenerator(
    featurewise_center=False,
    featurewise_std_normalization=False,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=.1,
    horizontal_flip=True)

validation_data_generator = ImageDataGenerator(
    featurewise_center=False,
    featurewise_std_normalization=False)

# model parameters/compilation
model = mini_XCEPTION(input_shape, num_classes)
model.compile(optimizer='adam', loss='categorical_crossentropy',metrics=['accuracy'])
model.summary()

# callbacks
log_file_path = base_path + '_emotion_training.log'
csv_logger = CSVLogger(log_file_path, append=False)
early_stop = EarlyStopping(monitor='val_loss', patience=patience)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=int(patience/4), verbose=1)
trained_models_path = base_path + '_mini_XCEPTION'
model_names = trained_models_path + '.{epoch:02d}-{val_accuracy:.2f}.hdf5'
model_checkpoint = ModelCheckpoint(model_names, monitor='val_loss', verbose=1, save_best_only=True)
callbacks = [model_checkpoint, csv_logger, early_stop, reduce_lr]

train_generator = data_generator.flow_from_directory(
    train_dir,
    target_size=(64, 64),
    color_mode='grayscale',
    classes=emotion_classes,
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=True)

validation_generator = validation_data_generator.flow_from_directory(
    validation_dir,
    target_size=(64, 64),
    color_mode='grayscale',
    classes=emotion_classes,
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=False)

expected_classes = set(emotion_classes)
for split_name, split_dir in [("train", train_dir), ("validation", validation_dir)]:
    found_classes = {d.name for d in os.scandir(split_dir) if d.is_dir()}
    if found_classes != expected_classes:
        raise ValueError(
            f"Class folders mismatch in {split_name}. "
            f"Expected: {sorted(expected_classes)}, found: {sorted(found_classes)}"
        )

if train_generator.class_indices != validation_generator.class_indices:
    raise ValueError(
        f"Class index mismatch train vs validation: "
        f"{train_generator.class_indices} != {validation_generator.class_indices}"
    )

print("Class indices:", train_generator.class_indices)

model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=num_epochs,
    verbose=verbose,
    callbacks=callbacks,
    validation_data=validation_generator,
    validation_steps=len(validation_generator))
