# -*- coding: utf-8 -*-
"""API module"""

from fastapi import APIRouter, Request, HTTPException, Query
from typing import List

from challenge.models.leads_model import Lead, LeadInDB


router = APIRouter()

# In-memory database
db: List[LeadInDB] = []

@router.post("/", response_model=LeadInDB)
async def create_lead(lead: Lead, request: Request) -> LeadInDB:
    """
    Create a new lead.

    This endpoint creates a new lead with the provided data, assigns it a unique ID, and stores it in the database.
    It logs the creation process and returns the newly created lead.

    Args:
        lead (Lead): The lead data to be created.
        request (Request): The request object which provides access to application-specific data and logging.

    Returns:
        LeadInDB: The newly created lead with an assigned ID.
    """

    logger = request.app.logger
    logger.info("Creating lead...")
    lead_id = len(db) + 1
    lead_in_db = LeadInDB(id=lead_id, **lead.model_dump())
    db.append(lead_in_db)
    return lead_in_db

@router.get("/", response_model=List[LeadInDB])
async def get_leads(
    request: Request,
    skip: int = Query(0, alias="start", ge=0),
    limit: int = Query(10, le=100)) -> List[LeadInDB]:
    """
    Retrieve a list of leads with pagination.

    This endpoint retrieves a subset of leads from the database based on the specified pagination parameters.
    It logs the retrieval process and returns a list of leads starting from the index specified by `skip` and
    including up to `limit` leads.

    Args:
        request (Request): The request object which provides access to application-specific data and logging.
        skip (int, optional): The number of leads to skip. Defaults to 0. This parameter is aliased as "start" and must be greater than or equal to 0.
        limit (int, optional): The maximum number of leads to return. Defaults to 10. It must be less than or equal to 100.

    Returns:
        List[LeadInDB]: A list of leads retrieved from the database, starting from the `skip` index and including up to `limit` leads.
    """

    logger = request.app.logger
    logger.info("Getting leads...")
    return db[skip: skip + limit]

@router.get("/{lead_id}", response_model=LeadInDB)
async def get_lead_by_id(lead_id: int, request: Request) -> LeadInDB:
    """
    Retrieve a lead by its ID.

    This endpoint retrieves a lead from the database based on the provided lead ID. It logs the retrieval process
    and returns the lead with the specified ID. If the lead is not found, it logs an error and raises a 404 HTTP
    exception.

    Args:
        lead_id (int): The ID of the lead to retrieve.
        request (Request): The request object which provides access to application-specific data and logging.

    Returns:
        LeadInDB: The lead with the specified ID.

    Raises:
        HTTPException: If the lead with the specified ID is not found, a 404 HTTP exception is raised.
    """

    logger = request.app.logger
    logger.info("Getting lead...")
    for lead in db:
        if lead.id == lead_id:
            return lead
    logger.error("Lead not found")
    raise HTTPException(status_code=404, detail="Lead not found")
