from fastapi import APIRouter
from src.api.microplastic_zones.microplastic_zones_post import microplastic_zones_post
from src.api.microplastic_zones.microplastic_zones_get_all import (
    microplastic_zones_get_all,
)


router = APIRouter()
router.include_router(microplastic_zones_post.router)
router.include_router(microplastic_zones_get_all.router)
