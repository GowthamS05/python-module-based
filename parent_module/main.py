from fastapi import FastAPI
from controllers.health_controller import router as health_router
from controllers.math_controller import router as math_router
from child_library import subtraction_router
import uvicorn

app = FastAPI(title="Parent Module API", version="1.0.0")

app.include_router(health_router, tags=["Health"])
app.include_router(math_router, tags=["Math"])
app.include_router(subtraction_router, tags=["Math"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
