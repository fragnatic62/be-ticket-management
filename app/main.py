from fastapi import FastAPI

from app.api import v1, public
from app.core.common.config import config


app = FastAPI(
    root_path=config.ROOT_PATH
)


app.include_router(v1.private_router, prefix=f'/{v1.VERSION}')
app.include_router(public.public_router, prefix=f'/{public.VERSION}')
