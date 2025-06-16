import streamlit as st
import psutil
import time
import os
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- Simple Auth ---
def check_login():
    if 'admin_logged_in' not in st.session_state:
        st.session_state['admin_logged_in'] = False
    if not st.session_state['admin_logged_in']:
        st.markdown('<style>\n.login-card {\n  max-width: 400px;\n  margin: 80px auto 0 auto;\n  background: #fff;\n  border-radius: 16px;\n  box-shadow: 0 4px 24px rgba(0,0,0,0.10);\n  padding: 2.5rem 2rem 2rem 2rem;\n  text-align: center;\n}\n.login-logo {\n  width: 64px;\n  margin-bottom: 1rem;\n}\n.login-title {\n  font-size: 2rem;\n  font-weight: 700;\n  color: #0052cc;\n  margin-bottom: 0.5rem;\n}\n.login-subtitle {\n  color: #888;\n  margin-bottom: 1.5rem;\n}\n.stTextInput>div>div>input {\n  border-radius: 8px;\n  border: 1px solid #e0e0e0;\n  padding: 0.75rem;\n}\n.stButton>button {\n  background: linear-gradient(90deg, #0052cc 60%, #0077ff 100%);\n  color: #fff;\n  border-radius: 8px;\n  font-weight: 600;\n  padding: 0.75rem 2rem;\n  margin-top: 1rem;\n  transition: background 0.2s;\n}\n.stButton>button:hover {\n  background: #003d99;\n}\n</style>', unsafe_allow_html=True)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="center-logo"><img src="assets/logo.svg" class="animated-logo" alt="MyLegalAI Logo"></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Admin Login</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Welcome to MyLegalAI Admin Dashboard</div>', unsafe_allow_html=True)
        username = st.text_input('Username', key='login_username')
        password = st.text_input('Password', type='password', key='login_password')
        login_btn = st.button('Login', key='login_btn')
        if login_btn:
            if username == 'abhay' and password == 'abhay1150':
                st.session_state['admin_logged_in'] = True
                st.rerun()
            else:
                st.error('Invalid credentials')
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

check_login()

st.set_page_config(page_title='Admin Dashboard', page_icon='🔒', layout='wide')
st.markdown('<style>div.block-container{padding-top:2rem;} .stMetric{background:#f0f2f6;border-radius:8px;} .stButton>button{background:#0052cc;color:#fff;} .stDataFrame{background:#fff;border-radius:8px;} .stPlotlyChart{background:#fff;border-radius:8px;}</style>', unsafe_allow_html=True)
st.title('Admin Dashboard')

# --- Live System Stats with Graphs ---
st.header('Live System Stats')
col1, col2 = st.columns(2)

with col1:
    st.subheader('CPU & RAM Usage (Live)')
    cpu_data = []
    ram_data = []
    time_labels = []
    chart_placeholder = st.empty()
    for i in range(20):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        cpu_data.append(cpu)
        ram_data.append(mem)
        time_labels.append(datetime.now().strftime('%H:%M:%S'))
        df_stats = pd.DataFrame({'Time': time_labels, 'CPU': cpu_data, 'RAM': ram_data})
        fig = px.line(df_stats, x='Time', y=['CPU','RAM'], markers=True, title='CPU & RAM Usage (%)')
        fig.update_layout(legend_title_text='Metric', yaxis=dict(range=[0,100]))
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.1)

with col2:
    st.subheader('Active Users (Session)')
    st.metric('Active Users', len(st.session_state))
    st.subheader('Network Stats (Live)')
    net_data = []
    net_time = []
    net_placeholder = st.empty()
    for i in range(20):
        net = psutil.net_io_counters()
        net_data.append({'Sent': net.bytes_sent, 'Recv': net.bytes_recv})
        net_time.append(datetime.now().strftime('%H:%M:%S'))
        df_net = pd.DataFrame(net_data, index=net_time)
        fig_net = px.area(df_net, x=df_net.index, y=['Sent','Recv'], title='Network Bytes (Cumulative)')
        fig_net.update_layout(legend_title_text='Direction')
        net_placeholder.plotly_chart(fig_net, use_container_width=True)
        time.sleep(0.1)

# --- User Activity Logging ---
LOG_FILE = 'admin_activity_log.csv'

def init_log():
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=['timestamp','username','page','action','details'])
        df.to_csv(LOG_FILE, index=False)

init_log()

def log_action(username, page, action, details=''):
    df = pd.DataFrame([[datetime.now().isoformat(), username, page, action, details]],
                      columns=['timestamp','username','page','action','details'])
    df.to_csv(LOG_FILE, mode='a', header=False, index=False)

log_action('abhay', 'admin_dashboard', 'access', 'Admin dashboard opened')

# --- Interactive Log Viewer ---
st.header('User Activity Logs')
if os.path.exists(LOG_FILE):
    logs = pd.read_csv(LOG_FILE)
    st.markdown('**Filter by Action:**')
    actions = ['All'] + sorted(logs['action'].unique())
    selected_action = st.selectbox('Action', actions, index=0)
    if selected_action != 'All':
        logs = logs[logs['action'] == selected_action]
    st.markdown('**Filter by Username:**')
    users = ['All'] + sorted(logs['username'].unique())
    selected_user = st.selectbox('Username', users, index=0)
    if selected_user != 'All':
        logs = logs[logs['username'] == selected_user]
    st.dataframe(logs.sort_values('timestamp', ascending=False), use_container_width=True)
else:
    st.info('No logs yet.')

# --- Page Analytics (Live & Interactive) ---
st.header('Page Analytics')
pages = ['Home', 'Rights Predictor', 'Hearing Scheduler', 'Judicial Analytics', 'Notifications', 'Bookmarks', 'Admin Dashboard']
import random
analytics = pd.DataFrame({
    'Page': pages,
    'Visits': [random.randint(10, 200) for _ in pages],
    'Unique Users': [random.randint(5, 100) for _ in pages],
    'Avg. Time (s)': [random.randint(30, 300) for _ in pages]
})

st.markdown('**Select Analytics Metric:**')
metric = st.radio('Metric', ['Visits', 'Unique Users', 'Avg. Time (s)'], horizontal=True)
fig = px.bar(analytics, x='Page', y=metric, color=metric, title=f'Page {metric}', text_auto=True)
fig.update_layout(xaxis_title='Page', yaxis_title=metric)
st.plotly_chart(fig, use_container_width=True)

# --- Live Log Viewer ---
st.header('Live Log Viewer')
if st.button('Refresh Logs'):
    st.experimental_rerun()
if os.path.exists(LOG_FILE):
    st.dataframe(pd.read_csv(LOG_FILE).sort_values('timestamp', ascending=False).head(50), use_container_width=True)

st.markdown('---')
st.info('This admin dashboard is for authorized use only. All actions are logged.')