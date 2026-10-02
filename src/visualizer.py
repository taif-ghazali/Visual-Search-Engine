import matplotlib.pyplot as plt


def display_top_results(ranked_results, top_k=3):
    top_results = ranked_results[:top_k]

    fig, axes = plt.subplots(1, top_k, figsize=(12, 4))

    for ax, (image_path, score) in zip(axes, top_results):
        image = plt.imread(image_path)

        ax.imshow(image)
        ax.set_title(
            f"{image_path.split(chr(92))[-1]}\nScore: {score:.4f}"
        )
        ax.axis("off")

    plt.tight_layout()
    plt.show()