import json
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from google import genai
from total_todo.total_todo_dto import TodoRequest
from dotenv import load_dotenv

load_dotenv()

with open("todos/ai/prompt.md", "r", encoding="utf-8") as f:
    prompt = f.read()

user_todo = TodoRequest(title="최종 기획안 작성", due_date="2026-09-01", due_time=None)

async def divide_and_submit(user_todo: TodoRequest):
    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()

    client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_KEY"))

    final_prompt = prompt.replace("{{CURRENT_DATE}}", str(current_date)).replace("{{CURRENT_TIME}}", str(current_time))

    response = await client.interactions.create(
        model="gemini-3.5-flash",
        system_instruction=final_prompt,
        input=user_todo.model_dump_json()
    )

    return json.loads(response.output_text)