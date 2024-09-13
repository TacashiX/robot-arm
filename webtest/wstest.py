import asyncio
import websockets

curr = [0,0,0,0,0,0,0]

async def handler(websocket, path):
    update_task = asyncio.create_task(update(websocket))
    receive_task = asyncio.create_task(receive(websocket))
    await asyncio.wait([ update_task, receive_task], return_when=asyncio.FIRST_COMPLETED)


async def receive(websocket):
    global curr
    async for message in websocket:
        curr = [ float(x) for x in message.split(",")]
        print(f"Received: {message}")

async def update(websocket):
    global curr 
    while True: 
        await websocket.send(f"Current trigger: {curr[4]}")
        await asyncio.sleep(1/500)

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

