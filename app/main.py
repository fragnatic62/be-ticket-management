from fastapi import FastAPI

from app.api import v1, public
from app.core.common.config import config
from fastapi.middleware.cors import CORSMiddleware

# Define the allowed origins for the CORS policy
origins = [
    "http://localhost:5173",  # Adjust this to the origin of your frontend application
]

app = FastAPI(
    root_path=config.ROOT_PATH
)

# Add CORS middleware to allow cross-origin requests from the specified origins
app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=origins,  # Allows specified origins to make requests
    allow_credentials=True,  # Allows cookies to be included in cross-origin HTTP requests
    allow_methods=['GET', 'POST', 'OPTIONS'],  # Specifies the allowed HTTP methods
    allow_headers=['Authorization', 'Content-Type', 'x-api-key'],  # Specifies the allowed headers
)

app.include_router(v1.private_router, prefix=f'/{v1.VERSION}')
app.include_router(public.public_router, prefix=f'/{public.VERSION}')
