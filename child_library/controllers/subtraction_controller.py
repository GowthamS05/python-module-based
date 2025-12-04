from fastapi import APIRouter, Query
from child_library.handlers.math_handler import subtract_numbers
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.get("/subtract")
def subtraction(
    a: float = Query(..., description="First number"),
    b: float = Query(..., description="Second number")
):
    test_key = os.getenv("TEST_KEY")
    print(f"Subtraction Controller - TEST_KEY: {test_key}")
    result = subtract_numbers(a, b)
    return {"a": a, "b": b, "result": result}
