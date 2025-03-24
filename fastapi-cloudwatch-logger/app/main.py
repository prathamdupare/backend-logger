from fastapi import FastAPI, Request
from .logger import logger

app = FastAPI()

# Middleware to flush log handlers after each request
@app.middleware("http")
async def flush_logs_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # Flush all log handlers
    for handler in logger.handlers:
        if hasattr(handler, 'flush'):
            handler.flush()
    
    return response

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}

@app.get("/test-debug")
async def test_debug():
    logger.debug("This is a DEBUG level test message")
    return {"level": "debug", "status": "log sent"}

@app.get("/test-info")
async def test_info(message: str = None):
    log_message = message if message else "This is an INFO level test message"
    logger.info(log_message)
    return {"level": "info", "status": "log sent", "message": log_message}

@app.get("/test-warning")
async def test_warning():
    logger.warning("This is a WARNING level test message")
    return {"level": "warning", "status": "log sent"}

@app.get("/test-error")
async def test_error():
    logger.error("This is an ERROR level test message")
    return {"level": "error", "status": "log sent"}

@app.get("/test-exception")
async def test_exception():
    try:
        # Deliberately cause an exception
        result = 1 / 0
    except Exception as e:
        logger.exception(f"Caught an exception: {str(e)}")
    return {"level": "exception", "status": "log sent"}
