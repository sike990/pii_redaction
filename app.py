import streamlit as st
import spacy
from src.detector import PIIDetector
from src.redactor import Redactor
from src.classifier import Classifier

# Set page config
st.set_page_config(
    page_title="PII Redaction Tool",
    page_icon="🔒",
    layout="wide"
)

# Title and Description
st.title("🔒 PII Data Redaction & Classification Tool")
st.markdown("""
This tool scans text for **Personally Identifiable Information (PII)** using NLP and Regex.
It detects sensitive data like **Names, Emails, Phone Numbers, PAN Cards, and Aadhaar Numbers**, 
classifies the document sensitivity, and provides a redacted version.
""")

# Sidebar
st.sidebar.header("Settings")
model_name = st.sidebar.selectbox("Spacy Model", ["en_core_web_sm"])

# Initialize components
@st.cache_resource
def load_components():
    return PIIDetector(model_name=model_name), Redactor(), Classifier()

try:
    detector, redactor, classifier = load_components()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.info("Please make sure you have installed the model: python -m spacy download en_core_web_sm")
    st.stop()

# Input Area
st.subheader("1. Input Text")
input_text = st.text_area("Paste text here to scan:", height=200, placeholder="Enter text containing PII...")

if st.button("Analyze & Redact"):
    if not input_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        # Detection
        with st.spinner("Scanning for PII..."):
            detected_items = detector.detect(input_text)
            sensitivity = classifier.classify(detected_items)
            redacted_text = redactor.redact(input_text, detected_items)

        # Application Layout - Columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("2. Analysis Results")
            st.info(f"**Sensitivity Level:** {sensitivity}")
            
            if detected_items:
                st.write(f"**Found {len(detected_items)} entities:**")
                # Create a simple dataframe-like display
                items_display = [{"Type": item['type'], "Value": item['value'], "Method": item['method']} for item in detected_items]
                st.table(items_display)
            else:
                st.success("No PII detected.")

        with col2:
            st.subheader("3. Redacted Output")
            st.text_area("Redacted Text:", value=redacted_text, height=300)
            
            # Download Button
            st.download_button(
                label="Download Redacted Text",
                data=redacted_text,
                file_name="redacted_output.txt",
                mime="text/plain"
            )

# Footer
st.markdown("---")
st.markdown("Built with Python, Spacy, and Streamlit.")
