from fastapi import FastAPI, HTTPException, Request
import os
from dotenv import load_dotenv
import uvicorn
import logging
from sqlalchemy.orm import Session
from prompts import construct_prompt
from agent import agent
import grpc
from speechkit import DataStreamingRecognition, Session
from speechkit.auth import generate_jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

api_key = os.getenv('YANDEX_API_KEY')

session = Session.from_api_key(api_key)
data_streaming_recognition = DataStreamingRecognition(
    session,
    language_code='ru-RU',
    audio_encoding='LINEAR16_PCM',
    sample_rate_hertz=8000,
    partial_results=True,
    single_utterance=False,
)


@app.get("/")
def read_root():
    try:
        query = 'Hey, tell me about youself'
        full_prompt = construct_prompt(query_str=query)
        # agent_resp = agent.query(full_prompt)
        # response_text = agent_resp.response
        return {"response": 'working'}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/stream-recognize")
async def stream_recognize(request: Request):

    async def audio_generator():
        async for chunk in request.stream():
            if chunk:
                yield chunk
            else:
                break

    try:
        recognition_iterator = data_streaming_recognition.recognize(
            audio_generator(), chunk_size=4000
        )

        results = []
        async for text, final, end_of_utterance in recognition_iterator:
            if text:
                results.append(text[0])
            if final:
                break

        return {"status": "completed", "transcription": results}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
