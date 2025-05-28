import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import psutil
import numpy as np
from utils.helpers import load_json_data, save_json_data
from utils.access_logger import log_access

# Admin credentials
ADMIN_USERNAME = "abhay1150"
ADMIN_PASSWORD = "abhay@1150"

def check_admin_auth():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    return st.session_state.admin_authenticated

def admin_login():
    st.markdown("""
    <style>
    .admin-login {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.2));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .login-header {
        text-align: center;
        color: #0066cc;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
           
            st.markdown('<h2 class="login-header">🔐 Admin Access</h2>', unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="Enter admin username")
            password = st.text_input("Password", type="password", placeholder="Enter admin password")

            if st.button("Login", type="primary", use_container_width=True):
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            st.markdown('</div>', unsafe_allow_html=True)

def load_access_logs():
    try:
        logs = load_json_data("data/access_logs.json")
        return logs if isinstance(logs, list) else []
    except:
        return []

def get_user_metrics():
    logs = load_access_logs()
    today = datetime.now().date()
    today_logs = [log for log in logs if datetime.fromisoformat(log.get('timestamp', '')).date() == today]

    return {
        "total_users": len(set(log.get('user_id', '') for log in logs)),
        "active_users": len(set(log.get('user_id', '') for log in today_logs)),
        "new_users_today": len(today_logs),
        "total_page_views": len(logs)
    }

def get_system_health():
    try:
        import psutil
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            "cpu_usage": f"{cpu}%",
            "memory_usage": f"{memory.percent}%",
            "storage_used": f"{disk.percent}%",
            "system_uptime": str(timedelta(seconds=int(psutil.boot_time())))
        }
    except:
        return {
            "cpu_usage": "N/A",
            "memory_usage": "N/A",
            "storage_used": "N/A",
            "system_uptime": "N/A"
        }

def create_usage_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['dates'], y=data['views'], mode='lines+markers',
                            line=dict(color='#0066cc', width=2),
                            marker=dict(size=8, color='#003366')))
    fig.update_layout(
        title="System Usage Trends",
        xaxis_title="Date",
        yaxis_title="Views",
        template="plotly_white",
        height=400
    )
    return fig

def get_real_time_metrics():
    """Get real-time metrics from access logs and system data"""
    logs = load_access_logs()
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)

    # Parse timestamps to datetime objects
    for log in logs:
        log['timestamp'] = datetime.fromisoformat(log['timestamp'])

    # Calculate real metrics
    metrics = {
        "active_users_hour": len(set(log.get('user_id', '') for log in logs if log['timestamp'] > hour_ago)),
        "page_views_hour": len([log for log in logs if log['timestamp'] > hour_ago]),
        "active_users_today": len(set(log.get('user_id', '') for log in logs if log['timestamp'] > day_ago)),
        "total_sessions": len(set(log.get('session_id', '') for log in logs)),
        "weekly_active_users": len(set(log.get('user_id', '') for log in logs if log['timestamp'] > week_ago)),
        "popular_pages": get_popular_pages(logs),
        "user_engagement": calculate_user_engagement(logs)
    }

    return metrics

def get_popular_pages(logs):
    """Calculate most visited pages in the last 24 hours"""
    day_ago = datetime.now() - timedelta(days=1)
    recent_logs = [log for log in logs if log['timestamp'] > day_ago]
    page_counts = {}
    for log in recent_logs:
        page = log.get('page', '')
        page_counts[page] = page_counts.get(page, 0) + 1
    return dict(sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:5])

def calculate_user_engagement(logs):
    """Calculate user engagement metrics"""
    user_sessions = {}
    for log in logs:
        user_id = log.get('user_id', '')
        if user_id not in user_sessions:
            user_sessions[user_id] = []
        user_sessions[user_id].append(log['timestamp'])

    # Calculate average session duration
    durations = []
    for sessions in user_sessions.values():
        sorted_sessions = sorted(sessions)
        for i in range(len(sorted_sessions)-1):
            duration = (sorted_sessions[i+1] - sorted_sessions[i]).total_seconds()
            if duration < 3600:  # Consider sessions less than 1 hour apart
                durations.append(duration)

    return {
        "avg_session_duration": sum(durations)/len(durations) if durations else 0,
        "total_users": len(user_sessions)
    }

def get_system_health_psutil():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network_io": psutil.net_io_counters()
    }

def main():
    st.set_page_config(page_title="Admin Dashboard", layout="wide")

    # Custom CSS
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.9));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(0,51,102,0.1);
        box-shadow: 0 8px 32px rgba(0,51,102,0.1);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,51,102,0.15);
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(45deg, #003366 30%, #0066cc 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .metric-label {
        color: #4a5568;
        font-size: 16px;
        font-weight: 500;
    }
    .status-indicator {
        height: 12px;
        width: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        transition: all 0.3s ease;
    }
    .status-good { background-color: #10B981; box-shadow: 0 0 10px rgba(16, 185, 129, 0.4); }
    .status-warning { background-color: #F59E0B; box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }
    .status-critical { background-color: #EF4444; box-shadow: 0 0 10px rgba(239, 68, 68, 0.4); }
    .dashboard-section {
        animation: fadeIn 0.5s ease-out;
        margin-bottom: 2rem;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #0066cc;
    }
    .metric-label {
        color: #666;
        font-size: 14px;
    }
    .status-indicator {
        height: 10px;
        width: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    .status-good { background-color: #00cc66; }
    .status-warning { background-color: #ffcc00; }
    .status-critical { background-color: #ff3333; }
    </style>
    """, unsafe_allow_html=True)

    if not check_admin_auth():
        admin_login()
        return

    # Header with logout
    col1, col2 = st.columns([3,1])
    with col1:
        st.title("🎛️ Admin Control Center")
    with col2:
        if st.button("🚪 Logout", type="primary"):
            st.session_state.admin_authenticated = False
            st.rerun()

    # Main Navigation
    tabs = st.tabs(["📊 Dashboard", "📈 Analytics", "🖥️ System", "👥 Users", "⚙️ Settings", "🔔 Notifications", "📁 Content"])

    with tabs[0]:
        st.subheader("System Overview")
        metrics = get_user_metrics()
        system = get_system_health()

        # Metrics Grid
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">""" + str(metrics["total_users"]) + """</div>
                <div class="metric-label">Total Users</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">""" + str(metrics["active_users"]) + """</div>
                <div class="metric-label">Active Users</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">""" + str(metrics["new_users_today"]) + """</div>
                <div class="metric-label">New Users Today</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">""" + str(metrics["total_page_views"]) + """</div>
                <div class="metric-label">Total Page Views</div>
            </div>
            """, unsafe_allow_html=True)

        # System Health
        st.subheader("System Health")
        col1, col2, col3 = st.columns(3)
        with col1:
            cpu_status = "good" if float(system["cpu_usage"].strip('%')) < 70 else "warning"
            st.markdown(f"""
            <div class="metric-card">
                <span class="status-indicator status-{cpu_status}"></span>
                <div class="metric-value">{system["cpu_usage"]}</div>
                <div class="metric-label">CPU Usage</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            memory_status = "good" if float(system["memory_usage"].strip('%')) < 80 else "warning"
            st.markdown(f"""
            <div class="metric-card">
                <span class="status-indicator status-{memory_status}"></span>
                <div class="metric-value">{system["memory_usage"]}</div>
                <div class="metric-label">Memory Usage</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            storage_status = "good" if float(system["storage_used"].strip('%')) < 85 else "warning"
            st.markdown(f"""
            <div class="metric-card">
                <span class="status-indicator status-{storage_status}"></span>
                <div class="metric-value">{system["storage_used"]}</div>
                <div class="metric-label">Storage Used</div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[1]:
        st.subheader("Analytics Dashboard")

        # Date Range Selector
        col1, col2 = st.columns([2,2])
        with col1:
            date_range = st.selectbox("Time Period", 
                                    ["Last 7 Days", "Last 30 Days", "Last 90 Days"],
                                    index=1)
        with col2:
            chart_type = st.selectbox("Chart Type",
                                    ["Line Chart", "Bar Chart", "Area Chart"],
                                    index=0)

        # Sample data - replace with actual analytics
        sample_data = {
            'dates': pd.date_range(end=datetime.now(), periods=30),
            'views': np.random.randint(100, 1000, 30)
        }
        st.plotly_chart(create_usage_chart(sample_data), use_container_width=True)

        # Most Visited Pages
        st.subheader("Most Visited Pages")
        page_data = pd.DataFrame({
            'Page': ['Legal Codes', 'Case Search', 'Rights Predictor', 'Document Management'],
            'Views': [1200, 950, 850, 700]
        })
        st.bar_chart(page_data.set_index('Page'))

    with tabs[2]:
        st.subheader("System Monitoring")

        # System Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("System Uptime", system["system_uptime"])
            st.metric("Active Sessions", "24")
            st.metric("API Response Time", "230ms")
        with col2:
            st.metric("Database Size", "2.3 GB")
            st.metric("Cache Hit Rate", "94%")
            st.metric("Error Rate", "0.02%")

        # System Logs
        st.subheader("Recent System Logs")
        with st.expander("View Logs"):
            st.code("""
[2024-01-20 10:15:23] INFO: System startup complete
[2024-01-20 10:15:25] INFO: Database connection established
[2024-01-20 10:15:30] INFO: Cache initialized
[2024-01-20 10:16:00] WARN: High memory usage detected
            """)

    with tabs[3]:
        st.subheader("User Management")

        # User Actions
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Add New User"):
                new_username = st.text_input("Username")
                new_role = st.selectbox("Role", ["User", "Admin", "Moderator"])
                new_email = st.text_input("Email")
                if st.button("Add User"):
                    st.success(f"User {new_username} added successfully!")

        with col2:
            with st.expander("User Permissions"):
                st.multiselect("Select Permissions",
                             ["View Documents", "Edit Documents", "Delete Documents",
                              "Manage Users", "Access Analytics", "System Settings"])

        # User List
        st.subheader("Active Users")
        user_df = pd.DataFrame({
            'Username': ['user1', 'user2', 'user3'],
            'Role': ['Admin', 'User', 'Moderator'],
            'Last Active': pd.date_range(start='2024-01-01', periods=3),
            'Status': ['Online', 'Offline', 'Away']
        })
        st.dataframe(user_df, use_container_width=True)

    with tabs[4]:
        st.subheader("System Settings")

        # General Settings
        with st.expander("General Settings", expanded=True):
            st.number_input("Session Timeout (minutes)", min_value=5, value=30)
            st.selectbox("Default Theme", ["Light", "Dark", "System"])
            st.checkbox("Enable Debug Mode")
            st.checkbox("Enable Email Notifications")

        # Security Settings
        with st.expander("Security Settings"):
            st.number_input("Maximum Login Attempts", min_value=3, value=5)
            st.number_input("Password Expiry (days)", min_value=30, value=90)
            st.checkbox("Enable Two-Factor Authentication")
            st.checkbox("Force SSL")

        # Backup Settings
        with st.expander("Backup Settings"):
            st.checkbox("Enable Auto Backup")
            st.select_slider("Backup Frequency", options=['Daily', 'Weekly', 'Monthly'])
            if st.button("Create Backup Now"):
                st.success("Backup created successfully!")

    with tabs[5]:
        st.subheader("Notification Center")

        # Notification Settings
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Email Notifications")
            st.checkbox("SMS Notifications")
            st.checkbox("System Alerts")
        with col2:
            st.checkbox("User Activity Alerts")
            st.checkbox("Error Notifications")
            st.checkbox("Performance Alerts")

        # Recent Notifications
        st.subheader("Recent Notifications")
        notifications = [
            {"type": "success", "message": "System backup completed successfully"},
            {"type": "warning", "message": "High CPU usage detected"},
            {"type": "info", "message": "New user registration"},
        ]
        for notif in notifications:
            if notif["type"] == "success":
                st.success(notif["message"])
            elif notif["type"] == "warning":
                st.warning(notif["message"])
            else:
                st.info(notif["message"])

    with tabs[6]:
        st.subheader("Content Management")

        # Legal Content
        with st.expander("Legal Content Management"):
            st.selectbox("Select Content Type", 
                        ["Legal Codes", "Case Laws", "Rights Information"])
            st.text_area("Content", height=200)
            col1, col2 = st.columns(2)
            with col1:
                st.button("Save Changes")
            with col2:
                st.button("Preview Changes")

        # Document Templates
        with st.expander("Document Templates"):
            st.file_uploader("Upload Template")
            st.dataframe(pd.DataFrame({
                'Template Name': ['Rights Template', 'Case Template'],
                'Last Modified': ['2024-01-15', '2024-01-18']
            }))

if __name__ == "__main__":
    main()