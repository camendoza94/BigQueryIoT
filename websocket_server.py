import asyncio
import websockets

async def data(websocket, path):
    data = await websocket.recv()
    print(f"< {data}")

start_server = websockets.serve(data, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()