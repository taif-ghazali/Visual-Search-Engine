import streamlit as st
import base64
from pathlib import Path
import textwrap

# def render_query(image):
#     ...


# def render_result(image_path, rank, score):
#     ...


def image_to_base64(image_path):
    image_path = Path(image_path)

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/jpeg;base64,{encoded}"


def render_query(image):
    image_data = image_to_base64(image)

    return f"""
    <div class="query-panel">
        <div class="section-title">Your image</div>
        <div class="query-image-container">
            <img src="{image_data}">
        </div>
    </div>
    """.strip()


def render_result(image_path, rank, score):
    image_data = image_to_base64(image_path)

    return f"""
    <div class="result-card">
    <img src="{image_data}">
    <div class="result-info">
    <span class="result-rank">#{rank}</span>
    <span class="result-score">Similarity: {score:.4f}</span>
    </div>
    </div>
    """


def render_results(results):
    cards = []
    for rank, (image_path, score) in enumerate(results, start=1):
        cards.append(
            render_result(image_path, rank, score)
        )

    return f"""
    <div class="results-panel">
    <div class="results-header">
    <span>Visual Matches</span>
    <span class="result-count">{len(results)} results</span>
    </div>
    <div class="results-grid">
    {"".join(cards)}
    </div>
    </div>
    """

def render_search_layout(query_image, results):
    query_html = render_query(query_image)
    results_html = render_results(results)

    html = f"""
    <div class="search-layout">
        {query_html}
        {results_html}
    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )