from fastapi import FastAPI
from app.routers.genotools_router import router as genotools_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the GenoTools API!"}

# Include the router for genotools
app.include_router(genotools_router)