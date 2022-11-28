import os
from importlib.util import find_spec

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi


# from fastapi.openapi.docs import (
#     get_redoc_html,
#     get_swagger_ui_html,
#     get_swagger_ui_oauth2_redirect_html,
# )



# Export Django settings env variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
apps.populate(settings.INSTALLED_APPS)

# This endpoint imports should be placed below the settings env declaration
# Otherwise, django will throw a configure() settings error
from app.api import router as api_router

# Get the Django WSGI application we are working with
application = get_wsgi_application()

# This can be done without the function, but making it functional
# tidies the entire code and encourages modularity
def get_application() -> FastAPI:
    # Main Fast API application
    app = FastAPI(
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        debug=settings.DEBUG
    )
    
    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_HOSTS] or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include all api endpoints
    app.include_router(api_router, prefix=settings.API_V1_STR) 
    app.mount("/app/", WSGIMiddleware(application))
    
    return app


app = get_application()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="KORA",
        version="0.0.1",
        description="Zarządzanie userami i innymi rzeczami",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/kora-logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

