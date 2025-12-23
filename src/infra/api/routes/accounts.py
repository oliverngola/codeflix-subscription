import logging

from fastapi import APIRouter, HTTPException

from src.application.create_user_account import (
    CreateUserAccountOutput,
    CreateUserAccountInput,
)
from src.application.exceptions import UserAlreadyExistsError
from src.infra.api.dependencies import CreateUserAccountUseCaseDep

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", status_code=201)
def create_user_account(
    payload: CreateUserAccountInput,
    use_case: CreateUserAccountUseCaseDep,
) -> CreateUserAccountOutput:
    try:
        return use_case.execute(payload)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logging.error("Unexpected error while creating user account", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
