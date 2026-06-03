import asyncio
import httpx

async def poll_server(server_id: str, url: str, store: dict):
    """
    Makes an HTTP GET request to {url}/health.
    Sets status to "UP" (200 OK), "DEGRADED" (non-200), or "DOWN" (connection error).
    Updates the server in the store in-place.
    """
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{url}/health")
            if response.status_code == 200:
                status = "UP"
            else:
                status = "DEGRADED"
    except httpx.HTTPError:
        status = "DOWN"
    except Exception:
        status = "DOWN"

    if server_id in store:
        store[server_id].status = status


async def run_poll_loop(store: dict, interval: int = 10):
    """
    An infinite async loop that runs poll_server for all servers in the store concurrently.
    """
    while True:
        # Create a snapshot list of items to avoid size-change exceptions during iteration
        servers = list(store.values())
        if servers:
            tasks = [
                poll_server(server.id, server.base_url(), store)
                for server in servers
            ]
            await asyncio.gather(*tasks)
        await asyncio.sleep(interval)
