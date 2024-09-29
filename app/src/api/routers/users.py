from typing import Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Query

from src import schemas
from src.api.dependencies.repository import get_repository
from src.repository.user import UserRepository
from src.utilities.exceptions.database import EntityDoesNotExist


router = APIRouter()


@router.get("/users/{user_id}", response_model=schemas.User)
async def get_user(
    user_id: int,
    filter: Annotated[schemas.UserFilter, Query()],
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
):
    try:
        user = await user_repo.read_user_by_id(id=user_id, filter=filter)
    except EntityDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))

    exclude_fields = schemas.get_missing_includes(
        filter.include, schemas.UserAllowedIncludes
    )
    UserScheme = schemas.omit_model_fields(schemas.User, exclude_fields)

    json_compatible_item_data = jsonable_encoder(UserScheme.model_validate(user))
    return JSONResponse(content=json_compatible_item_data)
