from fastapi import APIRouter
from handlers.health_handler import check_health
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.get("/health")
def health_check():
    test_key = os.getenv("TEST_KEY")
    print(f"Health Controller - TEST_KEY: {test_key}")
    return check_health()
