# -*- coding: utf-8 -*-
"""API Leads module"""

from fastapi import APIRouter, Request, Path
from typing import List

from challenge.models.api_models import (CreateLeadModel,
                                         ResponseLeadId,
                                         ResponseLead)
from challenge.exceptions import (StudentDoesNotExist,
                                  StudentAlreadyExists)
from challenge.core.db_handler import DbHandler


router = APIRouter()

@router.post("/", response_model=ResponseLeadId)
async def create_lead(lead: CreateLeadModel, request: Request):
    """
    Create a new lead record in the database.

    Args:
        lead (CreateLeadModel): The lead data to be created. This includes:
        dni, name, email, phone and address.
        request (Request): The FastAPI request object, used for logging.

    Returns:
        dict: A dictionary containing the ID of the created lead.

    Raise:
        StudentAlreadyExists: When the student exists.
    """
    logger = request.app.logger
    logger.info("Creating lead...")
    db_handler = DbHandler()
    try:
        lead_in_db = await db_handler._get_student_id_by_dni(dni=lead.dni)
        raise StudentAlreadyExists(
                    f"Student with DNI: {lead.dni}, exists. ID record: {lead_in_db}")
    except StudentDoesNotExist:
        lead_in_db = await db_handler._create_student(dni=lead.dni,
                                                      name=lead.name,
                                                      email=lead.email,
                                                      phone=lead.phone,
                                                      address=lead.address)
    logger.info(f"Lead {lead_in_db} created sucessfully")
    return {"student_id": lead_in_db}

@router.get("/", response_model=List[ResponseLead])
async def get_leads(request: Request):
    """
    Retrieve all lead records from the database.

    Args:
        request (Request): The FastAPI request object, used for logging.

    Returns:
        List[ResponseLead]: A list of lead records. Each record is represented as an instance of ResponseLead.
    """
    logger = request.app.logger
    logger.info("Getting leads...")
    db_handler = DbHandler()
    leads = await db_handler._get_all_students()
    return leads

@router.get("/{register_id}", response_model=ResponseLead)
async def get_lead_by_id(request: Request, register_id: int = Path(gt = 0)):
    """
    Retrieve a lead record by its ID from the database.

    Args:
        request (Request): The FastAPI request object, used for logging.
        register_id (int): The ID of the lead to retrieve. Must be greater than 0.

    Returns:
        ResponseLead: The lead record matching the provided ID.
    """
    logger = request.app.logger
    logger.info("Getting lead by ID {register_id}...")
    db_handler = DbHandler()
    lead = await db_handler._get_student_by_id(register_id)
    return lead
