from fastapi import APIRouter, Depends
from app.auth.dependencies import require_admin
from app.models import User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def admin_stats(user: User = Depends(require_admin)):
    return {
        "message": "Admin access granted",
        "admin_id": user.id,
    }
