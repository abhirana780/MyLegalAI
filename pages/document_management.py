import streamlit as st
import pandas as pd
from datetime import datetime
import os
import io
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from cryptography.fernet import Fernet
from pathlib import Path

# Initialize encryption key (in production, this should be securely stored)
KEY = Fernet.generate_key()
fernet = Fernet(KEY)

# Ensure secure storage directory exists
SECURE_STORAGE = Path("secure_storage")
SECURE_STORAGE.mkdir(exist_ok=True)

def main():
    st.set_page_config(
        page_title="Document Management - Indian Legal Assistant",
        page_icon="⚖️",
        layout="wide"
    )

    st.title("Document Management System")
    st.markdown("### Secure storage and version control for legal documents")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Back to Home"):
        st.switch_page("app.py")

    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Document Upload", "Document Library", "Version Control"])

def upload_documents(tab):
    with tab:
        st.markdown("## Upload or Scan Legal Documents")
        st.markdown("Securely upload, scan and store your legal documents with automatic OCR processing")
        
        # Document type selection
        doc_type = st.selectbox(
            "Document Type",
            ["Evidence", "Affidavit", "Petition", "Legal Draft", "Court Order", "Other"]
        )
        
        # Case association
        case_number = st.text_input("Associated Case Number (optional)")
        
        # Document description
        doc_description = st.text_area("Document Description")
        
        # Document source selection
        doc_source = st.radio(
            "Document Source",
            ["Upload File", "Scan Document"],
            horizontal=True
        )
        
        # Initialize uploaded_file variable
        uploaded_file = None
        
        if doc_source == "Upload File":
            # File uploader
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=["pdf", "doc", "docx", "jpg", "png"],
                help="Supported formats: PDF, DOC, DOCX, JPG, PNG"
            )
        else:
            # Scan document option
            if st.button("Open Scanner", use_container_width=True):
                uploaded_file = scan_document()
                if uploaded_file:
                    st.success("Document scanned successfully!")
        
        if uploaded_file is not None:
            if st.button("Process Document", use_container_width=True):
                with st.spinner("Processing document..."):
                    # Create unique filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{doc_type}_{timestamp}_{uploaded_file.name}"
                    
                    # Process the uploaded file
                    if uploaded_file.type.startswith('image/'):
                        process_image(uploaded_file, filename)
                    elif uploaded_file.type == 'application/pdf':
                        process_pdf(uploaded_file, filename)
                    
                    # Save metadata
                    save_document_metadata(filename, doc_type, case_number, doc_description)
                    
                    st.success("Document uploaded and processed successfully!")
                    
                    # Display document preview
                    st.markdown("### Document Preview")
                    if uploaded_file.type.startswith('image/'):
                        st.image(uploaded_file)
                    elif uploaded_file.type == 'application/pdf':
                        st.markdown("PDF preview will be displayed here")

def scan_document():
    """
    Capture document from scanner or camera
    Returns file-like object containing scanned image
    """
    try:
        # First try to use actual scanner if available
        try:
            import pyinsane2
            pyinsane2.init()
            devices = pyinsane2.get_devices()
            if devices:
                device = devices[0]
                scan_session = device.scan(multiple=False)
                try:
                    scan_session.scan.read()
                    img_bytes = io.BytesIO()
                    scan_session.scan.save(img_bytes, format="PNG")
                    img_bytes.seek(0)
                    return img_bytes
                finally:
                    scan_session.cancel()
            
        except ImportError:
            st.warning("Scanner hardware integration not available on this system.")
            st.info("Please use the file upload option below to add your documents")
        except Exception as scan_error:
            st.error(f"Scanner error: {str(scan_error)}")
            st.info("Please use the file upload option below instead")
        
        # Fallback to webcam capture if scanner not available
        try:
            import cv2
            from streamlit_webrtc import webrtc_streamer
            
            st.info("Using device camera as fallback")
            webrtc_ctx = webrtc_streamer(
                key="webcam",
                video_frame_callback=lambda frame: frame,
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            )
            
            if webrtc_ctx.video_frame:
                img_bytes = io.BytesIO()
                webrtc_ctx.video_frame.save(img_bytes, format="PNG")
                img_bytes.seek(0)
                return img_bytes
            
        except ImportError:
            st.warning("Webcam access not available")
            
        # Final fallback to file upload
        return st.file_uploader(
            "Choose a file (fallback when scanner unavailable)",
            type=["jpg", "png", "jpeg"],
            key="scanner_fallback"
        )
    except Exception as e:
        st.error(f"Document capture failed: {str(e)}")
        return None


