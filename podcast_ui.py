# podcast_ui.py
import streamlit as st
import requests

st.set_page_config(page_title="AI Podcast Creator", page_icon="🎙️", layout="wide")

st.title("🎙️ AI-Powered Podcast Script Generator")
st.caption(" [A Multi-Agent System powered by ADK and A2A]")
st.markdown("Define your topic, hosts, and tone, and let our AI agents craft a unique script for you.")

with st.form("podcast_request_form"):
    st.subheader("Create Your Next Episode")
    
    topic = st.text_input("Podcast Topic", placeholder="e.g., The Future of Artificial Intelligence")
    col1, col2 = st.columns(2)
    with col1:
        host1_name = st.text_input("Host 1 Name", placeholder="Alex")
    with col2:
        host2_name = st.text_input("Host 2 Name", placeholder="Jordan")
    
    tone = st.selectbox(
        "Desired Tone",
        ("Conversational & Casual", "Formal & Informative", "Debate & Controversial", "Humorous & Witty"),
        index=0
    )

    submitted = st.form_submit_button("✨ Generate Script")

if submitted:
    if not all([topic, host1_name, host2_name]):
        st.warning("Please fill in all the fields.")
    else:
        payload = {
            "topic": topic,
            "host_names": [host1_name, host2_name],
            "tone": tone
        }

        with st.spinner("Your AI team is drafting the script..."):
            try:
                response = requests.post("http://localhost:8000/run", json=payload)
                response.raise_for_status()
                data = response.json()

                st.success("Your podcast script is ready!")
                st.subheader(f"Episode Title: {data.get('title', 'Untitled')}")
                st.text_area("Podcast Script", data.get('script', 'No script was generated.'), height=500)

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the agent network. Please ensure all agents are running. Details: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")