from fastapi import APIRouter
from src.api.forum.forum_post import forum_post
from src.api.forum.forum_get_all import forum_get_all


router = APIRouter()
router.include_router(forum_post.router)
router.include_router(forum_get_all.router)
