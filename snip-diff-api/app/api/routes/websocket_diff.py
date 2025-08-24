"""
WebSocket Live Diff Channel for SNIP-DIFF
Real-time diff updates with subscription management and heartbeat
"""
from __future__ import annotations

import asyncio
import json
import time
from typing import Dict, List, Set, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from dataclasses import dataclass, field

from app.core.watch.watch_service import WatchService, DiffEvent
from app.core.models.diff_types import FileDiff

router = APIRouter(prefix="/ws", tags=["websocket"])

@dataclass
class WebSocketConnection:
    """Active WebSocket connection with subscription state"""
    websocket: WebSocket
    client_id: str
    subscribed_paths: Set[str] = field(default_factory=set)
    last_ping: float = field(default_factory=time.time)
    last_seq: int = 0
    is_active: bool = True

class ConnectionManager:
    """WebSocket connection manager with subscription handling"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocketConnection] = {}
        self.watch_service = WatchService()
        self.heartbeat_interval = 30  # 30 seconds
        self.max_connections = 50     # Configurable connection limit
        self.sequence_counter = 0
        self.heartbeat_task: Optional[asyncio.Task] = None
        
        # Register as event listener for file changes
        self.watch_service.add_event_listener(self._on_diff_event)
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept new WebSocket connection"""
        if len(self.active_connections) >= self.max_connections:
            await websocket.close(code=1013, reason="Too many connections")
            return False
        
        await websocket.accept()
        connection = WebSocketConnection(websocket=websocket, client_id=client_id)
        self.active_connections[client_id] = connection
        
        # Start heartbeat if first connection
        if len(self.active_connections) == 1 and not self.heartbeat_task:
            self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        print(f"WebSocket client {client_id} connected. Total: {len(self.active_connections)}")
        return True
    
    def disconnect(self, client_id: str):
        """Remove connection"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"WebSocket client {client_id} disconnected. Total: {len(self.active_connections)}")
        
        # Stop heartbeat if no connections
        if len(self.active_connections) == 0 and self.heartbeat_task:
            self.heartbeat_task.cancel()
            self.heartbeat_task = None
    
    async def subscribe(self, client_id: str, paths: List[str]):
        """Subscribe client to file paths"""
        if client_id not in self.active_connections:
            return False
        
        connection = self.active_connections[client_id]
        connection.subscribed_paths.update(paths)
        
        # Send confirmation
        message = {
            "type": "subscription_confirmed",
            "paths": list(connection.subscribed_paths),
            "timestamp": time.time()
        }
        await self._send_to_connection(connection, message)
        print(f"Client {client_id} subscribed to {len(paths)} paths")
        return True
    
    async def unsubscribe(self, client_id: str, paths: List[str]):
        """Unsubscribe client from file paths"""
        if client_id not in self.active_connections:
            return False
        
        connection = self.active_connections[client_id]
        for path in paths:
            connection.subscribed_paths.discard(path)
        
        message = {
            "type": "subscription_updated",
            "paths": list(connection.subscribed_paths),
            "timestamp": time.time()
        }
        await self._send_to_connection(connection, message)
        return True
    
    async def broadcast_diff_event(self, event: DiffEvent):
        """Broadcast diff event to subscribed clients"""
        if not self.active_connections:
            return
        
        self.sequence_counter += 1
        
        # Build event message
        message = {
            "type": "file_diff",
            "seq": self.sequence_counter,
            "path": event.file_path,
            "change_type": event.change_type.value,
            "timestamp": event.timestamp,
            "modes": {}
        }
        
        # Include diff data if available
        if event.file_diff:
            # Convert to serializable format
            from app.api.routes.live_diff import _build_api_file_diff
            api_diff = _build_api_file_diff(event.file_diff)
            message["diff"] = api_diff.dict()
            message["modes"] = event.file_diff.modes
        
        # Send to subscribed clients
        tasks = []
        for connection in self.active_connections.values():
            if event.file_path in connection.subscribed_paths or not connection.subscribed_paths:
                # Send to all clients or those specifically subscribed to this path
                tasks.append(self._send_to_connection(connection, message))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _send_to_connection(self, connection: WebSocketConnection, message: dict):
        """Send message to specific connection with error handling"""
        try:
            if connection.is_active:
                await connection.websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error sending to client {connection.client_id}: {e}")
            connection.is_active = False
            # Mark for cleanup
            self.disconnect(connection.client_id)
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeat pings to all connections"""
        while self.active_connections:
            try:
                current_time = time.time()
                tasks = []
                
                for connection in list(self.active_connections.values()):
                    if current_time - connection.last_ping > self.heartbeat_interval:
                        ping_message = {
                            "type": "ping",
                            "timestamp": current_time,
                            "seq": self.sequence_counter
                        }
                        tasks.append(self._send_ping(connection, ping_message))
                
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                await asyncio.sleep(self.heartbeat_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in heartbeat loop: {e}")
                await asyncio.sleep(5)  # Brief pause before retry
    
    async def _send_ping(self, connection: WebSocketConnection, ping_message: dict):
        """Send ping and update last ping time"""
        await self._send_to_connection(connection, ping_message)
        connection.last_ping = time.time()
    
    def _on_diff_event(self, event: DiffEvent):
        """Handle diff event from watch service"""
        # Use asyncio.create_task only if we're in an event loop context
        if self.active_connections:
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.broadcast_diff_event(event))
            except RuntimeError:
                # No running loop - store event for later processing
                # This can happen during startup/shutdown
                pass
    
    def get_stats(self) -> dict:
        """Get connection manager statistics"""
        return {
            "active_connections": len(self.active_connections),
            "max_connections": self.max_connections,
            "sequence_counter": self.sequence_counter,
            "heartbeat_interval": self.heartbeat_interval,
            "total_subscriptions": sum(len(conn.subscribed_paths) for conn in self.active_connections.values())
        }

