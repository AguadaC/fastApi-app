# -*- coding: utf-8 -*-
"""API record module"""

from fastapi import APIRouter, Request, Path, Query
from typing import List

from challenge.models.api_models import (AddLeadRecord,
                                         ResponseSubjectEnroll,
                                         RetriveLeadRecord)
from challenge.core.db_handler import DbHandler
from challenge.exceptions import (StudentDoesNotExist,
                                  UnenrolledStudent)


router = APIRouter()

@router.post("/", response_model=ResponseSubjectEnroll)
async def load_complete_record(lead: AddLeadRecord, request: Request):
    """
    Load a complete record for a student lead.

    This endpoint processes a new lead record by performing the following steps:
    1. Checks if a student exists in the database by their DNI.
    2. If the student does not exist, creates a new student record with
       the provided information.
    3. Checks if the student is enrolled in the specified career.
    4. If the student is not enrolled, enrolls the student in the specified career.
    5. Enrolls the student in the specified subject within the career.

    Args:
        lead (AddLeadRecord): The lead record containing student information,
        including DNI, name, email, phone, address, subject, career, enrollment
        year, and time taken.
        request (Request): The FastAPI request object, used for logging
        and handling the request context.

    Returns:
        ResponseSubjectEnroll: A response containing the enrollment ID
        of the student in the subject.
    """
    logger = request.app.logger
    logger.info("Loading complete record...")
    db_handler = DbHandler()
    try:
        student_id = await db_handler._get_student_id_by_dni(dni=lead.dni)
    except StudentDoesNotExist:
        student_id = await db_handler._create_student(dni=lead.dni,
                                                     name=lead.name,
                                                     email=lead.email,
                                                     phone=lead.phone,
                                                     address=lead.address)
    career_id = await db_handler._get_career_id_by_name(lead.career)
    try:
        await db_handler._get_student_career_by_ids(student_id=student_id,
                                                career_id=career_id)
    except UnenrolledStudent:
        await db_handler._enroll_student_in_a_career(student_id=student_id,
                                                     career_id=career_id,
                                                     year_enroll=lead.year_enroll)
        
    subject_id = await db_handler._get_subject_id_by_name(subject_name=lead.subject)
    career_subject_id = await db_handler._get_career_subject_id(
                                            career_id=career_id,
                                            subject_id=subject_id)
    try:
        enroll_id = await db_handler._get_subject_enrollment_id(
                                            student_id=student_id,
                                            career_subject_id=career_subject_id,
                                            enroll_times=lead.enroll_times)
    except UnenrolledStudent:
        enroll_id = await db_handler._enroll_student_in_a_subject(
                                            student_id=student_id,
                                            career_subject_id=career_subject_id,
                                            enroll_times=lead.enroll_times)

    logger.info(f"Lead with DNI:{lead.dni} enrolled to {lead.subject} sucessfully")
    return {"id": enroll_id}

@router.get("/{record_id}", response_model=RetriveLeadRecord)
async def get_record_by_id(request: Request, record_id: int = Path(gt = 0)):
    """
    Retrieve a complete lead record by its ID.

    This endpoint fetches a lead record based on the provided record ID. 
    It retrieves the associated student information, career, subject, 
    and enrollment details, constructing a comprehensive response model.

    Args:
        request (Request): The FastAPI request object, used for logging.
        record_id (int): The ID of the lead record to retrieve.
        Must be greater than 0.

    Returns:
        RetriveLeadRecord: A model containing the details of the lead, 
        including student information, subject, career, and enrollment year.
    Raise:
        EnrollRecordDoesNotExist: When the record does not exist.
    """
    logger = request.app.logger
    logger.info("Getting complete record...")
    db_handler = DbHandler()
    record_built = await db_handler._build_record_by_id(record_id=record_id)
    return record_built

@router.get("/", response_model=List[RetriveLeadRecord])
async def get_all_records(request: Request,
                          start: int = Query(0, ge=0),
                          limit: int = Query(10, gt=0)):
    """
    Retrieve all complete records with pagination.

    Args:
        request (Request): The FastAPI request object, used for logging.
        start (int): The index to start fetching records from.
        Must be >= 0. Default is 0.
        limit (int): The maximum number of records to return.
        Must be > 0. Default is 10.

    Returns:
        List[RetriveLeadRecord]: A list of lead records starting from 'start' index
        up to 'limit'.
    """
    logger = request.app.logger
    logger.info(f"Getting complete records from {start} to {start + limit}...")
    db_handler = DbHandler()
    all_record_ids = await db_handler._get_all_record_ids()

    if start >= len(all_record_ids):
        return []
    paginated_ids = all_record_ids[start:start + limit]
    
    records_built = list()
    for record_id in paginated_ids:
        records_built.append(
            await db_handler._build_record_by_id(record_id=record_id)
        )
    return records_built
