import streamlit as st
from pathlib import Path
import hashlib
import shutil
import uuid
import sys

st.set_page_config(
    page_title="Visual Search WebApp",
    layout="wide"
)

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from pipeline import run_visual_search
from ui import render_search_layout
from web_search_ui import render_web_search

def load_css():
    css_path = Path(__file__).parent / "style.css"

    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()
st.title("Visual Search")
if "web_search_mode" not in st.session_state:
    st.session_state.web_search_mode= False

if st.button("Search Web", use_container_width=True):
    st.session_state.web_search_mode = True

if st.session_state.web_search_mode:
    render_web_search()
    st.stop()

# Create a temporary folder for this Streamlit session
if "session_dir" not in st.session_state:
    session_id = str(uuid.uuid4())
    session_dir = Path("runtime") / "sessions" / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    st.session_state.session_dir = session_dir

uploaded_file = st.file_uploader(
    "Drop an image here or browse",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    file_hash= hashlib.md5(
        uploaded_file.getvalue()
    ).hexdigest()

    query_path= st.session_state.session_dir / "query.jpg"
    candidates_dir= st.session_state.session_dir / "candidates" 

    is_new_query = (
        "query_hash" not in st.session_state
        or st.session_state.query_hash != file_hash
    )

    if is_new_query:
        sessions_dir = st.session_state.session_dir.parent

        #Delete old sessions
        for session in sessions_dir.iterdir():
            if session.is_dir() and session != st.session_state.session_dir:
                shutil.rmtree(session)

        #Clear current sessions old candidates
        if candidates_dir.exists():
            shutil.rmtree(candidates_dir)

        st.session_state.query_hash = file_hash

        with open(query_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        

    with st.spinner("Searching for visually similar images..."):
        results = run_visual_search(
            query_path,
            candidates_dir,
            top_k=4
        )

    st.write("Search complete.")
    render_search_layout(query_path, results)