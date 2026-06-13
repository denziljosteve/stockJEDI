from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User, Watchlist

router = APIRouter()


class AddTickerRequest(BaseModel):
    ticker: str


class RemoveTickerRequest(BaseModel):
    ticker: str


def _get_user_id(current_user: dict) -> int:
    user_id = current_user.get("sub") or current_user.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return int(user_id)


def _get_user_db(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("/", response_model=dict)
def get_watchlist(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> Any:
    user_id = _get_user_id(current_user)
    _get_user_db(db, user_id)

    items = db.query(Watchlist).filter(Watchlist.user_id == user_id).all()

    return {
        "items": [
            {"ticker": item.ticker, "added_at": str(item.added_at)}
            for item in items
        ]
    }


@router.post("/add", response_model=dict)
def add_to_watchlist(
    request: AddTickerRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    user_id = _get_user_id(current_user)
    _get_user_db(db, user_id)

    ticker = request.ticker.upper()

    existing = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id, Watchlist.ticker == ticker)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{ticker} is already in your watchlist.",
        )

    item = Watchlist(user_id=user_id, ticker=ticker)
    db.add(item)
    db.commit()

    return {"message": f"Added {ticker} to watchlist."}


@router.delete("/remove", response_model=dict)
def remove_from_watchlist(
    request: RemoveTickerRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    user_id = _get_user_id(current_user)
    _get_user_db(db, user_id)

    ticker = request.ticker.upper()

    item = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == user_id, Watchlist.ticker == ticker)
        .first()
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{ticker} not found in watchlist.",
        )

    db.delete(item)
    db.commit()

    return {"message": f"Removed {ticker} from watchlist."}
