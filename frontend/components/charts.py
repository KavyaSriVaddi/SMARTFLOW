import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def render_charts():
    api = st.session_state['api_client']
    st.subheader('Analytics')
    status_data = api.get('/api/analytics/status-distribution') or []
    importance_data = api.get('/api/analytics/importance-distribution') or []
    completion_data = api.get('/api/analytics/completion-trend') or []
    weekly_data = api.get('/api/analytics/weekly-productivity') or []
    overdue_data = api.get('/api/analytics/overdue-analysis') or []

    if not any([status_data, importance_data, completion_data, weekly_data, overdue_data]):
        st.info('No analytics data available yet.')
        return

    col1, col2 = st.columns(2)
    with col1:
        if status_data:
            df = pd.DataFrame(status_data)
            fig, ax = plt.subplots()
            ax.pie(df['value'], labels=df['name'], autopct='%1.1f%%', startangle=90)
            ax.set_title('Task Status Distribution')
            st.pyplot(fig)
    with col2:
        if importance_data:
            df = pd.DataFrame(importance_data)
            fig, ax = plt.subplots()
            ax.bar(df['name'], df['value'], color=['green', 'gold', 'orange', 'red'])
            ax.set_title('Importance Distribution')
            ax.set_xlabel('Importance')
            ax.set_ylabel('Tasks')
            st.pyplot(fig)

    if completion_data:
        df = pd.DataFrame(completion_data)
        fig, ax = plt.subplots()
        ax.plot(df['date'], df['completed'], marker='o')
        ax.set_title('Completion Trend')
        ax.set_xlabel('Date')
        ax.set_ylabel('Completed Tasks')
        st.pyplot(fig)

    if weekly_data:
        df = pd.DataFrame(weekly_data)
        fig, ax = plt.subplots()
        ax.bar(df['week'], df['completed'], color='indigo')
        ax.set_title('Weekly Productivity')
        ax.set_xlabel('Week')
        ax.set_ylabel('Completed')
        st.pyplot(fig)

    if overdue_data:
        df = pd.DataFrame(overdue_data)
        fig, ax = plt.subplots()
        ax.bar(df['name'], df['count'], color=['red', 'orange', 'gold', 'green'])
        ax.set_title('Overdue Task Analysis')
        ax.set_xlabel('Importance')
        ax.set_ylabel('Overdue Count')
        st.pyplot(fig)
