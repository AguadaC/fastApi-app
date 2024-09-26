# -*- coding: utf-8 -*-
"""API Enroll module"""

from fastapi import APIRouter, Request

from challenge.models.api_models import (EnrollStudentToCareer,
                                         EnrollStudentToSubject,
                                         ResponseStudentCareer,
                                         ResponseSubjectEnroll)
from challenge.exceptions import (StudentCareerEnroll,
                                  UnenrolledStudent)
from challenge.core.db_handler import DbHandler


router = APIRouter()

@router.post("/career", response_model=ResponseStudentCareer)
async def enroll_student_in_a_career(request: Request,
                                     student_and_career: EnrollStudentToCareer):
    """
    Enroll a student in a specified career.

    This endpoint allows the enrollment of a student in a career based on
    the student's DNI and the career name provided.

    Args:
        request (Request): The FastAPI request object, used for logging.
        student_and_career (EnrollStudentToCareer): The data model containing
        the student's DNI, career name, and enrollment year.

    Raises:
        StudentCareerEnroll: If the student is already enrolled in the specified career.

    Returns:
        ResponseStudentCareer: An object containing the ID of the newly
        created student-career enrollment record.
    """
    logger = request.app.logger
    logger.info("Enrolling Student in a Career...")
    db_handler = DbHandler()
    student_id = await db_handler._get_student_id_by_dni(dni=student_and_career.student_dni)
    career_id = await db_handler._get_career_id_by_name(name=student_and_career.career_name)
    try:
        await db_handler._get_student_career_by_ids(student_id=student_id,
                                                    career_id=career_id)
        message_to_send = (
            f"Student with DNI: {student_and_career.student_dni} "
            f"is already enrolled in {student_and_career.career_name}"
            )
        logger.info(message_to_send)
        raise StudentCareerEnroll(message_to_send)

    except UnenrolledStudent:
        student_career_id = await db_handler._enroll_student_in_a_career(
        student_id=student_id,
        career_id=career_id,
        year_enroll=student_and_career.year_enroll
    )
    logger.info(f"New student-carrer ID: {student_career_id}")
    return ResponseStudentCareer(id=student_career_id)

@router.post("/subject", response_model=ResponseSubjectEnroll)
async def enroll_student_in_a_subject(request: Request,
                                      student_career_subject: EnrollStudentToSubject):
    """
    Enroll a student in a specified subject within their career.

    This endpoint allows the enrollment of a student in a specific subject
    based on the student's DNI, the career name, and the subject name provided.

    Args:
        request (Request): The FastAPI request object, used for logging.
        student_career_subject (EnrollStudentToSubject): The data model containing
        the student's DNI, career name, subject name, and enrollment times.

    Returns:
        ResponseSubjectEnroll: An object containing the ID of the newly
        created student-subject enrollment record.
    """
    logger = request.app.logger
    logger.info("Enrolling Student in a Subject...")
    db_handler = DbHandler()
    student_id = await db_handler._get_student_id_by_dni(dni=student_career_subject.student_dni)
    career_id = await db_handler._get_career_id_by_name(name=student_career_subject.career_name)
    await db_handler._get_student_career_by_ids(student_id=student_id, career_id=career_id)
    subject_id = await db_handler._get_subject_id_by_name(subject_name=student_career_subject.subject_name)
    career_subject_id = await db_handler._get_career_subject_id(career_id=career_id,
                                                                subject_id=subject_id)
    student_career_subject_id = await db_handler._enroll_student_in_a_subject(
                                student_id=student_id,
                                career_subject_id=career_subject_id,
                                enroll_times=student_career_subject.enroll_times)
    logger.info(
        f"Student with ID {student_id} was enrolled in "
        f"Subject {student_career_subject.subject_name}")
    return ResponseStudentCareer(id=student_career_subject_id)
