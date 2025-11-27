from fastapi import APIRouter

from src.api.routes import source
from src.api.routes import (
    ticket,
    operator,
    lead,
    stats,
)

router = APIRouter()

router.include_router(operator.router)
router.include_router(source.router)
router.include_router(ticket.router)
router.include_router(lead.router)
router.include_router(stats.router)
