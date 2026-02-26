import socketio

# --- CONFIGURACIÓN SOCKET.IO ---
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*') 


@sio.event
async def connect(sid, environ):
    
    # Esta función recibe sid y environ automáticamente
    print(f"✅ Cliente conectado: {sid}")
    
    # Si querías enviar el "HOLAAA", hazlo aquí:
    await sio.emit('response', {'data': 'HOLAAA'}, to=sid)
    print("PUPU")
    
    
@sio.event
async def disconnect(sid):
    print(f"❌ Cliente desconectado: {sid}")

