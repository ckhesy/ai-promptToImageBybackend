from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

app = FastAPI()
class Prompt(BaseModel):
    prompt: str

class ImageRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/optimize-prompt/")
def optimize_prompt(prompt: Prompt):
    optimized_prompt = prompt.prompt + " optimized"
    return {"optimized_prompt": optimized_prompt}



@app.post("/generate-image/")
def generate_image(request: ImageRequest):
    # Placeholder for image generation logic
    image_url = "https://dimg04.tripcdn.com/images/0a13i12000e8gmk5hDC23.jpg"
    return {"image_url": image_url, "prompt": request.text}


