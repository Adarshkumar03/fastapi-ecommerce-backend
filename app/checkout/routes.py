from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.security import user_required
from .crud import process_checkout

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("/")
async def checkout(db: Session = Depends(get_db), user=Depends(user_required)):
    try:
        return process_checkout(db, user.id)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": str(ve),
                "code": 400
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "message": "An unexpected error occurred during checkout",
                "code": 500
            }
        )
