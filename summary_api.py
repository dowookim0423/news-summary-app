from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import openai

# .env 파일에서 API 키 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# 요청 바디 모델 정의
class TextRequest(BaseModel):
    text: str

@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # GPT-3.5 모델 지정
            messages=[
                {"role": "system", "content": "You are a helpful assistant who summarizes texts briefly."},
                {"role": "user", "content": f"Summarize the following text:\n\n{request.text}"}
            ],
            max_tokens=150,
            temperature=0.5,
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sentiment")
async def sentiment_analysis(request: TextRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who analyzes sentiment of texts."},
                {"role": "user", "content": f"Analyze the sentiment (positive, negative, or neutral) of the following text:\n\n{request.text}"}
            ],
            max_tokens=50,
            temperature=0.3,
        )
        sentiment = response.choices[0].message.content.strip()
        return {"sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
