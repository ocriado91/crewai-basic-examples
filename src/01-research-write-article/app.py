"""Streamlit App of Research and Write AI Crew."""

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from crew import ResearchAndWriterCrew
import os


def initialize_session_state():
    """Initialize session state variables."""
    if "env_configured" not in st.session_state:
        st.session_state.env_configured = False
        st.session_state.model_name = os.getenv("MODEL_NAME", "Gemma 2 9B")
        st.session_state.model_temperature = float(
            os.getenv("MODEL_TEMPERATURE", "0.0")
        )
        st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")


def configure_environment():
    """Configure environment section."""
    st.sidebar.header("🛠️ Environment Configuration")

    with st.sidebar.expander("Configuration", expanded=True):
        # Groq API Key
        groq_api_key = st.text_input(
            "Groq API key *",
            type="password",
            help="Enter your Groq API Key. Get one at console.groq.com",
            placeholder="INSERT YOUR GROQ API KEY",
        )

        # Model selection
        models = {
            "Gemma 2 9B": "groq/gemma2-9b-it",
            "Llama 3 8B": "groq/llama3-8b-8192",
            "Llama 3 70B": "groq/llama3-70b-8192",
        }

        selected_model = st.selectbox(
            "Select Model",
            options=list(models.keys()),
            index=list(models.values()).index(st.session_state.model_name)
            if st.session_state.model_name in models.values()
            else 0,
        )

        model_name = models[selected_model]

        # Temperature setting
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.model_temperature,
            step=0.1,
            help="Lower values make the output more focused and deterministic, higher values make it more creative",
        )

        # Apply settings button
        if st.button("Apply Settings", type="primary"):
            if not groq_api_key or groq_api_key.isspace():
                st.error("❌ Groq API Key is required")
                return

            st.session_state.groq_api_key = groq_api_key
            st.session_state.model_name = model_name
            st.session_state.model_temperature = temperature
            os.environ["MODEL_NAME"] = model_name
            os.environ["MODEL_TEMPERATURE"] = str(temperature)
            os.environ["GROQ_API_KEY"] = groq_api_key
            st.session_state.env_configured = True
            st.success("✅ Settings applied successfully!")


def main():
    st.set_page_config(page_title="Research & Writer AI Crew", page_icon="📝", layout="wide")

    initialize_session_state()
    configure_environment()

    # Main content
    st.title("📝 Research & Writer AI Crew")
    st.markdown("""
    This AI-powered tool helps you research and write comprehensive articles on any topic.

    ### Process:
    1. 🔍 **Research & Planning**: AI analyzes the topic and plans the content
    2. ✍️ **Writing**: Creates an engaging and informative article
    3. 📝 **Editing**: Professional editing and refinement
    """)

    # Input section
    topic = st.text_input(
        "Enter your research topic:",
        placeholder="e.g., The Future of Quantum Computing",
        help="Be specific about what you want to learn about",
    )
    verbose = st.checkbox(
        "Show detailed progress",
        value=False,
        help="Display the step-by-step progress of the article generation",
    )

    # Generation section
    if st.button("🚀 Generate Article", type="primary", use_container_width=True):
        if not st.session_state.env_configured:
            st.warning(
                "⚠️ Please configure and apply environment settings in the sidebar first."
            )
            return

        if not topic:
            st.warning("⚠️ Please enter a topic first.")
            return

        try:
            # Initialize the crew
            crew = ResearchAndWriterCrew(verbose=verbose)

            # Show progress
            with st.spinner("🤖 Researching and writing your article..."):
                # Generate the article
                result = crew.run(topic)

            # Display results
            st.success("✨ Article generated successfully!")

            # Create tabs for viewing and downloading
            tab1, tab2 = st.tabs(["📄 View Article", "💾 Download"])

            with tab1:
                st.markdown(result)

            with tab2:
                st.download_button(
                    label="Download Article as Markdown",
                    data=result.raw,
                    file_name=f"{topic.lower().replace(' ', '_')}_article.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            if verbose:
                st.exception(e)


if __name__ == "__main__":
    main()
