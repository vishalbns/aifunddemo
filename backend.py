from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import re
import motor.motor_asyncio
from dotenv import load_dotenv

# Load environment variables from .env
#load_dotenv()

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Initialize FastAPI app
app = FastAPI()

# CORS for frontend access - update origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = mongo_client.haiku_db
haiku_collection = db.haikus

# Request schema
class HaikuRequest(BaseModel):
    elements: str

# Utility to sanitize filename
def sanitize_filename(text: str) -> str:
    return re.sub(r'[^\w\- ]', '', text).strip().replace(" ", "_")

# Generate haiku from OpenAI
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

# Save to MongoDB
async def save_haiku_to_db(filename: str, haiku: str):
    await haiku_collection.insert_one({"filename": filename, "haiku": haiku})

# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "Haiku Generator API is running!"}

# POST /generate-haiku/
@app.post("/generate-haiku/")
async def create_haiku(req: HaikuRequest):
    try:
        haiku = generate_haiku(req.elements)
        filename = sanitize_filename(req.elements)
        await save_haiku_to_db(filename, haiku)
        return {"filename": filename, "haiku": haiku}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET /haikus/
@app.get("/haikus/")
async def get_all_haikus():
    try:
        cursor = haiku_collection.find({})
        results = []
        async for doc in cursor:
            results.append({"filename": doc.get("filename"), "haiku": doc.get("haiku")})
        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