def process_image(uploaded_file, filename):
    # Convert uploaded file to image
    image = Image.open(uploaded_file)
    
    # Perform OCR
    text = pytesseract.image_to_string(image)
    
    # Encrypt the extracted text and image data
    encrypted_text = fernet.encrypt(text.encode())
    
    # Save the encrypted text and original file
    file_path = SECURE_STORAGE / f"{filename}"
    text_path = SECURE_STORAGE / f"{filename}.txt"
    
    # Save encrypted text
    with open(text_path, "wb") as f:
        f.write(encrypted_text)
    
    # Save encrypted original file
    with open(file_path, "wb") as f:
        encrypted_file = fernet.encrypt(uploaded_file.getvalue())
        f.write(encrypted_file)

def process_pdf(uploaded_file, filename):
    # Read PDF content
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text_content = ""
    
    # Extract text from each page
    for page in pdf_document:
        text_content += page.get_text()
    
    # Encrypt the extracted text and PDF data
    encrypted_text = fernet.encrypt(text_content.encode())
    
    # Save the encrypted text and original file
    file_path = SECURE_STORAGE / f"{filename}"
    text_path = SECURE_STORAGE / f"{filename}.txt"
    
    # Save encrypted text
    with open(text_path, "wb") as f:
        f.write(encrypted_text)
    
    # Save encrypted original file
    with open(file_path, "wb") as f:
        encrypted_file = fernet.encrypt(uploaded_file.getvalue())
        f.write(encrypted_file)

def view_documents(tab):
    with tab:
        st.markdown("## Document Library")
        st.markdown("Access and manage your stored legal documents")
        
        # Search and filter options
        col1, col2 = st.columns(2)
        
        with col1:
            search_query = st.text_input("Search documents", placeholder="Enter keywords...")
        
        with col2:
            filter_type = st.multiselect(
                "Filter by type",
                ["Evidence", "Affidavit", "Petition", "Legal Draft", "Court Order", "Other"]
            )
        
        # Display documents
        if SECURE_STORAGE.exists():
            files = list(SECURE_STORAGE.glob("*"))
            for file in files:
                if not file.name.endswith(".txt"):  # Skip OCR text files
                    if (not search_query or search_query.lower() in file.name.lower()) and \
                       (not filter_type or any(ft in file.name for ft in filter_type)):
                        with st.expander(file.name):
                            # Get metadata
                            metadata = get_document_metadata(file.name)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.markdown(f"**Type:** {metadata.get('type', 'N/A')}")
                            with col2:
                                st.markdown(f"**Case:** {metadata.get('case_number', 'N/A')}")
                            with col3:
                                st.markdown(f"**Date:** {metadata.get('upload_date', 'N/A')}")
                            
                            st.markdown(f"**Description:** {metadata.get('description', 'N/A')}")
                            
                            # Document actions
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                if st.button("📄 View", key=f"view_{file.name}"):
                                    display_document(file)
                            with col2:
                                if st.button("⬇️ Download", key=f"download_{file.name}"):
                                    download_document(file)
                            with col3:
                                if st.button("📝 Edit", key=f"edit_{file.name}"):
                                    edit_document(file)
                            with col4:
                                if st.button("🗑️ Delete", key=f"delete_{file.name}"):
                                    delete_document(file)

