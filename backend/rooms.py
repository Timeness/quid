class RoomManager:
    def __init__(self):
        self.active_rooms = {}

    def create_room(self, room_id):
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = []

    async def connect(self, room_id, websocket):
        await websocket.accept()
        if room_id in self.active_rooms:
            self.active_rooms[room_id].append(websocket)
        else:
            self.active_rooms[room_id] = [websocket]

    def disconnect(self, room_id, websocket):
        self.active_rooms[room_id].remove(websocket)

    async def send_to_room(self, room_id, message):
        if room_id in self.active_rooms:
            for ws in self.active_rooms[room_id]:
                await ws.send_json(message)

    def end_room(self, room_id):
        if room_id in self.active_rooms:
            del self.active_rooms[room_id]
