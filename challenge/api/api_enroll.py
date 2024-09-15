# -*- coding: utf-8 -*-
"""API Leads module"""

from fastapi import APIRouter, Request

from challenge.models.api_models import (EnrollStudentToCareer,
                                         EnrollStudentToSubject,
                                         ResponseStudentCareer,
                                         ResponseSubjectEnroll)
from challenge.core.db_handler import DbHandler


router = APIRouter()

@router.post("/career", response_model=ResponseStudentCareer)
async def enroll_student_in_a_career(request: Request, student_and_career: EnrollStudentToCareer):
    
    logger = request.app.logger
    logger.info("Enrolling Student in a Career...")
    db_handler = DbHandler()
    student_career_id = await db_handler.enroll_student_in_a_career(
        student_and_career.student_dni,
        student_and_career.career_name
    )
    return ResponseStudentCareer(id=student_career_id)

@router.post("/subject", response_model=ResponseSubjectEnroll)
async def enroll_student_in_a_subject(request: Request, student_career_subject: EnrollStudentToSubject):
    
    logger = request.app.logger
    logger.info("Enrolling Student in a Subject...")
    db_handler = DbHandler()
    student_career_subject_id = await db_handler.enroll_student_in_a_subject(
        student_career_subject.student_dni,
        student_career_subject.career_name,
        student_career_subject.subject_name
    )
    return ResponseStudentCareer(id=student_career_subject_id)
