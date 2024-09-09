import uvicorn

from fastapi import FastAPI
from typing import AsyncIterator

from challenge import constants
from challenge.core.log_manager import LogManager


#Lifespan events
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manages the lifecycle of the FastAPI application.

    This function handles the startup and shutdown events for the application:
    - **Startup**: Initializes the logger, logs application version and startup message.
    - **Shutdown**: Logs a shutdown message when the application is closing.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This is an asynchronous iterator that yields control to FastAPI and waits for the application to finish running.
    """

    # StartUp events
    log_manager = LogManager()
    app.logger = log_manager.logger()
    app.logger.info(f"Unit version: {constants.VERSION}")
    app.logger.info(f"Starting unit execution.")
    try:
        yield
    finally:
    # ShutDown event
        app.logger.info("Shutting down.")

# Initialize App object
app = FastAPI(lifespan=lifespan)

# App metadata
app.title = constants.TITLE
app.description = constants.DESCRIPTION
app.version = constants.VERSION
app.contact = constants.CONTACT

# Include all APIs routers
# Response exceptions Handlers

def run_dev_server():
    """Run the server for development purposes."""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_dev_server()
