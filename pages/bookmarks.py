import streamlit as st
import json
import os
from datetime import datetime
from legal_data import ipc_sections, it_act_sections, mv_act_sections, legal_precedents

# Initialize session state for bookmarks if not exists
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []

if 'collections' not in st.session_state:
    st.session_state.collections = []

class BookmarkManager:
    def __init__(self):
        self.storage_path = 'data/bookmarks.json'
        self.load_bookmarks()
    
    def load_bookmarks(self):
        """Load bookmarks from storage"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    st.session_state.bookmarks = data.get('bookmarks', [])
                    st.session_state.collections = data.get('collections', [])
        except Exception as e:
            st.error(f"Error loading bookmarks: {str(e)}")
    
    def save_bookmarks(self):
        """Save bookmarks to storage"""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump({
                    'bookmarks': st.session_state.bookmarks,
                    'collections': st.session_state.collections
                }, f, indent=2)
        except Exception as e:
            st.error(f"Error saving bookmarks: {str(e)}")
    
    def add_bookmark(self, section_id, act, title, notes="", collection=""):
        """Add a new bookmark"""
        bookmark = {
            'id': len(st.session_state.bookmarks),
            'section_id': section_id,
            'act': act,
            'title': title,
            'notes': notes,
            'collection': collection,
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.bookmarks.append(bookmark)
        self.save_bookmarks()
        return bookmark
    
    def update_bookmark(self, bookmark_id, notes=None, collection=None):
        """Update an existing bookmark"""
        for bookmark in st.session_state.bookmarks:
            if bookmark['id'] == bookmark_id:
                if notes is not None:
                    bookmark['notes'] = notes
                if collection is not None:
                    bookmark['collection'] = collection
                self.save_bookmarks()
                return bookmark
        return None
    
    def delete_bookmark(self, bookmark_id):
        """Delete a bookmark"""
        st.session_state.bookmarks = [
            b for b in st.session_state.bookmarks if b['id'] != bookmark_id
        ]
        self.save_bookmarks()
    
    def get_collections(self):
        """Get list of all collections"""
        return list(set(b['collection'] for b in st.session_state.bookmarks if b['collection']))
    
    def get_bookmarks_by_collection(self, collection):
        """Get all bookmarks in a collection"""
        return [b for b in st.session_state.bookmarks if b['collection'] == collection]

# Initialize bookmark manager
bookmark_manager = BookmarkManager()

def main():
    st.title("Legal Bookmarks & Annotations")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select View",
        ["All Bookmarks", "Collections", "Add Bookmark"]
    )
    
    if page == "Add Bookmark":
        show_add_bookmark_page()
    elif page == "Collections":
        show_collections_page()
    else:
        show_all_bookmarks_page()

def show_add_bookmark_page():
    st.header("Add New Bookmark")
    
    # Select Act
    act = st.selectbox(
        "Select Act",
        ["IPC", "IT Act", "MV Act"]
    )
    
    # Get sections based on selected act
    sections = {
        "IPC": ipc_sections,
        "IT Act": it_act_sections,
        "MV Act": mv_act_sections
    }[act]
    
    # Select Section
    section_options = [f"{section} - {title}" 
                      for section, title in sections.items()]
    selected_section = st.selectbox("Select Section", section_options)
    
    # Get section ID from selection
    section_id = selected_section.split(' - ')[0]
    
    # Notes input
    notes = st.text_area("Add Notes", "")
    
    # Collection input
    collections = [""] + bookmark_manager.get_collections()
    collection = st.selectbox(
        "Add to Collection",
        collections,
        format_func=lambda x: "None" if x == "" else x
    )
    
    # New collection input
    new_collection = st.text_input("Or Create New Collection")
    if new_collection:
        collection = new_collection
    
    if st.button("Save Bookmark"):
        bookmark = bookmark_manager.add_bookmark(
            section_id, act, selected_section, notes, collection
        )
        st.success("Bookmark added successfully!")

def show_collections_page():
    st.header("Collections")
    
    collections = bookmark_manager.get_collections()
    if not collections:
        st.info("No collections created yet. Create one when adding a bookmark!")
        return
    
    for collection in collections:
        with st.expander(f"Collection: {collection}"):
            bookmarks = bookmark_manager.get_bookmarks_by_collection(collection)
            for bookmark in bookmarks:
                show_bookmark(bookmark)

def show_all_bookmarks_page():
    st.header("All Bookmarks")
    
    if not st.session_state.bookmarks:
        st.info("No bookmarks saved yet. Add some using the 'Add Bookmark' page!")
        return
    
    for bookmark in st.session_state.bookmarks:
        show_bookmark(bookmark)

def show_bookmark(bookmark):
    """Display a single bookmark with its details and actions"""
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(bookmark['title'])
            st.text(f"Act: {bookmark['act']} | Section: {bookmark['section_id']}")
            
            if bookmark['notes']:
                st.text_area(
                    "Notes",
                    bookmark['notes'],
                    key=f"notes_{bookmark['id']}",
                    on_change=lambda: bookmark_manager.update_bookmark(
                        bookmark['id'],
                        notes=st.session_state[f"notes_{bookmark['id']}"])
                )
            
            if bookmark['collection']:
                st.text(f"Collection: {bookmark['collection']}")
            
            st.text(f"Added: {datetime.fromisoformat(bookmark['timestamp']).strftime('%Y-%m-%d %H:%M')}")
        
        with col2:
            if st.button("Delete", key=f"delete_{bookmark['id']}"):
                bookmark_manager.delete_bookmark(bookmark['id'])
                st.rerun()

if __name__ == "__main__":
    main()