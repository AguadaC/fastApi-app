# -*- coding: utf-8 -*-
"""Custom unit exceptions."""

from challenge.constants import DEFAULT_ERROR_MESSAGE


class BaseError(Exception):
    """All exceptions must extend this class."""

    def __init__(self, message=DEFAULT_ERROR_MESSAGE):
        """Construct message."""
        self.message = message


class StudentAlreadyExists(BaseError):
    """Exception that occurs when the student that is wanted to create, exists"""
    pass


class StudentDoesNotExist(BaseError):
    """Exception that occurs when the student_id doesn't exist in the database"""
    pass


class StudentCareerEnroll(BaseError):
    """Exception that occurs when the student is enrolled in the career"""
    pass


class UnenrolledStudent(BaseError):
    """Exception that occurs when the student is not enrolled"""
    pass


class CareerDoesNotExist(BaseError):
    """Exception that occurs when the career does not exist"""
    pass


class StudentSubjectEnroll(BaseError):
    """Exception that occurs when the student is enrolled in the subject"""
    pass


class SubjectDoesNotExist(BaseError):
    """Exception that occurs when the subject does not exist"""
    pass


class CareerSubjectDoesNotExist(BaseError):
    """Exception that occurs when the subject and the career are not related"""
    pass

class EnrollRecordDoesNotExist(BaseError):
    """Exception that occurs when the enroll record does not exist"""
    pass