def display_document(file_path):
    # Read and decrypt document
    with open(file_path, "rb") as f:
        encrypted_content = f.read()
    
    # Get OCR text if available
    text_path = file_path.parent / f"{file_path.name}.txt"
    if text_path.exists():
        with open(text_path, "rb") as f:
            encrypted_text = f.read()
            decrypted_text = fernet.decrypt(encrypted_text).decode()
            st.text_area("Extracted Text", decrypted_text, height=200)
    
    # Display original document
    decrypted_content = fernet.decrypt(encrypted_content)
    if file_path.suffix.lower() in [".jpg", ".png"]:
        image = Image.open(io.BytesIO(decrypted_content))
        st.image(image)
    elif file_path.suffix.lower() == ".pdf":
        st.markdown("PDF preview will be implemented")

def save_document_metadata(filename, doc_type, case_number, description):
    metadata = {
        "type": doc_type,
        "case_number": case_number,
        "description": description,
        "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "versions": [{
            "version": "1.0",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "changes": "Initial version"
        }]
    }
    
    metadata_path = SECURE_STORAGE / f"{filename}.metadata"
    with open(metadata_path, "wb") as f:
        encrypted_metadata = fernet.encrypt(str(metadata).encode())
        f.write(encrypted_metadata)

def get_document_metadata(filename):
    metadata_path = SECURE_STORAGE / f"{filename}.metadata"
    if metadata_path.exists():
        with open(metadata_path, "rb") as f:
            encrypted_metadata = f.read()
            decrypted_metadata = fernet.decrypt(encrypted_metadata).decode()
            return eval(decrypted_metadata)
    return {}

def download_document(file_path):
    with open(file_path, "rb") as f:
        encrypted_content = f.read()
        decrypted_content = fernet.decrypt(encrypted_content)
        st.download_button(
            label="Download Document",
            data=decrypted_content,
            file_name=file_path.name,
            mime="application/octet-stream"
        )

def edit_document(file_path):
    st.markdown("Document editing will be implemented")

def delete_document(file_path):
    # Delete document and related files
    file_path.unlink()
    
    # Delete OCR text if exists
    text_path = file_path.parent / f"{file_path.name}.txt"
    if text_path.exists():
        text_path.unlink()
    
    # Delete metadata if exists
    metadata_path = file_path.parent / f"{file_path.name}.metadata"
    if metadata_path.exists():
        metadata_path.unlink()
    
    st.success("Document deleted successfully!")

def version_control(tab):
    with tab:
        st.markdown("## Version Control")
        st.markdown("Track and manage document versions and changes")
        
        # Get all documents
        if SECURE_STORAGE.exists():
            files = [f for f in SECURE_STORAGE.glob("*") 
                    if not f.name.endswith((".txt", ".metadata"))]
            
            if files:
                # Document selection
                selected_doc = st.selectbox(
                    "Select Document",
                    options=[f.name for f in files]
                )
                
                if selected_doc:
                    # Get document metadata
                    metadata = get_document_metadata(selected_doc)
                    versions = metadata.get("versions", [])
                    
                    # Display version history
                    for version in versions:
                        with st.container():
                            st.markdown(f"### Version {version['version']}")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"**Date:** {version['date']}")
                            
                            with col2:
                                st.markdown(f"**Changes:** {version['changes']}")
                            
                            # Version actions
                            action_col1, action_col2 = st.columns(2)
                            
                            with action_col1:
                                st.button("📄 View", key=f"view_v{version['version']}")
                            with action_col2:
                                st.button("↩️ Restore", key=f"restore_v{version['version']}")
                            
                            st.markdown("---")
            else:
                st.info("No documents found in the system.")
if __name__ == "__main__":
    main()
    # Initialize tabs
    tab1, tab2, tab3 = st.tabs(["Document Upload", "Document Library", "Version Control"])
    upload_documents(tab1)
    view_documents(tab2)
    version_control(tab3)
