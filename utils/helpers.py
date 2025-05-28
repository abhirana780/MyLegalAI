"""Helper functions for the LegalDefendAI application."""

from datetime import datetime
import json
import os

def load_json_data(file_path):
    """Load data from a JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        raise Exception(f"Error loading JSON data: {str(e)}")

def save_json_data(data, file_path):
    """Save data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise Exception(f"Error saving JSON data: {str(e)}")

def format_timestamp(timestamp_str):
    """Format timestamp string to human readable format."""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime('%Y-%m-%d %H:%M')
    except Exception:
        return timestamp_str

def validate_file_type(filename, allowed_types):
    """Validate if file type is allowed."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_types

def get_file_size(file_path):
    """Get file size in human readable format."""
    try:
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    except Exception:
        return "Unknown size"