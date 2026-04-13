import logging

from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException

from src.application.cancel_subscription import CancelSubscriptionInput
from src.application.renew_subscription import RenewSubscriptionInput
from src.application.exceptions import SubscriptionConflictError, SubscriptionNotFoundError, UserNotFoundError, PlanNotFoundError
from src.application.subscribe_to_plan import SubscribeToPlanInput, SubscribeToPlanOutput
from src.infra.api.dependencies import SubscribeToPlanUseCaseDep, CancelSubscriptionUseCaseDep, RenewSubscriptionUseCaseDep

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
    

@router.delete("/{subscription_id}", status_code=200)   
def cancel_subscription(
    subscription_id: UUID,
    use_case: CancelSubscriptionUseCaseDep
) -> None:
    try:
        use_case.execute(input=CancelSubscriptionInput(subscription_id=subscription_id))
    except SubscriptionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logging.error("Unexpected error while cancelling subscription", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/{subscription_id}/renew", status_code=200)
def renew_subscription(
    subscription_id: UUID,
    payload: RenewSubscriptionInput,
    use_case: RenewSubscriptionUseCaseDep
) -> None:
    try:
        use_case.execute(payload)
    except SubscriptionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logging.error("Unexpected error while renewing subscription", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")