from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def auth_status() -> dict[str, str]:
    """Temporary route proving the auth router is connected; replace with real auth endpoints."""
    return {"module": "auth", "status": "scaffold"}
