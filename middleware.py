from fastapi import Request
from dotenv import load_dotenv
import os

load_dotenv()

def setup_middleware(app):
    if os.getenv("ENABLE_PROCESS_TIME_HEADER", "True").lower() == "true":
        @app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            hari=request.json
            print ("qqqqq",hari )
            import time
            start = time.perf_counter()
            response = await call_next(request)
            response.headers["X-Process-Time"] = str(time.perf_counter() - start)
            return response
        
