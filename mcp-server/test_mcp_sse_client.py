#!/usr/bin/env python3
"""
Test client for MCP SSE Server
Demonstrates how to connect to and use the online MCP server
"""

import asyncio
import json
import os
from typing import Optional

import httpx


class MCPSSEClient:
    """Simple MCP SSE client for testing"""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "text/event-stream"
        }

    async def health_check(self) -> dict:
        """Check server health"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/health",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()

    async def get_server_info(self) -> dict:
        """Get server information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()

    async def test_connection(self):
        """Test basic connection to MCP SSE server"""
        print("🧪 Testing MCP SSE Server Connection\n")

        # Test 1: Server info
        print("📋 Test 1: Server Info")
        try:
            info = await self.get_server_info()
            print(f"✅ Server: {info.get('name')}")
            print(f"✅ Version: {info.get('version')}")
            print(f"✅ Transport: {info.get('transport')}")
            print()
        except Exception as e:
            print(f"❌ Failed: {e}\n")
            return

        # Test 2: Health check
        print("💚 Test 2: Health Check")
        try:
            health = await self.health_check()
            print(f"✅ Status: {health.get('status')}")
            print(f"✅ Backend: {health.get('backend')}")
            print(f"✅ Timestamp: {health.get('timestamp')}")
            print()
        except Exception as e:
            print(f"❌ Failed: {e}\n")
            return

        # Test 3: SSE connection
        print("🔌 Test 3: SSE Connection")
        print("Connecting to SSE endpoint...")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream(
                    "GET",
                    f"{self.base_url}/sse",
                    headers=self.headers
                ) as response:
                    response.raise_for_status()
                    print(f"✅ Connected! Status: {response.status_code}")
                    print("📡 Listening for events (5 seconds)...")

                    count = 0
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]  # Remove "data: " prefix
                            print(f"📨 Event: {data[:100]}...")  # Show first 100 chars
                            count += 1

                        # Limit test duration
                        if count >= 3:
                            break

                    print(f"✅ Received {count} events\n")
        except Exception as e:
            print(f"❌ Failed: {e}\n")
            return

        print("🎉 All tests passed!")


async def main():
    """Main test function"""
    # Configuration
    BASE_URL = os.getenv("MCP_SSE_URL", "https://yourdomain.com/mcp")
    API_KEY = os.getenv("MCP_API_KEY", "")

    if not API_KEY:
        print("❌ Error: MCP_API_KEY environment variable not set")
        print("\nUsage:")
        print("  export MCP_SSE_URL='https://yourdomain.com/mcp'")
        print("  export MCP_API_KEY='your-api-key-here'")
        print("  python test_mcp_sse_client.py")
        return

    print(f"🌐 Connecting to: {BASE_URL}")
    print(f"🔑 Using API key: {API_KEY[:10]}...\n")

    # Create client and run tests
    client = MCPSSEClient(BASE_URL, API_KEY)
    await client.test_connection()


if __name__ == "__main__":
    asyncio.run(main())
