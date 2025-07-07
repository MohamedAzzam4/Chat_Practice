import os
import uvicorn
from dotenv import load_dotenv
import openai

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict

# --- 1. Initial Setup ---

load_dotenv()

app = FastAPI(
    title="Language Practice Tutor API",
    description="An API to practice languages with an AI tutor. This API is stateless.",
    version="1.0.2", # Incremented version
)

# --- 2. Setup OpenAI Client (DEFERRED) ---

# We no longer initialize the client here to prevent blocking app startup.
# The client will be initialized inside the endpoint that needs it.

API_KEY = os.getenv("ROUTER_API_KEY")

# --- 3. System Prompt Definition ---
the_chatter_prompt = """
Persona & Role Definition
You are Ahmed, a 23-year-old language tutor.

Your Persona:
Personality: You are calm, patient, and encouraging. Your tone is friendly and relaxed, like talking to a friend over coffee. You are not a formal teacher.
Interests: You love photography, hiking in nature, and trying new coffee shops. You can use these interests to start or guide conversations.
Goal: Your primary goal is to help the user practice their [{TARGET_LANGUAGE}] in a comfortable, low-pressure, and natural conversation. Building the user's confidence is more important than achieving perfection.

Core Instructions & Rules of Engagement
1. Response Style: Short, Simple, and Conversational
Keep your replies brief and to the point. Avoid long paragraphs or complex explanations.
Focus on maintaining a natural, back-and-forth conversational flow. Ask questions to keep the conversation moving.

2. Correction Policy (Crucial Rule):
Your default behavior is to correct the user's mistakes. Prioritize conversational flow and encouragement. You should only provide a correction or suggestion 


3. Language Adaptation Based on User Level:
You must adapt your language to the user's stated proficiency level: [{USER_LEVEL}].
For Beginners (A1-A2): Use very simple sentences and common vocabulary. Be very encouraging. The main goal is to make them feel comfortable speaking.
for Intermediate (B1-B2): Use natural, everyday language. You can occasionally introduce a common idiom or expression, but always keep the conversation flowing smoothly.
For Advanced (C1-C2): You can use more complex sentence structures and richer vocabulary, but always maintain the core principles of being conversational, brief, and encouraging.

Getting Started
Begin the very first interaction by introducing yourself as Ahmed and asking a simple, open-ended question related to your interests to start the chat.
"""
# --- 4. API Data Models ---

class ChatRequest(BaseModel):
    target_language: str
    user_level: str
    user_message: str
    chat_history: List[Dict[str, str]]

    class Config:
        json_schema_extra = {
            "example": {
                "target_language": "Spanish",
                "user_level": "B1",
                "user_message": "Hola, como estas?",
                "chat_history": []
            }
        }

class ChatResponse(BaseModel):
    tutor_response: str
    updated_chat_history: List[Dict[str, str]]

# --- 5. API Endpoint Definition ---
@app.get("/")
async def read_root():
    return {"message": "Welcome ;) Chat practicing For Turjuman is running.", "version": "1.0.2"}

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def handle_chat(request: ChatRequest):
    try:
        if not API_KEY:
            raise ValueError("ROUTER_API_KEY is not set.")

        # **FIXED**: Initialize the client inside the function
        client = openai.OpenAI(
            api_key=API_KEY,
            base_url="https://router.requesty.ai/v1"
        )
        
        current_history = list(request.chat_history)

        if not current_history:
            formatted_prompt = the_chatter_prompt.format(
                TARGET_LANGUAGE=request.target_language,
                USER_LEVEL=request.user_level
            )
            current_history.append({"role": "system", "content": formatted_prompt})

        current_history.append({"role": "user", "content": request.user_message})

        response = client.chat.completions.create(
            model='openai/gpt-4o-mini',
            messages=current_history
        )
        
        if not response.choices:
            raise Exception("No response choices found from the model.")

        llm_response_content = response.choices[0].message.content
        current_history.append({"role": "assistant", "content": llm_response_content})

        return ChatResponse(
            tutor_response=llm_response_content,
            updated_chat_history=current_history
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(e) or "An internal server error occurred."}
        )

# --- 6. Application Runner ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
```

### الخطوات التالية:

1.  **انسخ الكود المحدث** وقم باستبدال الكود القديم به.
2.  **قم بعمل deploy** للتغييرات على Railway.
3.  **بعد اكتمال النشر،** اختبر الأمر عن طريق زيارة الرابط الرئيسي أولاً: `https://your-app-name.up.railway.app/`. من المفترض الآن أن يعمل ويعرض لك رسالة الترحيب فورًا.
4.  إذا نجح ذلك، يمكنك اختبار وظيفة الدردشة الأساسية عبر إرسال طلب `POST` إلى `/cha
