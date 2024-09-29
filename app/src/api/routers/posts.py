from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src import schemas

from typing import Annotated
from src.repository.post import PostRepository
from src.api.dependencies.repository import get_repository
from src.utilities.exceptions.database import EntityDoesNotExist


router = APIRouter()


@router.get("/posts", response_model=List[schemas.Post])
async def get_posts(
    filter: Annotated[schemas.PostsFilter, Query()],
    post_repo: PostRepository = Depends(get_repository(PostRepository)),
):
    posts = await post_repo.read_posts(filter=filter)

    exclude_fields = schemas.get_missing_includes(
        filter.include, schemas.PostAllowedIncludes
    )
    PostSchema = schemas.omit_model_fields(schemas.Post, exclude_fields)

    json_compatible_item_data = jsonable_encoder(
        [PostSchema.model_validate(post) for post in posts]
    )
    return JSONResponse(content=json_compatible_item_data)


@router.get("/posts/{post_id}", response_model=schemas.Post)
async def get_post(
    post_id: int,
    filter: Annotated[schemas.PostFilter, Query()],
    post_repo: PostRepository = Depends(get_repository(PostRepository)),
):
    try:
        post = await post_repo.read_post_by_id(id=post_id, filter=filter)
    except EntityDoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))

    exclude_fields = schemas.get_missing_includes(
        filter.include, schemas.PostAllowedIncludes
    )
    PostSchema = schemas.omit_model_fields(schemas.Post, exclude_fields)

    json_compatible_item_data = jsonable_encoder(PostSchema.model_validate(post))
    return JSONResponse(content=json_compatible_item_data)
