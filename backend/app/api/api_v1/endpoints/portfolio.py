from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User, Portfolio, PortfolioTransaction

router = APIRouter()


class AddHoldingRequest(BaseModel):
    ticker: str
    shares: float
    price: float


class RemoveHoldingRequest(BaseModel):
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
def get_portfolio(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> Any:
    user_id = _get_user_id(current_user)
    _get_user_db(db, user_id)

    holdings = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    holdings_list = []
    total_value = 0.0
    total_cost = 0.0

    for h in holdings:
        value = h.shares * h.average_buy_price
        total_value += value
        total_cost += h.shares * h.average_buy_price
        holdings_list.append({
            "ticker": h.ticker,
            "shares": h.shares,
            "average_buy_price": h.average_buy_price,
        })

    return {
        "holdings": holdings_list,
        "total_value": round(total_value, 2),
        "total_cost": round(total_cost, 2),
    }


@router.post("/add", response_model=dict)
def add_to_portfolio(
    request: AddHoldingRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    user_id = _get_user_id(current_user)
    _get_user_db(db, user_id)

    existing = (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user_id, Portfolio.ticker == request.ticker.upper())
        .first()
    )

    if existing:
        new_total_shares = existing.shares + request.shares
        if new_total_shares <= 0:
            db.delete(existing)
            db.commit()
            return {"message": f"Removed all {request.ticker.upper()} holdings."}

        existing.average_buy_price = (
            (existing.shares * existing.average_buy_price + request.shares * request.price)
            / new_total_shares
        )
        existing.shares = new_total_shares
    else:
        if request.shares <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shares must be positive for a new holding.",
            )
        new_holding = Portfolio(
            user_id=user_id,
            ticker=request.ticker.upper(),
            shares=request.shares,
            average_buy_price=request.price,
        )
        db.add(new_holding)

    db.flush()
    portfolio_record = existing if existing else new_holding
    tx = PortfolioTransaction(
        portfolio_id=portfolio_record.id,
        transaction_type="BUY",
        shares=request.shares,
        price_per_share=request.price,
    )
    db.add(tx)
    db.commit()
    db.refresh(portfolio_record)

    return {"message": f"Added {request.shares} shares of {request.ticker.upper()} at {request.price}."}


@router.delete("/remove", response_model=dict)
def remove_from_portfolio(
    request: RemoveHoldingRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    user_id = _get_user_id(current_user)
    _get_user_db(db, user_id)

    holding = (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user_id, Portfolio.ticker == request.ticker.upper())
        .first()
    )
    if not holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{request.ticker.upper()} not found in portfolio.",
        )

    db.delete(holding)
    db.commit()

    return {"message": f"Removed {request.ticker.upper()} from portfolio."}
