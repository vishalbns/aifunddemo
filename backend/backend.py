from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import re
import motor.motor_asyncio  # Async MongoDB driver
from dotenv import load_dotenv

load_dotenv()  # This loads variables from .env into os.environ

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup - replace <your_mongo_uri> with your actual MongoDB connection string
MONGO_DETAILS = os.getenv("MONGO_URI")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = mongo_client.haiku_db
haiku_collection = db.get_collection("haikus")

class HaikuRequest(BaseModel):
    elements: str

def sanitize_filename(text: str) -> str:
    return re.sub(r'[^\w\- ]', '', text).strip().replace(" ", "_")

async def save_haiku_to_db(filename: str, haiku_text: str):
    haiku_doc = {
        "filename": filename,
        "haiku": haiku_text
    }
    await haiku_collection.insert_one(haiku_doc)

def generate_haiku(elements: str) -> str:
    prompt = f"""You are a haiku poet. Write a 3-line haiku (5-7-5 syllable structure) based on the following elements: {elements}.
Follow the traditional haiku form: three lines, with seasonal or emotional imagery."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

@app.post("/generate-haiku/")
async def create_haiku(req: HaikuRequest):
    try:
        haiku = generate_haiku(req.elements)
        filename = sanitize_filename(req.elements)
        await save_haiku_to_db(filename, haiku)
        return {"filename": filename, "haiku": haiku}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi.responses import JSONResponse

@app.get("/haikus/")
async def get_all_haikus():
    haikus_cursor = haiku_collection.find({})
    haikus = []
    async for doc in haikus_cursor:
        haikus.append({"filename": doc.get("filename"), "haiku": doc.get("haiku")})
    return JSONResponse(content=haikus)
