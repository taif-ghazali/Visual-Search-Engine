from search import VisualSearch
from web_search import WebImageSearch
from image_downloader import download_matches


def run_visual_search(image_path, target_dir, top_k=4):

    search = WebImageSearch()
    visual_search = VisualSearch(target_dir)

    # Upload query image
    upload_result = search.upload_image(image_path)
    image_id = upload_result["image_id"]

    # Search for visual matches
    results = search.search_by_image(image_id)
    print("Search response keys:", results.keys())
    print(f"Visual matches returned: {len(results.get('visual_matches', []))}")
    
    if not results.get("visual_matches"):
        print("FULL RESPONSE:", results)
    
    visual_matches = search.get_visual_matches(results)

    # Download candidates
    candidate_paths = download_matches(
        visual_matches,
        target_dir,
        10
    )

    # Extract query embedding
    query_embedding = visual_search.extractor.extract(image_path)

    # Extract candidate embeddings
    candidate_embeddings = visual_search.get_embeddings(candidate_paths)
    if not candidate_paths:
        return []

    # Calculate cosine similarities
    similarities = visual_search.cosine_similarity(
        query_embedding,
        candidate_embeddings
    )

    # Rank candidates*
    ranked_results = visual_search.rank_results(
        candidate_paths,
        similarities
    )

    return ranked_results[:top_k]