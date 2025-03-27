from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os
import base64
from pathlib import Path

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
    optimized_prompt = prompt.prompt + " ------ this is optimized"
    return {"optimized_prompt": optimized_prompt}



@app.post("/generate-image/")
def generate_image(request: ImageRequest):
    # Placeholder for image generation logic
    # Define the path to the image
    # Define the path to the image directory
    image_dir = Path("image")

    # Find the first image file in the directory (supports png and jpg)
    # Find the first image file in the directory (supports png, jpg, and jpeg)
    image_file = next(image_dir.glob("*.png"), None) or \
                 next(image_dir.glob("*.jpg"), None) or \
                 next(image_dir.glob("*.jpeg"), None)

    # Read the image file in binary mode
    if image_file and image_file.exists():
        with open(image_file, "rb") as file:
            # Encode the image to base64
            encoded_image = base64.b64encode(file.read()).decode("utf-8")
        return {"image_base64": f"data:image/{image_file.suffix[1:]};base64,{encoded_image}", "prompt": request.text}
    else:
        return {"error": "No image file found", "prompt": request.text}


# 指定图片名称，传给后端
@app.post("/generateoptimize-image/")
def generate_targetImage(request: ImageRequest):
    # Define the specific image file path
    image_path = Path("image/0a13212000b8l4oja7216.png")

    # Read the image file in binary mode
    if image_path.exists():
        with open(image_path, "rb") as file:
            # Encode the image to base64
            encoded_image = base64.b64encode(file.read()).decode("utf-8")
        return {"image_base64": f"data:image/{image_path.suffix[1:]};base64,{encoded_image}", "prompt": request.text}
    else:
        return {"error": f"Image file {image_path.name} not found", "prompt": request.text}

