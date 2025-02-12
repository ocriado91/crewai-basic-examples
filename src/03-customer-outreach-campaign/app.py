"""Streamlit App for Customer Outreach Campaign."""

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from crew import CustomerOutreach
import os
import time


def initialize_session_state():
    """Initialize session state variables."""
    if "env_configured" not in st.session_state:
        st.session_state.env_configured = False
        st.session_state.model_name = os.getenv("MODEL_NAME", "Llama 3 8B")
        st.session_state.model_temperature = float(
            os.getenv("MODEL_TEMPERATURE", "0.0")
        )
        st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")
        st.session_state.serper_api_key = os.getenv("SERPER_API_KEY", "")
        st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")


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

        # Groq API Key
        serper_api_key = st.text_input(
            "Serper API key *",
            type="password",
            help="Enter your Serper API Key.",
            placeholder="INSERT YOUR SERPER API KEY",
        )

        # Gemini API Key
        gemini_api_key = st.text_input(
            "Gemini API key *",
            type="password",
            help="Enter your Gemini API Key",
            placeholder="INSERT YOUR GEMINI API KEY",
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

            if not serper_api_key or serper_api_key.isspace():
                st.error("❌ Serper API Key is required")
                return

            if not gemini_api_key or gemini_api_key.isspace():
                st.error("❌ Gemini API Key is required")
                return

            st.session_state.groq_api_key = groq_api_key
            st.session_state.serper_api_key = serper_api_key
            st.session_state.gemini_api_key = gemini_api_key
            st.session_state.model_name = model_name
            st.session_state.model_temperature = temperature
            os.environ["MODEL_NAME"] = model_name
            os.environ["MODEL_TEMPERATURE"] = str(temperature)
            os.environ["GROQ_API_KEY"] = groq_api_key
            os.environ["SERPER_API_KEY"] = serper_api_key
            os.environ["GEMINI_API_KEY"] = gemini_api_key
            st.session_state.env_configured = True
            st.success("✅ Settings applied successfully!")


def main():
    st.set_page_config(
        page_title="Customer Outreach Campaign",
        page_icon="🎯",
        layout="wide"
    )

    initialize_session_state()
    configure_environment()

    # Main content
    st.title("🎯 Customer Outreach Campaign AI Crew")
    st.markdown("""
    This AI-powered tool helps create personalized outreach campaigns for potential leads.

    ### Process:
    1. 🔍 **Sales Representative**: Analyzes and profiles the lead
    2. 📝 **Lead Sales Representative**: Creates personalized outreach messages
    3. ✨ **Final Output**: Delivers detailed lead analysis and tailored communication
    """)

    # Input section
    col1, col2 = st.columns(2)
    with col1:
        lead_name = st.text_input(
            "Lead Company Name:",
            placeholder="e.g., InnovaTech Solutions",
            help="Enter the name of the target company",
        )
    with col2:
        industry = st.text_input(
            "Industry:",
            placeholder="e.g., Software Development",
            help="Enter the industry sector of the company",
        )

    col3, col4 = st.columns(2)
    with col3:
        key_decision_maker = st.text_input(
            "Key Decision Maker:",
            placeholder="e.g., Sarah Johnson",
            help="Enter the name of the key decision maker",
        )
    with col4:
        position = st.text_input(
            "Position:",
            placeholder="e.g., Chief Technology Officer",
            help="Enter the position of the key decision maker",
        )

    milestone = st.text_area(
        "Recent Milestone:",
        placeholder="Enter any recent company achievements or developments...",
        help="Describe a recent milestone or achievement of the company",
        height=100,
    )

    # Generation section
    if st.button("🚀 Generate Campaign", type="primary", use_container_width=True):
        if not st.session_state.env_configured:
            st.warning(
                "⚠️ Please configure and apply environment settings in the sidebar first."
            )
            return

        if not all([lead_name, industry, key_decision_maker, position, milestone]):
            st.warning("⚠️ Please fill in all fields.")
            return

        try:
            with st.spinner("⏰ Waiting 1 minute to restart LLM API..."):
                time.sleep(60)

            # Initialize the crew
            crew = CustomerOutreach(verbose=True)

            # Show progress
            with st.spinner("🤖 Generating outreach campaign..."):
                # Generate the campaign
                result = crew.run({
                    "lead_name": lead_name,
                    "industry": industry,
                    "key_decision_maker": key_decision_maker,
                    "position": position,
                    "milestone": milestone
                })

            # Display results
            st.success("✨ Campaign generated successfully!")

            # Create tabs for viewing and downloading
            tab1, tab2 = st.tabs(["📄 View Campaign", "💾 Download"])

            with tab1:
                st.markdown(result)

            with tab2:
                st.download_button(
                    label="Download Campaign as Markdown",
                    data=result.raw,
                    file_name=f"outreach_campaign_{lead_name.lower().replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")


if __name__ == "__main__":
    main()