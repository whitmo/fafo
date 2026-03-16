AGENT_SKILLS_DATA = [
    {
        "id": "skill_email",
        "document": "Sends an email to a specified recipient with a given subject and body.",
        "metadata": {
            "name": "send_email",
            "description": "Tool for sending emails.",
            "usage": "send_email(recipient, subject, body)"
        }
    },
    {
        "id": "skill_web_search",
        "document": "Performs a web search using a search engine and returns top results.",
        "metadata": {
            "name": "web_search",
            "description": "Tool for searching the internet.",
            "usage": "web_search(query)"
        }
    },
    {
        "id": "skill_write_file",
        "document": "Writes content to a specified file path on the local file system.",
        "metadata": {
            "name": "write_file",
            "description": "Tool for creating or modifying local files.",
            "usage": "write_file(file_path, content)"
        }
    },
    {
        "id": "skill_read_file",
        "document": "Reads and returns the content of a specified file from the local file system.",
        "metadata": {
            "name": "read_file",
            "description": "Tool for reading local files.",
            "usage": "read_file(file_path)"
        }
    },
    {
        "id": "skill_calendar_event",
        "document": "Creates a new event in the user's calendar with a given title, time, and attendees.",
        "metadata": {
            "name": "create_calendar_event",
            "description": "Tool for managing calendar events.",
            "usage": "create_calendar_event(title, time, attendees)"
        }
    },
    {
        "id": "skill_summarize",
        "document": "Summarizes a long piece of text or a document into a concise overview.",
        "metadata": {
            "name": "summarize_text",
            "description": "Tool for text summarization.",
            "usage": "summarize_text(text)"
        }
    }
]
