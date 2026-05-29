from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.ticker_subscriptions: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, ticker: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        if ticker not in self.ticker_subscriptions:
            self.ticker_subscriptions[ticker] = []
        self.ticker_subscriptions[ticker].append(websocket)

    def disconnect(self, websocket: WebSocket, ticker: str):
        self.active_connections.remove(websocket)
        if ticker in self.ticker_subscriptions and websocket in self.ticker_subscriptions[ticker]:
            self.ticker_subscriptions[ticker].remove(websocket)

    async def broadcast_to_ticker(self, ticker: str, message: dict):
        if ticker in self.ticker_subscriptions:
            for connection in self.ticker_subscriptions[ticker]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{ticker}")
async def websocket_endpoint(websocket: WebSocket, ticker: str):
    await manager.connect(websocket, ticker)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket data if needed
            await manager.broadcast_to_ticker(ticker, {"message": f"Server received: {data}"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, ticker)
