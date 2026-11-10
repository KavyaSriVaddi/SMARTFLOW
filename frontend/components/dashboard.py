import streamlit as st

from frontend.components.charts import render_charts


def render_dashboard():
    st.title('SMARTFLOW Dashboard')
    st.caption('Workload overview and productivity snapshot')
    try:
        summary = st.session_state['api_client'].get('/api/analytics/summary')
        if not summary:
            st.info('No tasks yet. Add your first task to populate the dashboard.')
            return

        metrics = [
            ('Total Tasks', summary.get('total_tasks', 0), 'Overall task load'),
            ('Completed', summary.get('completed_tasks', 0), 'Finished work'),
            ('Pending', summary.get('pending_tasks', 0), 'Awaiting action'),
            ('In Progress', summary.get('in_progress_tasks', 0), 'Currently active'),
            ('Overdue', summary.get('overdue_tasks', 0), 'Needs attention'),
            ('Completion Rate', f"{summary.get('completion_rate', 0)}%", 'Delivery momentum'),
        ]

        cols = st.columns(6)
        for col, (label, value, help_text) in zip(cols, metrics):
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.metric(label, value)
                st.caption(help_text)
                st.markdown('</div>', unsafe_allow_html=True)

    except Exception as exc:  # pragma: no cover
        st.error(f'Unable to load dashboard metrics: {exc}')

    render_charts()
