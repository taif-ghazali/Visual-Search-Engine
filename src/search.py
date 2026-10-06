import os # Helps us 'walk through' the candidates folder
import numpy as np

from feature_extractor import FeatureExtractor
from visualizer import display_top_results

# Extract Query Embedding
# Extract Candidate Embedding
# Compare Query against each Candidate
# Rank and Display

class VisualSearch:
    def __init__(self, candidate_dir):
        self.candidate_dir = candidate_dir
        self.extractor = FeatureExtractor()

    def get_candidate_images(self): ## Get the candidate images
        images = []

        for filename in os.listdir(self.candidate_dir):
            path = os.path.join(self.candidate_dir, filename)

            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                images.append(path)

        return images

    def get_embeddings(self, image_paths): ## Get the embeddings
        embeddings = []

        for image_path in image_paths:
            embedding = self.extractor.extract(image_path)
            embeddings.append(np.asarray(embedding).reshape(-1))

        if not embeddings:
            return np.empty((0,0))

        return np.vstack(embeddings)

    def cosine_similarity(self, query_embedding, candidate_embeddings):
        query_norm = np.linalg.norm(query_embedding)
        candidate_norms = np.linalg.norm(candidate_embeddings, axis=1)

        similarities = np.dot(candidate_embeddings, query_embedding) / (
            candidate_norms * query_norm
        )

        return similarities

    def rank_results(self, image_paths, similarities):
        results = list(zip(image_paths, similarities))

        results.sort(key=lambda x: x[1], reverse=True)

        return results

## Metric we're using for similarity = Cosine Similarity

if __name__ == "__main__":
    search = VisualSearch("examples/candidates") # Can be /c or \c either way works
    query_path = "examples/query/query.jpg"

    images= search.get_candidate_images()

    query_embedding = search.extractor.extract(query_path)
    embeddings = search.get_embeddings(images)

    similarities= search.cosine_similarity(
        query_embedding, 
        embeddings
    )

    ranked_results = search.rank_results(
        images, similarities
    )


    print("Found", len(images), "candidate images: ")

    print("Embeddings shape:", embeddings.shape)
    print("Similarities shape:", similarities.shape)

    for rank, (image, score) in enumerate(ranked_results, start=1):
        print(f"{rank}, {image} - {score: .4f}")

    display_top_results(ranked_results, top_k=3)