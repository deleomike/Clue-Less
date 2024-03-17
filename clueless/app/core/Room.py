class Room:
  def __init__(self, room_id):
    self.room = room_id
    self.connections = []

  async def broadcast(self, message, sender):
    for connection in self.connections:
      print(message)
      await connection.send_text(message)