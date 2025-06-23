from fastapi import APIRouter
from src.api.media_files.media_files_get_all import media_files_get_all
from src.api.media_files.media_files_post import media_files_post
from src.api.media_files.media_files_patch import media_files_patch
from src.api.media_files.media_files_get import media_files_get
from src.api.media_files.media_files_delete import media_files_delete


router = APIRouter()
router.include_router(media_files_get_all.router)
router.include_router(media_files_get.router)
router.include_router(media_files_post.router)
router.include_router(media_files_patch.router)
router.include_router(media_files_delete.router)
