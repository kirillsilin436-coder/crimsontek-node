import asyncio, websockets, json, os

USERS = {}

async def handle_client(websocket):
    my_id = None
    try:
        my_id = await websocket.recv()
        my_id = my_id.strip()
        USERS[my_id] = websocket
        print(f"[+] Node connected: {my_id}")
        
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            recipient = data.get("to")
            
            if action == "typing" and recipient in USERS:
                await USERS[recipient].send(json.dumps({"action": "is_typing", "from": my_id}))
            
            elif action == "send_msg":
                if recipient in USERS:
                    await USERS[recipient].send(json.dumps({
                        "action":"new_msg", "from":my_id, 
                        "text":data.get("text"), "type":data.get("type","text")
                    }))
    except: pass
    finally:
        if my_id in USERS: del USERS[my_id]

async def main():
    # Koyeb сам назначит порт через переменную PORT, по умолчанию 8080
    port = int(os.environ.get("PORT", 8080))
    async with websockets.serve(handle_client, "0.0.0.0", port):
        print(f"[*] CRIMSONTEK CLOUD ACTIVE ON PORT {port}")
        await asyncio.Future()

asyncio.run(main())