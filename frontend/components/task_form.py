from datetime import datetime

import streamlit as st


def render_task_form():
    st.title('Create Task')
    st.caption('Capture a new assignment, project, or priority item.')

    with st.form('create_task_form'):
        title = st.text_input('Task Title', placeholder='E.g. Finalize capstone report')
        description = st.text_area('Description', placeholder='Add task details, objectives, or notes...')
        due_date = st.datetime_input('Due Date and Time', value=datetime.now())
        importance = st.selectbox('Importance', ['Low', 'Medium', 'High', 'Critical'])
        status = st.selectbox('Status', ['Pending', 'In Progress', 'Completed'])
        estimated_duration = st.number_input('Estimated Duration (hours)', min_value=0, max_value=1000, value=0)
        submitted = st.form_submit_button('Save Task', use_container_width=True)

    if submitted:
        if not title.strip():
            st.error('Task title is required.')
            return
        payload = {
            'title': title.strip(),
            'description': description.strip() or None,
            'due_date': due_date.isoformat(),
            'importance': importance,
            'status': status,
            'estimated_duration': int(estimated_duration),
        }
        try:
            response = st.session_state['api_client'].post('/api/tasks', payload)
            if isinstance(response, dict) and response.get('id'):
                st.success(f"Task '{response.get('title')}' created successfully.")
                st.rerun()
            else:
                st.error('Unable to create task. Check the input and try again.')
        except Exception as exc:  # pragma: no cover
            st.error(f'Failed to create task: {exc}')
