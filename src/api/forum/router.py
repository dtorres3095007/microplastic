from fastapi import APIRouter
from src.api.forum.forum_post import forum_post


router = APIRouter()
router.include_router(forum_post.router)
