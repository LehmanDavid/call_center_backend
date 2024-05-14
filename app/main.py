from fastapi import FastAPI, HTTPException, Request
import os
from dotenv import load_dotenv
import uvicorn
import logging
from prompts import construct_prompt
from agent import agent
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()


@app.post("/get-response")
def read_root(query: str):
    try:
        start_time = time.time()
        full_prompt = construct_prompt(query_str=query)
        agent_resp = agent.query(full_prompt)        
        response_text = agent_resp.response
        end_time = time.time()
        logger.info(f"Response time: {end_time - start_time}")
        return {"response": response_text}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
