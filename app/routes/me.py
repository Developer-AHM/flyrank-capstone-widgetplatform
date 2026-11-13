from fastapi import APIRouter, Depends

from app.routes.deps import current_user

router = APIRouter()


@router.get("/me", summary="Who am I? (temporary test route)")
def me(user=Depends(current_user)):
    return {"id": user.id, "email": user.email}