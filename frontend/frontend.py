import streamlit as st
import requests

API_URL = "http://localhost:8000/generate-haiku/"
GET_HAIKUS_URL = "http://localhost:8000/haikus/"

st.title("🖋️ Haiku Generator")
st.subheader("Describe your mood, season, or moment...")

elements = st.text_input("Enter key elements (e.g., sunrise, solitude, winter)")

if st.button("Generate Haiku"):
    if not elements.strip():
        st.error("Please enter some key elements.")
    else:
        with st.spinner("Composing your haiku..."):
            try:
                response = requests.post(API_URL, json={"elements": elements})
                if response.status_code == 200:
                    data = response.json()
                    st.success("Haiku successfully generated and saved!")
                    st.markdown("### 🌸 Your Haiku")
                    st.code(data["haiku"], language="text")
                    st.markdown(f"**Saved as:** `{data['filename']}`")
                else:
                    st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

st.markdown("---")
st.header("📜 Past Haikus")

try:
    res = requests.get(GET_HAIKUS_URL)
    if res.status_code == 200:
        haikus = res.json()
        if haikus:
            # Create a dict: filename -> haiku for easy lookup
            haiku_dict = {h['filename']: h['haiku'] for h in haikus}
            filenames = list(haiku_dict.keys())

            selected_file = st.selectbox("Select a haiku filename to view:", filenames)

            if selected_file:
                st.markdown(f"### Haiku: `{selected_file}`")
                st.code(haiku_dict[selected_file], language="text")
        else:
            st.info("No haikus stored yet. Generate one!")
    else:
        st.error("Failed to fetch past haikus.")
except Exception as e:
    st.error(f"Connection Error while fetching haikus: {e}")
