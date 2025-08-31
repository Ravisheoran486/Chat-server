import asyncio
import json
import logging
import os
from datetime import datetime
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store connected clients with their usernames
connected_clients = {}  # {websocket: username}

async def handle_client(websocket):
    """Handle individual client connections"""
    client_id = id(websocket)
    username = None
    
    logger.info(f"Client {client_id} connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            try:
                # Try to parse as JSON first
                try:
                    data = json.loads(message)
                    logger.info(f"Received JSON from client {client_id}: {data}")
                    
                    # Handle different message types
                    if isinstance(data, dict):
                        msg_type = data.get('type', '')
                        
                        if msg_type == 'login':
                            # Handle user login
                            username = data.get('username', f'User_{client_id}')
                            connected_clients[websocket] = username
                            
                            # Send login confirmation
                            response = {
                                'type': 'login_success',
                                'username': username,
                                'message': f'Welcome {username}!',
                                'timestamp': datetime.now().isoformat()
                            }
                            await websocket.send(json.dumps(response))
                            
                            # Notify other clients about new user
                            await broadcast_to_others(websocket, {
                                'type': 'user_joined',
                                'username': username,
                                'message': f'{username} joined the chat',
                                'timestamp': datetime.now().isoformat()
                            })
                            
                            # Send current users list
                            users_list = list(connected_clients.values())
                            await websocket.send(json.dumps({
                                'type': 'users_list',
                                'users': users_list,
                                'timestamp': datetime.now().isoformat()
                            }))
                            
                        elif msg_type == 'chat':
                            # Handle chat message
                            if username:
                                chat_message = data.get('message', '')
                                await broadcast_to_all({
                                    'type': 'chat',
                                    'username': username,
                                    'message': chat_message,
                                    'timestamp': datetime.now().isoformat()
                                })
                            else:
                                await websocket.send(json.dumps({
                                    'type': 'error',
                                    'message': 'Please login first',
                                    'timestamp': datetime.now().isoformat()
                                }))
                                
                        elif msg_type == 'private':
                            # Handle private message
                            if username:
                                target_username = data.get('to', '')
                                private_message = data.get('message', '')
                                
                                # Find target user
                                target_websocket = None
                                for ws, uname in connected_clients.items():
                                    if uname == target_username:
                                        target_websocket = ws
                                        break
                                
                                if target_websocket:
                                    # Send to target user
                                    await target_websocket.send(json.dumps({
                                        'type': 'private',
                                        'from': username,
                                        'message': private_message,
                                        'timestamp': datetime.now().isoformat()
                                    }))
                                    
                                    # Send confirmation to sender
                                    await websocket.send(json.dumps({
                                        'type': 'private_sent',
                                        'to': target_username,
                                        'message': private_message,
                                        'timestamp': datetime.now().isoformat()
                                    }))
                                else:
                                    await websocket.send(json.dumps({
                                        'type': 'error',
                                        'message': f'User {target_username} not found',
                                        'timestamp': datetime.now().isoformat()
                                    }))
                            else:
                                await websocket.send(json.dumps({
                                    'type': 'error',
                                    'message': 'Please login first',
                                    'timestamp': datetime.now().isoformat()
                                }))
                                
                        elif msg_type == 'typing':
                            # Handle typing indicator
                            if username:
                                await broadcast_to_others(websocket, {
                                    'type': 'typing',
                                    'username': username,
                                    'is_typing': data.get('is_typing', True),
                                    'timestamp': datetime.now().isoformat()
                                })
                                
                        else:
                            # Unknown message type
                            response = {'type': 'error', 'message': f'Unknown message type: {msg_type}', 'timestamp': datetime.now().isoformat()}
                            await websocket.send(json.dumps(response))
                    
                except json.JSONDecodeError:
                    # Handle plain text messages as chat messages
                    if username:
                        await broadcast_to_all({
                            'type': 'chat',
                            'username': username,
                            'message': message,
                            'timestamp': datetime.now().isoformat()
                        })
                    else:
                        await websocket.send(json.dumps({
                            'type': 'error',
                            'message': 'Please login first. Send: {"type": "login", "username": "your_name"}',
                            'timestamp': datetime.now().isoformat()
                        }))
                    
            except Exception as e:
                logger.error(f"Error processing message from client {client_id}: {e}")
                error_response = {
                    'type': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                await websocket.send(json.dumps(error_response))
                
    except ConnectionClosed:
        logger.info(f"Client {client_id} disconnected normally")
    except Exception as e:
        logger.error(f"Error with client {client_id}: {e}")
    finally:
        # Cleanup when client disconnects
        if websocket in connected_clients:
            username = connected_clients[websocket]
            del connected_clients[websocket]
            
            # Notify other clients about user leaving
            await broadcast_to_all({
                'type': 'user_left',
                'username': username,
                'message': f'{username} left the chat',
                'timestamp': datetime.now().isoformat()
            })
            
        logger.info(f"Client {client_id} disconnected. Total clients: {len(connected_clients)}")

async def broadcast_to_others(sender_websocket, message):
    """Broadcast message to all clients except the sender"""
    if connected_clients:
        disconnected_clients = []
        
        for client in connected_clients:
            if client != sender_websocket:
                try:
                    await client.send(json.dumps(message))
                except ConnectionClosed:
                    disconnected_clients.append(client)
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {e}")
                    disconnected_clients.append(client)
        
        # Clean up disconnected clients
        for client in disconnected_clients:
            if client in connected_clients:
                del connected_clients[client]

async def broadcast_to_all(message):
    """Broadcast message to all clients"""
    if connected_clients:
        disconnected_clients = []
        
        for client in connected_clients:
            try:
                await client.send(json.dumps(message))
            except ConnectionClosed:
                disconnected_clients.append(client)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected_clients.append(client)
        
        # Clean up disconnected clients
        for client in disconnected_clients:
            if client in connected_clients:
                del connected_clients[client]

async def main():
    """Main server function"""
    # Use environment variables for cloud deployment
    host = os.environ.get("HOST", "0.0.0.0")  # Listen on all interfaces for cloud
    port = int(os.environ.get("PORT", 8766))   # Use PORT env var or default to 8766
    
    logger.info(f"Starting Chat WebSocket server on {host}:{port}")
    
    async with serve(handle_client, host, port) as server:
        logger.info(f"Chat WebSocket server is running on ws://{host}:{port}")
        logger.info("Press Ctrl+C to stop the server")
        
        try:
            await server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
        finally:
            logger.info("Shutting down server...")

if __name__ == "__main__":
    asyncio.run(main()) 