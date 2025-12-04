from fastapi import APIRouter, Query
from handlers.math_handler import add_numbers
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.get("/add")
def addition(
    a: float = Query(..., description="First number"),
    b: float = Query(..., description="Second number")
):
    test_key = os.getenv("TEST_KEY")
    print(f"Math Controller - TEST_KEY: {test_key}")
    result = add_numbers(a, b)
    return {"a": a, "b": b, "result": result}