# Global connection manager
connection_manager = ConnectionManager()

@router.websocket("/diff")
async def websocket_diff_endpoint(websocket: WebSocket, client_id: str = Query(...)):
    """
    WebSocket endpoint for live diff updates
    
    Message formats:
    - Client -> Server: {"action": "subscribe", "paths": ["/path/to/file"]}
    - Client -> Server: {"action": "unsubscribe", "paths": ["/path/to/file"]}
    - Client -> Server: {"action": "pong", "timestamp": 1234567890}
    - Server -> Client: {"type": "file_diff", "seq": 123, "path": "...", "diff": {...}}
    - Server -> Client: {"type": "ping", "timestamp": 1234567890, "seq": 123}
    - Server -> Client: {"type": "subscription_confirmed", "paths": [...]}
    """
    
    # Attempt connection
    connected = await connection_manager.connect(websocket, client_id)
    if not connected:
        return
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                action = message.get("action")
                
                if action == "subscribe":
                    paths = message.get("paths", [])
                    await connection_manager.subscribe(client_id, paths)
                    
                elif action == "unsubscribe":
                    paths = message.get("paths", [])
                    await connection_manager.unsubscribe(client_id, paths)
                    
                elif action == "pong":
                    # Client responded to ping
                    if client_id in connection_manager.active_connections:
                        connection_manager.active_connections[client_id].last_ping = time.time()
                    
                else:
                    # Unknown action - send error
                    error_msg = {
                        "type": "error",
                        "message": f"Unknown action: {action}",
                        "timestamp": time.time()
                    }
                    await websocket.send_text(json.dumps(error_msg))
                    
            except json.JSONDecodeError:
                error_msg = {
                    "type": "error",
                    "message": "Invalid JSON format",
                    "timestamp": time.time()
                }
                await websocket.send_text(json.dumps(error_msg))
                
    except WebSocketDisconnect:
        connection_manager.disconnect(client_id)
    except Exception as e:
        print(f"WebSocket error for client {client_id}: {e}")
        connection_manager.disconnect(client_id)

@router.get("/diff/stats")
async def websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        "websocket_stats": connection_manager.get_stats(),
        "watch_service_stats": connection_manager.watch_service.get_stats()
    }

# Health check for WebSocket
@router.get("/diff/health")
async def websocket_health():
    """WebSocket service health check"""
    return {
        "status": "healthy",
        "active_connections": len(connection_manager.active_connections),
        "max_connections": connection_manager.max_connections
    }
