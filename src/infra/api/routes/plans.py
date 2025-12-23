import logging

from fastapi import APIRouter, HTTPException

from src.application.create_plan import CreatePlanInput, CreatePlanOutput
from src.application.exceptions import DuplicatePlanError
from src.infra.api.dependencies import CreatePlanUseCaseDep

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("", response_model=CreatePlanOutput, status_code=201)
def create_plan(
    plan_data: CreatePlanInput,
    use_case: CreatePlanUseCaseDep,
) -> CreatePlanOutput:
    try:
        return use_case.execute(plan_data)
    except DuplicatePlanError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logging.error("Unexpected error while creating plan", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
