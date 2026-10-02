import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image


class FeatureExtractor:

    def __init__(self):
        self.model = ResNet50(
            weights="imagenet",
            include_top=False,
            pooling="avg" # Scope to Experiment
        )

    def extract(self, image_path):
        img = image.load_img(
            image_path,
            target_size=(224, 224)
        )

        img_array = image.img_to_array(img)
        img_array = tf.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        embedding = self.model(img_array, training=False)

        return embedding.numpy()[0]

### Feature Extractor to convert image -> embeddings.. (the last layer before softmax in ResNet)

if __name__ == "__main__":

    extractor = FeatureExtractor()

    image_path = "examples/query/query.jpg"
    embedding = extractor.extract(
        image_path
    )

    img = image.load_img(image_path)

    # plt.imshow(img)
    # plt.axis("off")
    # plt.show()
    print("Embedding shape:", embedding.shape)
    print("First 10 values:", embedding[:10])

# extractor = FeatureExtractor()
# embedding= extractor.extract("image.jpg")