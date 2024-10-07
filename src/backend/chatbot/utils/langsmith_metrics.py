from langsmith import Langsmith

langsmith_client = Langsmith(project_name="chatbot_project")

def log_event(event_data):
    """
    Ghi lại sự kiện vào LangSmith.
    """
    langsmith_client.log_event(event_data)