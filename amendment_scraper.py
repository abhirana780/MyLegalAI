import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def scrape_india_code(max_retries=3, retry_delay=5):
    """Scrape amendments from India Code website with retry mechanism"""
    from time import sleep
    amendments = []
    
    for attempt in range(max_retries):
        try:
            url = "https://www.indiacode.nic.in/handle/123456789/1362/recent-updates"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Connection': 'keep-alive'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all amendment entries
            amendment_entries = soup.find_all(['div', 'article'], {'class': ['amendment-entry', 'amendment-item']})
            
            if not amendment_entries and attempt < max_retries - 1:
                print(f"No amendments found on attempt {attempt + 1}, retrying...")
                sleep(retry_delay)
                continue
                
            for entry in amendment_entries:
                try:
                    # Extract amendment details
                    date_elem = entry.find('span', class_='date')
                    act_elem = entry.find('h3', class_='act-name')
                    section_elem = entry.find('span', class_='section')
                    summary_elem = entry.find('div', class_='summary')
                    
                    if date_elem and act_elem:
                        amendment = {
                            'date': date_elem.text.strip(),
                            'act': act_elem.text.strip(),
                            'section': section_elem.text.strip() if section_elem else '',
                            'previous_text': entry.find('div', class_='old-text').text.strip() if entry.find('div', class_='old-text') else '',
                            'amended_text': entry.find('div', class_='new-text').text.strip() if entry.find('div', class_='new-text') else '',
                            'act_name': entry.find('span', class_='amendment-act').text.strip() if entry.find('span', class_='amendment-act') else '',
                            'summary': summary_elem.text.strip() if summary_elem else ''
                        }
                        amendments.append(amendment)
                except Exception as e:
                    print(f"Error parsing amendment entry: {e}")
                    continue
            
            return amendments
            
        except requests.RequestException as e:
            print(f"Request failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                sleep(retry_delay)
            continue
        except Exception as e:
            print(f"Unexpected error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                sleep(retry_delay)
            continue
    
    return amendments
    except Exception as e:
        print(f"Error scraping India Code: {e}")
        return []

def scrape_hp_amendments(max_retries=3, retry_delay=5):
    """Scrape amendments specific to Himachal Pradesh with retry mechanism"""
    from time import sleep
    amendments = []
    
    urls = [
        "https://legislative.gov.in/state-acts/himachal-pradesh",
        "https://himachal.nic.in/en/acts-and-rules",
        "https://himachal.nic.in/en/notifications"
    ]
    
    for url in urls:
        for attempt in range(max_retries):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Connection': 'keep-alive'
                }
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all amendment entries for HP
                amendment_entries = soup.find_all(['div', 'article'], 
                    {'class': ['state-amendment', 'amendment-item', 'notification-item', 'legal-update']})
                
                if not amendment_entries and attempt < max_retries - 1:
                    print(f"No amendments found on {url} attempt {attempt + 1}, retrying...")
                    sleep(retry_delay)
                    continue
                
                for entry in amendment_entries:
                    try:
                        # Extract HP specific amendment details
                        date_elem = entry.find(['span', 'time'], {'class': ['gazette-date', 'date', 'published-date']})
                        act_elem = entry.find(['h4', 'h3', 'h2'], {'class': ['act-title', 'title']})
                        section_elem = entry.find('span', {'class': ['section-number', 'section-id']})
                        
                        if date_elem and act_elem:
                            amendment = {
                                'date': date_elem.text.strip(),
                                'act': f"HP {act_elem.text.strip()}",  # Prefix with HP to identify state amendments
                                'section': section_elem.text.strip() if section_elem else '',
                                'previous_text': entry.find(['div', 'p'], {'class': ['original-text', 'old-content']}).text.strip() if entry.find(['div', 'p'], {'class': ['original-text', 'old-content']}) else '',
                                'amended_text': entry.find(['div', 'p'], {'class': ['modified-text', 'new-content']}).text.strip() if entry.find(['div', 'p'], {'class': ['modified-text', 'new-content']}) else '',
                                'act_name': entry.find('span', {'class': ['amendment-reference', 'reference']}).text.strip() if entry.find('span', {'class': ['amendment-reference', 'reference']}) else '',
                                'summary': entry.find(['div', 'p'], {'class': ['amendment-summary', 'summary']}).text.strip() if entry.find(['div', 'p'], {'class': ['amendment-summary', 'summary']}) else ''
                            }
                            amendments.append(amendment)
                    except Exception as e:
                        print(f"Error parsing HP amendment entry: {e}")
                        continue
                
                break  # Successfully processed this URL, move to next
                
            except requests.RequestException as e:
                print(f"Request failed for {url} on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    sleep(retry_delay)
                continue
            except Exception as e:
                print(f"Unexpected error for {url} on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    sleep(retry_delay)
                continue
    
    return amendments
    except Exception as e:
        print(f"Error scraping HP amendments: {e}")
        return []

def format_amendment(raw_data):
    """Format scraped amendment data to match our data structure"""
    return {
        'implementation_date': raw_data.get('date'),
        'old_text': raw_data.get('previous_text', ''),
        'new_text': raw_data.get('amended_text', ''),
        'amendment_act': raw_data.get('act_name', ''),
        'summary': raw_data.get('summary', '')
    }

def update_amendment_history(amendments):
    """Update the amendment_history with new scraped data"""
    from amendment_data import amendment_history
    
    def parse_date(date_str):
        """Parse date string to standard format"""
        try:
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d', '%B %d, %Y', '%d %B %Y']:
                try:
                    return datetime.strptime(date_str.strip(), fmt).strftime('%Y-%m-%d')
                except ValueError:
                    continue
            # Try to extract date using regex if standard formats fail
            date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
            match = re.search(date_pattern, date_str)
            if match:
                date_str = match.group(0)
                # Try parsing the extracted date
                for fmt in ['%d-%m-%Y', '%d/%m/%Y']:
                    try:
                        return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            return datetime.now().strftime('%Y-%m-%d')  # Use current date as fallback
        except Exception as e:
            print(f"Error parsing date {date_str}: {e}")
            return datetime.now().strftime('%Y-%m-%d')
    
    updated_count = 0
    for amendment in amendments:
        try:
            act = amendment.get('act')
            section = amendment.get('section')
            
            if not act or not section:
                print(f"Skipping amendment with missing act or section: {amendment}")
                continue
                
            # Format the amendment data
            formatted_amendment = format_amendment(amendment)
            formatted_amendment['implementation_date'] = parse_date(amendment.get('date', ''))
            
            # Initialize nested dictionaries if needed
            if act not in amendment_history:
                amendment_history[act] = {}
            if section not in amendment_history[act]:
                amendment_history[act][section] = []
                
            # Check if amendment already exists
            if not any(existing['implementation_date'] == formatted_amendment['implementation_date'] 
                      for existing in amendment_history[act][section]):
                amendment_history[act][section].append(formatted_amendment)
                updated_count += 1
                
        except Exception as e:
            print(f"Error processing amendment: {e}")
            continue
            
    return updated_count
            if act not in amendment_history:
                amendment_history[act] = {}
            if section not in amendment_history[act]:
                amendment_history[act][section] = []
                
            # Check for duplicates based on implementation date and content
            is_duplicate = False
            for existing in amendment_history[act][section]:
                if (existing['implementation_date'] == formatted_amendment['implementation_date'] and
                    existing['new_text'] == formatted_amendment['new_text']):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                amendment_history[act][section].append(formatted_amendment)
                print(f"Added new amendment for {act} Section {section} dated {formatted_amendment['implementation_date']}")
        except Exception as e:
            print(f"Error processing amendment: {e}")
            continue
    
    # Sort amendments by date for each section
    for act in amendment_history:
        for section in amendment_history[act]:
            amendment_history[act][section].sort(key=lambda x: x['implementation_date'], reverse=True)


def fetch_latest_amendments():
    """Fetch and update amendments from all sources"""
    all_amendments = []
    
    # Fetch from India Code
    india_code_amendments = scrape_india_code()
    all_amendments.extend(india_code_amendments)
    
    # Fetch HP specific amendments
    hp_amendments = scrape_hp_amendments()
    all_amendments.extend(hp_amendments)
    
    # Update the amendment history
    update_amendment_history(all_amendments)
    
    return len(all_amendments)