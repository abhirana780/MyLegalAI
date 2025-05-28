
from datetime import datetime
import json
import os
from pathlib import Path

def log_access(page_name, user_action="view"):
    """Log page access with timestamp"""
    log_file = Path("data/access_logs.json")
    
    # Create directory if it doesn't exist
    log_file.parent.mkdir(exist_ok=True)
    
    # Load existing logs
    if log_file.exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    # Add new log entry
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "page": page_name,
        "action": user_action
    })
    
    # Save updated logs
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
