from fastapi import FastAPI, Body
from starlette.responses import FileResponse, StreamingResponse
from ollama import Client

app = FastAPI()
ai  = Client(host='http://ollama:11434')

@app.get("/")
async def read_index():
    return FileResponse('/app/index.html')


@app.post("/define")
async def define(request = Body()):
    try:
        return StreamingResponse(
            response_generator(request['term']),
            media_type="text/event-stream",
        )
    except:
        return 'Type something'

def response_generator(message):
    stream = ai.chat(
        model='llama3.1',
        messages=[
            {'role': 'system', 'content': 'You are just an example of ollama deployment. Be concise.'},
            {'role': 'user', 'content': message}
        ],
        stream=True,
    )
    for chunk in stream:
        yield chunk['message']['content']
