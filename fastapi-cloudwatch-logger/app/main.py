from fastapi import FastAPI
from .logger import logger

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}


@app.get("/test-debug")
async def test_debug():
    logger.debug("This is a DEBUG level test message")
    return {"level": "debug", "status": "log sent"}


@app.get("/test-info")
async def test_info():
    logger.info("This is an INFO level test message")
    return {"level": "info", "status": "log sent"}


@app.get("/test-warning")
async def test_warning():
    logger.warning("This is a WARNING level test message")
    return {"level": "warning", "status": "log sent"}

@app.get("/test-error")
async def test_error():
    print("Endpoint /test-error called")
    
    try:
        # Log the error message
        print("Attempting to log error message to CloudWatch")
        logger.error("This is an ERROR level test message")
        print("Error message logged")
        
        # Force flush all handlers
        print("Attempting to flush log handlers")
        for handler in logger.handlers:
            print(f"Handler type: {type(handler)}")
            if hasattr(handler, 'flush'):
                handler.flush()
                print(f"Flushed handler: {type(handler)}")
        
        return {"level": "error", "status": "log sent"}
    except Exception as e:
        print(f"Exception in /test-error endpoint: {str(e)}")
        return {"level": "error", "status": "error", "message": str(e)}


@app.get("/test-exception")
async def test_exception():
    try:
        # Deliberately cause an exception
        result = 1 / 0
    except Exception as e:
        logger.exception(f"Caught an exception: {str(e)}")
    return {"level": "exception", "status": "log sent"}


@app.get("/test-info")
async def test_info(message: str = None):
    log_message = message if message else "This is an INFO level test message"
    logger.info(log_message)
    return {"level": "info", "status": "log sent", "message": log_message}
