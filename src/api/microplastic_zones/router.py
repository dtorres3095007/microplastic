from fastapi import APIRouter
from src.api.microplastic_zones.microplastic_zones_post import microplastic_zones_post


router = APIRouter()
router.include_router(microplastic_zones_post.router)
