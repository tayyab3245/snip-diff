"""
Test WebSocket Live Diff Channel
Validates WebSocket connection, subscription, and event broadcasting
"""
import asyncio
import json
import tempfile
import os
import time
import websockets
from pathlib import Path

async def test_websocket_live_diff():
    """Test complete WebSocket workflow"""
    print("=== WebSocket Live Diff Test ===")
    
    # Test configuration
    server_url = "ws://localhost:8000/api/ws/diff"
    client_id = "test_client_001"
    
    # Create test file
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "test_websocket.txt")
    with open(test_file, 'w') as f:
        f.write("Initial content\nLine 2\nLine 3")
    
    try:
        # Connect to WebSocket
        uri = f"{server_url}?client_id={client_id}"
        print(f"Connecting to: {uri}")
        
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected successfully")
            
            # Test 1: Subscribe to test file
            subscribe_msg = {
                "action": "subscribe",
                "paths": [test_file]
            }
            await websocket.send(json.dumps(subscribe_msg))
            print(f"📤 Sent subscription for: {test_file}")
            
            # Wait for subscription confirmation
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            print(f"📥 Received: {data}")
            
            if data.get("type") == "subscription_confirmed":
                print("✅ Subscription confirmed")
            else:
                print("❌ Expected subscription confirmation")
                return False
            
            # Test 2: Start live watch via REST API
            import requests
            start_watch_response = requests.post(
                "http://localhost:8000/api/live/start",
                json={"file_paths": [test_file]}
            )
            print(f"📤 Started live watch: {start_watch_response.json()}")
            
            # Test 3: Modify file and expect WebSocket event
            print("🔄 Modifying test file...")
            with open(test_file, 'w') as f:
                f.write("Modified content\nNew line 2\nAdded line 3\nExtra line 4")
            
            # Wait for file diff event
            event_received = False
            timeout_seconds = 10
            start_time = time.time()
            
            while time.time() - start_time < timeout_seconds:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    data = json.loads(response)
                    print(f"📥 Received event: {data.get('type')} for {data.get('path', 'unknown')}")
                    
                    if data.get("type") == "file_diff" and data.get("path") == test_file:
                        print("✅ File diff event received!")
                        print(f"   Change type: {data.get('change_type')}")
                        print(f"   Sequence: {data.get('seq')}")
                        print(f"   Has diff data: {'diff' in data}")
                        print(f"   Has modes: {'modes' in data}")
                        event_received = True
                        break
                    elif data.get("type") == "ping":
                        # Respond to ping
                        pong_msg = {"action": "pong", "timestamp": time.time()}
                        await websocket.send(json.dumps(pong_msg))
                        print("🏓 Responded to ping")
                    
                except asyncio.TimeoutError:
                    continue
            
            if event_received:
                print("✅ Live diff event test passed!")
            else:
                print("❌ No file diff event received within timeout")
                return False
            
            # Test 4: Unsubscribe
            unsubscribe_msg = {
                "action": "unsubscribe", 
                "paths": [test_file]
            }
            await websocket.send(json.dumps(unsubscribe_msg))
            print("📤 Sent unsubscribe request")
            
            # Wait for unsubscribe confirmation
            response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
            data = json.loads(response)
            print(f"📥 Unsubscribe response: {data}")
            
            # Test 5: Stop live watch
            stop_response = requests.post("http://localhost:8000/api/live/stop")
            print(f"📤 Stopped live watch: {stop_response.json()}")
            
            print("✅ All WebSocket tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False
    
    finally:
        # Cleanup test file
        try:
            os.unlink(test_file)
            os.rmdir(temp_dir)
        except:
            pass

async def test_websocket_stats():
    """Test WebSocket statistics endpoint"""
    print("\n=== WebSocket Stats Test ===")
    
    import requests
    try:
        response = requests.get("http://localhost:8000/api/ws/diff/stats")
        stats = response.json()
        print(f"📊 WebSocket Stats: {json.dumps(stats, indent=2)}")
        
        health_response = requests.get("http://localhost:8000/api/ws/diff/health")
        health = health_response.json()
        print(f"💚 WebSocket Health: {json.dumps(health, indent=2)}")
        
        return True
    except Exception as e:
        print(f"❌ Stats test failed: {e}")
        return False

async def main():
    """Run all WebSocket tests"""
    print("Starting WebSocket Live Diff Channel Tests...")
    
    # Test stats endpoint first
    stats_ok = await test_websocket_stats()
    
    # Test full WebSocket workflow
    websocket_ok = await test_websocket_live_diff()
    
    # Final stats
    await test_websocket_stats()
    
    if stats_ok and websocket_ok:
        print("\n🎉 All tests passed! WebSocket Live Diff Channel is working correctly.")
        return True
    else:
        print("\n💥 Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    asyncio.run(main())
