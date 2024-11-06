import requests
import json

def generate_summary(student):
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""
    Generate a JSON-formatted student summary with the following fields:
    - "Student Summary": A brief description of the student in 30 words or less.You are free to include data using age and email domain.
    - "Email": The student's email.
    
    Here’s the data for the student:
    Name: {student.name}
    Age: {student.age}
    Email: {student.email}
    
    Example output:
    {{
        "Student Summary": "{student.name} is a {student.age}-year-old student with interests in ... You can reach .. email ... {student.email}.",
        "Email": "{student.email}"
    }}
    Please follow this JSON structure precisely.
    """
    
    payload = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "format": "json",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            summary = response.json()
            # print(summary.get("response", {}))
            if isinstance(summary.get("response"), str):
                summary_data = json.loads(summary["response"])
                summary_text = summary_data.get("Student Summary", "")
            else:
                summary_text = summary.get("response", {}).get("Student Summary", "")
            return summary_text
        else:
            return f"Error: Unable to generate summary (status code {response.status_code})"
    
    except requests.RequestException as e:
        return f"Request failed: {e}"
