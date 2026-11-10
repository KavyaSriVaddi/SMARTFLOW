import streamlit as st


def render_sidebar():
    st.sidebar.title('SMARTFLOW')
    st.sidebar.caption('Intelligent task management')
    pages = [
        '📊 Dashboard',
        '📋 All Tasks',
        '➕ Create Task',
        '⚡ Smart Priorities',
        '⏰ Deadline Monitoring',
        '🔔 Notifications',
        '📈 Productivity Analytics',
        '⚙️ Settings',
        'ℹ️ About SMARTFLOW',
    ]
    selection = st.sidebar.radio('Navigation', pages)
    return selection
