"""Streamlit App of Customer Support."""

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from crew import CustomerSupport
import os


def initialize_session_state():
    """Initialize session state variables."""
    if "env_configured" not in st.session_state:
        st.session_state.env_configured = False
        st.session_state.model_name = os.getenv("MODEL_NAME", "Llama 3 8B")
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
    st.set_page_config(page_title="Customer Support", page_icon="🎯", layout="wide")

    initialize_session_state()
    configure_environment()

    # Main content
    st.title("🎯 Customer Support AI Crew")
    st.markdown("""
    This AI-powered tool helps provide comprehensive customer support responses.

    ### Process:
    1. 💬 **Support Representative**: Creates detailed response to customer inquiry
    2. 🔍 **Quality Assurance**: Reviews and refines the response
    3. ✨ **Final Response**: Delivers polished, accurate support message
    """)

    # Input section
    col1, col2 = st.columns(2)
    with col1:
        customer = st.text_input(
            "Customer Company Name:",
            placeholder="e.g., TechCorp Inc.",
            help="Enter the name of the customer's company",
        )
    with col2:
        person = st.text_input(
            "Contact Person:",
            placeholder="e.g., John Smith",
            help="Enter the name of the person making the inquiry",
        )

    inquiry = st.text_area(
        "Customer Inquiry:",
        placeholder="Enter the customer's question or issue here...",
        help="Be specific about the customer's needs",
        height=150,
    )

    # Generation section
    if st.button("🚀 Generate Response", type="primary", use_container_width=True):
        if not st.session_state.env_configured:
            st.warning(
                "⚠️ Please configure and apply environment settings in the sidebar first."
            )
            return

        if not all([customer, person, inquiry]):
            st.warning("⚠️ Please fill in all fields.")
            return

        try:
            # Initialize the crew
            crew = CustomerSupport()

            # Show progress
            with st.spinner("🤖 Processing customer inquiry..."):
                # Generate the response
                result = crew.run({
                    "customer": customer,
                    "person": person,
                    "inquiry": inquiry
                })

            # Display results
            st.success("✨ Response generated successfully!")

            # Create tabs for viewing and downloading
            tab1, tab2 = st.tabs(["📄 View Response", "💾 Download"])

            with tab1:
                st.markdown(result)

            with tab2:
                st.download_button(
                    label="Download Response as Markdown",
                    data=result,
                    file_name=f"support_response_{customer.lower().replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
