import azure.functions as func
from src.main import app as fastapi_app

import logging

app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
