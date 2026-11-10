import streamlit as st


def _importance_class(value):
    return {
        'Low': 'priority-low',
        'Medium': 'priority-medium',
        'High': 'priority-high',
        'Critical': 'priority-critical',
    }.get(value, 'priority-medium')


def render_task_table():
    st.title('All Tasks')
    st.caption('Search, filter, complete, and manage your task list.')

    search = st.text_input('Search by title', placeholder='Search tasks...')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        status_filter = st.selectbox('Filter by status', ['All', 'Pending', 'In Progress', 'Completed'])
    with col2:
        importance_filter = st.selectbox('Filter by importance', ['All', 'Low', 'Medium', 'High', 'Critical'])
    with col3:
        overdue_only = st.checkbox('Overdue only')

    params = {}
    if search:
        params['search'] = search
    if status_filter != 'All':
        params['status'] = status_filter
    if importance_filter != 'All':
        params['importance'] = importance_filter
    if overdue_only:
        params['overdue_only'] = 'true'

    try:
        tasks = st.session_state['api_client'].get('/api/tasks', params=params)
    except Exception as exc:
        st.error(f'Unable to load tasks: {exc}')
        return

    if not tasks:
        st.info('No tasks match your filters.')
        return

    for task in tasks:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            head_cols = st.columns([3, 1, 1, 1, 1])
            head_cols[0].markdown(f"### {task['title']}")
            head_cols[1].markdown(f"<span class='status-pill { _importance_class(task.get('importance', 'Medium')) }'>{task.get('importance', 'Medium')}</span>", unsafe_allow_html=True)
            head_cols[2].markdown(f"**Status:** {task.get('status', 'Pending')}")
            head_cols[3].markdown(f"**Priority:** {task.get('priority_score', 0)}")
            head_cols[4].markdown(f"**Rank:** {task.get('suggested_rank', 0)}")

            body_cols = st.columns([2, 2, 1.2, 1.2])
            body_cols[0].write(f"**Due:** {task.get('due_date', 'Not set')}")
            body_cols[1].write(f"**Description:** {task.get('description', 'No description') or 'No description'}")
            body_cols[2].write(f"**Category:** {task.get('priority_category', 'Low')}")
            body_cols[3].write(f"**Explanation:** {task.get('priority_explanation', 'No explanation available.')}")

            action_cols = st.columns([1, 1, 1])
            if action_cols[0].button(f"Complete #{task['id']}", key=f"complete_{task['id']}"):
                try:
                    response = st.session_state['api_client'].patch(f"/api/tasks/{task['id']}/complete", {})
                    if isinstance(response, dict) and response.get('id'):
                        st.success('Task marked as completed.')
                        st.rerun()
                    else:
                        st.error('Completion action did not return a valid task.')
                except Exception as exc:
                    st.error(f'Unable to complete task: {exc}')

            if action_cols[1].button(f"Delete #{task['id']}", key=f"delete_{task['id']}"):
                try:
                    response = st.session_state['api_client'].delete(f"/api/tasks/{task['id']}")
                    if response is None:
                        st.success('Task deleted successfully.')
                        st.rerun()
                    else:
                        st.warning('Delete request returned an unexpected response.')
                except Exception as exc:
                    st.error(f'Unable to delete task: {exc}')

            if action_cols[2].button(f"View #{task['id']}", key=f"view_{task['id']}"):
                st.info(f"Task ID: {task['id']} | Due: {task.get('due_date', 'Not set')}")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('---')
