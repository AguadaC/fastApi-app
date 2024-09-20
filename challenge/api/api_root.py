# -*- coding: utf-8 -*-
"""API Endpoints for the root URL"""

from fastapi import APIRouter
from fastapi import Request

from challenge.constants import DESCRIPTION
from challenge.models.api_models import WelcomeModel


router = APIRouter()

@router.get("/", response_model=WelcomeModel)
def return_welcome_message(request: Request):
    """
    Return welcome message.

    Gives information about the application.
    """
    logger = request.app.logger
    logger.info("New request to root endpoint.")

    title = "You have reached out to the App"
    detail = (
        f"{DESCRIPTION}."
        " For more information about available API endpoints, visit"
        " /docs endpoint."
    )

    base_url = str(request.base_url).strip("/")
    docs = f"{base_url}/docs"

    response = WelcomeModel(title=title, detail=detail, docs=docs)
    return response