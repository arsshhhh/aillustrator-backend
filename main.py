from fastapi import FastAPI
from agent import agent
from models import GenerateRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aillustrator-frontend.vercel.app"
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Normal JSON response (unchanged)
@app.post("/generate")
async def generate(req: GenerateRequest):
    try:
        result = await agent.run(req.prompt)

        return {
            "success": True,
            "data": {
                "output": result
            },
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


# ✅ Streaming generator
# async def stream_notes(prompt: str) -> AsyncGenerator[str, None]:
#     async with agent.run_stream(prompt) as result:
#         async for chunk in result.stream_text():
#             yield chunk

from typing import AsyncGenerator

async def stream_notes(prompt: str) -> AsyncGenerator[str, None]:
    async with agent.run_stream(prompt) as result:
        async for chunk in result.stream_text():
            for char in chunk:
                yield char
                await asyncio.sleep(0.008)  # controls typing speed


# ✅ Streaming endpoint
@app.post("/generate-stream")
async def generate_stream(req: GenerateRequest):
    return StreamingResponse(
        stream_notes(req.prompt),
        media_type="text/plain"
    )