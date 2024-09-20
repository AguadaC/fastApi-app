# -*- coding: utf-8 -*-
"""API Models module."""

from pydantic import BaseModel, ConfigDict


class CreateLeadModel(BaseModel):
    """Student information"""
    dni: str
    name: str
    email: str
    phone: str

class EnrollStudentToCareer(BaseModel):
    """Enroll Student in a Career"""
    student_dni: str
    career_name: str

class EnrollStudentToSubject(BaseModel):
    """Enroll Student in a Subject"""
    student_dni: str
    career_name: str
    subject_name: str

class ResponseLead(BaseModel):
    """Student model for response"""
    student_id: int
    dni: str
    name: str
    email: str
    phone: str
    model_config = ConfigDict(from_attributes=True)

class ResponseLeadId(BaseModel):
    """Created Student's Id"""
    student_id: int
    model_config = ConfigDict(from_attributes=True)

class ResponseStudentCareer(BaseModel):
    """Created Student's Id"""
    id: int
    model_config = ConfigDict(from_attributes=True)

class ResponseSubjectEnroll(BaseModel):
    """Subject enrollment Id"""
    id: int
    model_config = ConfigDict(from_attributes=True)

class WelcomeModel(BaseModel):
    """Model for root path"""

    title: str
    detail: str
    docs: str
