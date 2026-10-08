import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from web_image_search import WebImageSearch


def render_web_search():

    st.subheader("Search the Web")
    search= WebImageSearch()

    with st.form("web_search_form"):
        query = st.text_input(
            "Search for an image",
            placeholder= "Ferrari 488, aircraft, horror movie..."
        )

        submitted= st.form_submit_button("Search")

    if submitted and query:
        with st.spinner("Searching the web..."):
            images= search.search(query, limit= 6)
        st.session_state.web_images= images

    images = st.session_state.get("web_images", [])

    if images:

        st.write("Choose an image")

        cols = st.columns(3)

        for i, image in enumerate(images):

            with cols[i % 3]:
                st.image(
                    image["thumbnail"],
                    use_container_width=True
                )

                st.caption(
                    image["title"] or "Untitled"
                )

                if st.button("Select", key=f"select_web_image_{i}"):
                    st.session_state.selected_web_image = image
                    st.rerun()