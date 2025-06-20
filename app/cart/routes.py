from ..core.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from ..auth.security import get_current_user, user_required
from .schema import CartItemCreate, CartItemOut, CartItemUpdate
from .crud import add_to_cart, get_cart_items, remove_from_cart, update_cart_item

router = APIRouter()

@router.post("/", response_model=CartItemOut)
async def add_product_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user=Depends(user_required)):
    try:
        return add_to_cart(db, user.id, item)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": str(e),
                "code": 400
            }
        )


@router.get("/", response_model=list[CartItemOut])
async def view_cart(db: Session = Depends(get_db), user=Depends(user_required)):
    try:
        return get_cart_items(db, user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": True,
                "message": "Failed to fetch cart items.",
                "code": 500
            }
        )


@router.delete("/{product_id}")
async def remove_product_from_cart(product_id: int, db: Session = Depends(get_db), user=Depends(user_required)):
    try:
        return remove_from_cart(db, user.id, product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": True,
                "message": str(e),
                "code": 404
            }
        )


@router.put("/{product_id}", response_model=CartItemOut)
async def update_product_quantity(product_id: int, item: CartItemUpdate, db: Session = Depends(get_db), user=Depends(user_required)):
    try:
        return update_cart_item(db, user.id, product_id, item.quantity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": True,
                "message": str(e),
                "code": 400
            }
        )
