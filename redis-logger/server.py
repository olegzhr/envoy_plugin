import json
import asyncio
import os
import redis.asyncio as redis

LOG_FILE = "/logs/envoy_access.log"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_KEY = os.getenv("REDIS_KEY", "log_proxy")


async def get_redis():
    while True:
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            await r.ping()
            return r
        except Exception as e:
            print(f"redis connect error: {e}, retry in 3s", flush=True)
            await asyncio.sleep(3)


async def tail_and_push():
    r = await get_redis()
    print(f"connected to redis {REDIS_HOST}:{REDIS_PORT}", flush=True)

    while not os.path.exists(LOG_FILE):
        print(f"waiting for {LOG_FILE}...", flush=True)
        await asyncio.sleep(2)

    print(f"tailing {LOG_FILE}", flush=True)
    with open(LOG_FILE, "r") as f:
        while True:
            line = f.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
            line = line.strip()
            if line:
                try:
                    await r.rpush(REDIS_KEY, line)
                    print(f"pushed: {line[:80]}...", flush=True)
                except Exception as e:
                    print(f"redis push error: {e}", flush=True)
                    r = await get_redis()


if __name__ == "__main__":
    asyncio.run(tail_and_push())
