import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

CACHE_FILE = 'amendment_cache.json'
CACHE_DURATION_HOURS = 24

def load_cached_amendments():
    """Load amendments from cache if available and not expired"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
                cache_time = datetime.fromisoformat(cache['timestamp'])
                if (datetime.now() - cache_time).total_seconds() < CACHE_DURATION_HOURS * 3600:
                    return cache['amendments']
    except Exception as e:
        print(f"Error loading cache: {e}")
    return None

def save_to_cache(amendments):
    """Save amendments to cache with timestamp"""
    try:
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'amendments': amendments
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
    except Exception as e:
        print(f"Error saving cache: {e}")

def fetch_amendments():
    """Fetch amendments from multiple sources with caching"""
    # Try to load from cache first
    cached = load_cached_amendments()
    if cached:
        return cached

    amendments = []
    sources = [
        'https://legislative.gov.in/acts-and-bills',
        'https://egazette.gov.in/recent-amendments',
        'https://www.indiacode.nic.in/recent-amendments'
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    for url in sources:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find amendment entries
            entries = soup.find_all(['div', 'article'], class_=['amendment', 'gazette-notification'])
            
            for entry in entries:
                try:
                    amendment = {
                        'date': entry.find(['time', 'span'], class_='date').text.strip(),
                        'act': entry.find(['h3', 'h4'], class_=['act-name', 'title']).text.strip(),
                        'section': entry.find('span', class_=['section', 'provision']).text.strip(),
                        'summary': entry.find(['p', 'div'], class_='summary').text.strip(),
                        'old_text': entry.find('div', class_=['old-text', 'previous']).text.strip(),
                        'new_text': entry.find('div', class_=['new-text', 'amended']).text.strip(),
                        'source': url
                    }
                    amendments.append(amendment)
                except AttributeError:
                    continue

        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            continue

    # Cache the results
    if amendments:
        save_to_cache(amendments)

    return amendments

def update_amendment_data():
    """Update amendment_data.py with fetched amendments"""
    from amendment_data import amendment_history
    
    amendments = fetch_amendments()
    updated = 0

    for amendment in amendments:
        try:
            act = amendment['act']
            section = amendment['section']
            
            if act and section:
                if act not in amendment_history:
                    amendment_history[act] = {}
                if section not in amendment_history[act]:
                    amendment_history[act][section] = []
                
                formatted = {
                    'implementation_date': amendment['date'],
                    'old_text': amendment['old_text'],
                    'new_text': amendment['new_text'],
                    'summary': amendment['summary']
                }
                
                # Check for duplicates
                if not any(a['implementation_date'] == formatted['implementation_date'] 
                         for a in amendment_history[act][section]):
                    amendment_history[act][section].append(formatted)
                    updated += 1
        
        except Exception as e:
            print(f"Error processing amendment: {e}")
            continue
    
    return updated