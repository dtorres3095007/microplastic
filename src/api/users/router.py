from fastapi import APIRouter
from src.api.users.users_get_all import users_get_all
from src.api.users.users_login_post import users_login_post
from src.api.users.users_post import users_create_post
from src.api.users.users_get import users_get
from src.api.users.users_patch import users_patch


router = APIRouter()

router.include_router(users_get_all.router)
router.include_router(users_get.router)
router.include_router(users_login_post.router)
router.include_router(users_create_post.router)
router.include_router(users_patch.router)
