from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from pipeline import run_visual_search


query_path = Path("examples/query/query0.jpg")
target_dir = Path("runtime/test_pipeline/candidates")

results = run_visual_search(
    query_path,
    target_dir,
    top_k=4
)

print("\n===== TOP RESULTS =====")

for rank, (image_path, score) in enumerate(results, start=1):
    print(f"{rank}. {image_path} | similarity: {score:.4f}")