import os
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

train_dir = 'content/train'
output_model_path = 'model.keras'
output_json_path = 'class_indices.json' 
TF_ENABLE_ONEDNN_OPTS = 0
batch_size = 32

train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

sorted_class_indices = sorted(train_generator.class_indices.items(), key=lambda x: x[0])

class_indices_dict = {class_name: index for index, (class_name, _) in enumerate(sorted_class_indices)}

with open(output_json_path, 'w') as json_file:
    json.dump(class_indices_dict, json_file)

base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

model = Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(train_generator.class_indices), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

epochs = 50
model.fit(train_generator, epochs=epochs, validation_data=validation_generator)

model.save(output_model_path)