import os
import sys
from pathlib import Path

import httpx
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from frontend.components.dashboard import render_dashboard
from frontend.components.task_form import render_task_form
from frontend.components.task_table import render_task_table
from frontend.components.sidebar import render_sidebar
from frontend.components.charts import render_charts

BACKEND_URL = os.getenv('SMARTFLOW_BACKEND_URL', 'http://localhost:8000')


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def request(self, method, path, params=None, payload=None):
        response = httpx.request(method, f'{self.base_url}{path}', params=params, json=payload, timeout=20)
        if response.status_code == 204:
            return None
        if response.is_error:
            raise RuntimeError(response.text)
        try:
            return response.json()
        except ValueError:
            return response.text

    def get(self, path, params=None):
        return self.request('GET', path, params=params)

    def post(self, path, payload):
        return self.request('POST', path, payload=payload)

    def put(self, path, payload):
        return self.request('PUT', path, payload=payload)

    def patch(self, path, payload):
        return self.request('PATCH', path, payload=payload)

    def delete(self, path):
        return self.request('DELETE', path)


def load_css():
    css_path = Path(__file__).resolve().parent / 'styles' / 'custom.css'
    css = css_path.read_text(encoding='utf-8')
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


def render_priorities():
    st.title('Smart Priorities')
    st.caption('Transparent, rule-based recommendations for the next best task to work on.')
    try:
        tasks = st.session_state['api_client'].get('/api/tasks/prioritized') or []
    except Exception as exc:
        st.error(f'Unable to load priorities: {exc}')
        return

    if not tasks:
        st.info('No active tasks available for prioritization.')
        return

    for index, task in enumerate(tasks, start=1):
        st.markdown(f"<div class='card'><h4>#{index} {task.get('title', 'Untitled task')}</h4></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric('Priority score', task.get('priority_score', 0))
        col2.metric('Category', task.get('priority_category', 'Low'))
        col3.metric('Suggested rank', task.get('suggested_rank', index))
        st.write(task.get('priority_explanation', 'No explanation available.'))
        st.caption(f"Due: {task.get('due_date', 'Not set')} | Status: {task.get('status', 'Pending')}")
        st.markdown('---')


def render_deadline_monitoring():
    st.title('Deadline Monitoring')
    st.caption('Upcoming, due-today, and overdue tasks are highlighted here.')
    try:
        overdue = st.session_state['api_client'].get('/api/tasks/overdue') or []
        due_soon = st.session_state['api_client'].get('/api/tasks/due-soon') or []
    except Exception as exc:
        st.error(f'Unable to load deadline data: {exc}')
        return

    st.subheader('Overdue')
    if not overdue:
        st.success('No overdue tasks.')
    else:
        for task in overdue:
            st.warning(f"{task['title']} - due {task['due_date']}")

    st.subheader('Due soon')
    if not due_soon:
        st.info('No upcoming deadlines in the next 7 days.')
    else:
        for task in due_soon:
            st.info(f"{task['title']} - due {task['due_date']}")


def render_notifications():
    st.title('Notifications')
    st.caption('Read your in-app reminders and task alerts.')
    try:
        reminders = st.session_state['api_client'].get('/api/reminders') or []
    except Exception as exc:
        st.error(f'Unable to load reminders: {exc}')
        return

    if not reminders:
        st.info('No reminders yet.')
        return

    for reminder in reminders:
        is_unread = not reminder.get('is_read', False)
        if is_unread:
            st.warning(reminder['message'])
        else:
            st.info(reminder['message'])


def render_settings_page():
    st.title('Settings')
    try:
        current = st.session_state['api_client'].get('/api/settings')
    except Exception as exc:
        st.error(f'Unable to load settings: {exc}')
        return

    if not current:
        st.info('No settings found.')
        return

    with st.form('settings_form'):
        st.subheader('Priority weights')
        col1, col2 = st.columns(2)
        with col1:
            st.number_input('Importance Low', value=current.get('importance_low', 10), key='importance_low')
            st.number_input('Importance Medium', value=current.get('importance_medium', 25), key='importance_medium')
            st.number_input('Importance High', value=current.get('importance_high', 40), key='importance_high')
            st.number_input('Importance Critical', value=current.get('importance_critical', 50), key='importance_critical')
        with col2:
            st.number_input('Urgency Overdue', value=current.get('urgency_overdue', 50), key='urgency_overdue')
            st.number_input('Urgency Due Today', value=current.get('urgency_due_today', 45), key='urgency_due_today')
            st.number_input('Urgency Due Tomorrow', value=current.get('urgency_due_tomorrow', 35), key='urgency_due_tomorrow')
            st.number_input('Urgency Due Within 3 Days', value=current.get('urgency_due_3_days', 25), key='urgency_due_3_days')

        st.subheader('Scheduler preferences')
        col3, col4 = st.columns(2)
        with col3:
            st.number_input('Reminder Check Interval (minutes)', value=current.get('reminder_check_interval_minutes', 15), key='reminder_check_interval_minutes')
            st.number_input('Upcoming Reminder Window (days)', value=current.get('upcoming_deadline_reminder_days', 3), key='upcoming_deadline_reminder_days')
        with col4:
            st.number_input('Dashboard Refresh (seconds)', value=current.get('dashboard_refresh_seconds', 60), key='dashboard_refresh_seconds')

        submitted = st.form_submit_button('Save Settings', use_container_width=True)

    if submitted:
        payload = {
            'importance_low': st.session_state['importance_low'],
            'importance_medium': st.session_state['importance_medium'],
            'importance_high': st.session_state['importance_high'],
            'importance_critical': st.session_state['importance_critical'],
            'urgency_overdue': st.session_state['urgency_overdue'],
            'urgency_due_today': st.session_state['urgency_due_today'],
            'urgency_due_tomorrow': st.session_state['urgency_due_tomorrow'],
            'urgency_due_3_days': st.session_state['urgency_due_3_days'],
            'urgency_due_7_days': current.get('urgency_due_7_days', 15),
            'urgency_after_7_days': current.get('urgency_after_7_days', 5),
            'status_pending': current.get('status_pending', 10),
            'status_in_progress': current.get('status_in_progress', 5),
            'reminder_check_interval_minutes': st.session_state['reminder_check_interval_minutes'],
            'upcoming_deadline_reminder_days': st.session_state['upcoming_deadline_reminder_days'],
            'upcoming_deadline_reminder_enabled': current.get('upcoming_deadline_reminder_enabled', True),
            'overdue_reminder_enabled': current.get('overdue_reminder_enabled', True),
            'dashboard_refresh_seconds': st.session_state['dashboard_refresh_seconds'],
        }
        try:
            st.session_state['api_client'].put('/api/settings', payload)
            st.success('Settings updated successfully.')
        except Exception as exc:  # pragma: no cover
            st.error(f'Settings could not be saved: {exc}')


def render_about():
    st.title('About SMARTFLOW')
    st.markdown(
        """
        SMARTFLOW is an intelligent task management and workload optimization system designed for students, professionals, and small teams.

        It combines a FastAPI backend, SQLAlchemy ORM, SQLite data layer, and Streamlit dashboard to provide:
        - Task creation, updating, completion, and deletion
        - Rule-based priority scoring and workload recommendations
        - Deadline monitoring and overdue alerts
        - Productivity analytics and trend charts
        - In-app reminders and settings management
        """
    )


def render_productivity_page():
    st.title('Productivity Analytics')
    st.caption('Real data-driven performance insights from the SMARTFLOW database.')
    render_charts()


def main():
    st.set_page_config(page_title='SMARTFLOW', page_icon='✅', layout='wide')
    load_css()
    if 'api_client' not in st.session_state:
        st.session_state['api_client'] = ApiClient(BACKEND_URL)

    page = render_sidebar()
    page_key = page.replace('📊 ', '').replace('📋 ', '').replace('➕ ', '').replace('⚡ ', '').replace('⏰ ', '').replace('🔔 ', '').replace('📈 ', '').replace('⚙️ ', '').replace('ℹ️ ', '').strip()

    if page_key == 'Dashboard':
        render_dashboard()
    elif page_key == 'All Tasks':
        render_task_table()
    elif page_key == 'Create Task':
        render_task_form()
    elif page_key == 'Smart Priorities':
        render_priorities()
    elif page_key == 'Deadline Monitoring':
        render_deadline_monitoring()
    elif page_key == 'Notifications':
        render_notifications()
    elif page_key == 'Productivity Analytics':
        render_productivity_page()
    elif page_key == 'Settings':
        render_settings_page()
    elif page_key == 'About SMARTFLOW':
        render_about()


if __name__ == '__main__':
    main()
