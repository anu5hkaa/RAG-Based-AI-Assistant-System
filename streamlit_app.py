import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Lecture Assistant", page_icon="🎓", layout="wide")
st.title("🎓 Lecture AI Assistant")

tab_upload, tab_ask = st.tabs(["📤 Upload Lecture", "💬 Ask a Question"])

# ---------------- Upload tab ----------------
with tab_upload:
    st.subheader("Upload a lecture video/audio")
    st.caption("The file is sent to the FastAPI backend, transcribed with Whisper, "
               "chunked, and embedded — same pipeline as create_chunks.py + read_chunks.py.")

    uploaded_file = st.file_uploader(
        "Choose a video or audio file",
        type=["mp4", "mov", "mkv", "avi", "mp3", "wav", "m4a"],
    )
    col1, col2 = st.columns(2)
    with col1:
        number = st.text_input("Lecture number", placeholder="e.g. 11")
    with col2:
        title = st.text_input("Lecture title", placeholder="e.g. Recursion in Java")

    if st.button("Upload & Process", type="primary"):
        if uploaded_file is None:
            st.warning("Please choose a file first.")
        elif not number or not title:
            st.warning("Please enter both the lecture number and title.")
        else:
            with st.spinner("Uploading and processing... this can take a while for long videos"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    data = {"number": number, "title": title}
                    resp = requests.post(f"{API_URL}/upload", files=files, data=data, timeout=3600)

                    if resp.status_code == 200:
                        result = resp.json()
                        st.success(
                            f"Processed '{result['filename']}' — "
                            f"{result['chunks_added']} chunks added to the index."
                        )
                    else:
                        st.error(f"Upload failed ({resp.status_code}): {resp.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not reach the backend at {API_URL}. Is FastAPI running? ({e})")

# ---------------- Ask tab ----------------
with tab_ask:
    st.subheader("Ask about your lectures")

    question = st.text_input("Your question", placeholder="e.g. What is a 2D array?")

    if st.button("Ask", type="primary"):
        if not question.strip():
            st.warning("Type a question first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=300)

                    if resp.status_code == 200:
                        answer = resp.json().get("answer", "")
                        st.markdown(answer if answer else "_No answer returned._")
                    else:
                        st.error(f"Request failed ({resp.status_code}): {resp.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Could not reach the backend at {API_URL}. Is FastAPI running? ({e})")