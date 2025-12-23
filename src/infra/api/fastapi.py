from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.api.routes import plans_router, accounts_router, subscriptions_router
from src.infra.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize application
    create_db_and_tables()
    yield
    # Shutdown: Clean up resources if needed
    pass

app = FastAPI(title="Subscription Service API", lifespan=lifespan)

# Include routers
app.include_router(plans_router)
app.include_router(accounts_router)
app.include_router(subscriptions_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
