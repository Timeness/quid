from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.music import download_audio
from backend.rooms import RoomManager
import uvicorn

app = FastAPI()
manager = RoomManager()

@app.post("/create_room/{room_id}")
async def create_room(room_id: int):
    manager.create_room(room_id)
    return {"status": "room created"}

@app.post("/play_song/{room_id}")
async def play_song(room_id: int, query: str):
    file_path, title = await download_audio(query)
    await manager.send_to_room(room_id, {"action": "play", "file_path": file_path, "title": title})
    return {"status": "playing", "title": title}

@app.post("/end_room/{room_id}")
async def end_room(room_id: int):
    manager.end_room(room_id)
    return {"status": "room ended"}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    await manager.connect(room_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
