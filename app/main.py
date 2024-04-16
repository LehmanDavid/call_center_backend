from fastapi import FastAPI, HTTPException, Request
import os
from dotenv import load_dotenv
import uvicorn
import logging
from sqlalchemy.orm import Session
from prompts import construct_prompt
from agent import agent
import grpc
# import cloudapi.output.yandex.cloud.ai.stt.v3.stt_pb2 as stt_pb2
# import cloudapi.output.yandex.cloud.ai.stt.v3.stt_service_pb2_grpc as stt_service_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

folder_id = os.getenv("YANDEX_FOLDER_ID")


@app.get("/")
def read_root():
    try:
        query = 'Hey, tell me about youself'
        full_prompt = construct_prompt(query_str=query)
        agent_resp = agent.query(full_prompt)
        response_text = agent_resp.response
        return {"response": response_text}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# @app.post("/stream-recognize")
# async def stream_recognize(request: Request):
#     channel = get_stt_channel()
#     stub = stt_service_pb2_grpc.SttServiceStub(channel)
#     requests = generate_streaming_request(folder_id)
#     responses = stub.StreamingRecognize(requests)
#     async for response in responses:
#         for result in response.results:
#             for alternative in result.alternatives:
#                 print(alternative.text)
#     return {"status": "completed"}



# folder_id = os.getenv("YANDEX_FOLDER_ID")


# def get_stt_channel():
#     credentials = grpc.ssl_channel_credentials()
#     return grpc.secure_channel('stt.api.cloud.yandex.net:443', credentials)


# def generate_streaming_request(folder_id):
#     specification = stt_pb2.RecognitionSpec(
#         language_code='ru-RU',
#         model='general',
#         partial_results=True,
#         audio_encoding='LINEAR16_PCM',
#         sample_rate_hertz=8000
#     )
#     streaming_config = stt_pb2.RecognitionConfig(
#         specification=specification, folder_id=folder_id)
#     yield stt_pb2.StreamingRecognitionRequest(config=streaming_config)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
