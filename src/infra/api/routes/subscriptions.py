import logging

from fastapi import APIRouter, HTTPException

from src.application.exceptions import SubscriptionConflictError, UserNotFoundError, PlanNotFoundError
from src.application.subscribe_to_plan import SubscribeToPlanInput, SubscribeToPlanOutput
from src.infra.api.dependencies import SubscribeToPlanUseCaseDep

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("", status_code=201)
def subscribe_to_plan(
    payload: SubscribeToPlanInput,
    use_case: SubscribeToPlanUseCaseDep
) -> SubscribeToPlanOutput:
    try:
        return use_case.execute(payload)
    except (UserNotFoundError, PlanNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SubscriptionConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))  # Conflict
    except Exception:
        logging.error("Unexpected error while susbcribing to plan", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
