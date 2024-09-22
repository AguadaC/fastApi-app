# -*- coding: utf-8 -*-
"""Api Record test"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from starlette import status
from datetime import datetime

from main import app
from challenge.core.db_handler import DbHandler
from challenge.models.sql_models import Student
from challenge.exceptions import (CareerDoesNotExist,
                                  SubjectDoesNotExist,
                                  CareerSubjectDoesNotExist)
from challenge.constants import DATA_INVALID


class ServiceTests(unittest.TestCase):
    """Test for Record API Endpoints"""

#==============================================================================
# Auxiliar data
    records_url    = "/records"

    record_creation = {
        "dni"         : "12345678",
        "name"        : "pepe",
        "email"       : "pepe@example.com",
        "phone"       : "+5433333333",
        "address"     : "pepe's house",
        "subject"     : "digital_electronic",
        "enroll_times": 4,
        "career"      : "electrical_engineering",
        "year_enroll" : 2024
    }

    invalid_record_creation = {
        "dni"  : "12345678",
        "name" : "invalid_pepe",
    }

#==============================================================================
# Auxiliar functions
    def raise_career_does_not_exist(career_name):
        raise CareerDoesNotExist("No Career with name:")

    def raise_subject_does_not_exist(subject_name):
        raise SubjectDoesNotExist("No Subject with name:")

    def raise_career_subject_does_not_exist(career_id, subject_id):
        raise CareerSubjectDoesNotExist("No Career-Subject with name:")

#==============================================================================
# Tests
    @patch.object(DbHandler, "_get_career_id_by_name", side_effect=raise_career_does_not_exist)
    @patch.object(DbHandler, "_get_student_id_by_dni")
    def test_load_record_unexisting_career(self, get_student, get_career):
        """Test request with CareerDoesNotExist exception"""
        with TestClient(app) as client:
            get_student.return_value = 4
            response = client.post(self.records_url,
                                   json=self.record_creation)
            assert response.status_code == status.HTTP_303_SEE_OTHER
            assert response.text == '{"detail":"No Career with name:"}'

    @patch.object(DbHandler, "_get_subject_id_by_name", side_effect=raise_subject_does_not_exist)
    @patch.object(DbHandler, "_get_student_career_by_ids")
    @patch.object(DbHandler, "_get_career_id_by_name")
    @patch.object(DbHandler, "_get_student_id_by_dni")
    def test_load_record_unexisting_subject(self,
                                            get_student,
                                            get_career,
                                            get_student_career,
                                            get_subject):
        """Test request with SubjectDoesNotExist exception"""
        with TestClient(app) as client:
            get_student.return_value = 4
            get_career.return_value =4
            get_student_career.return_value = 4
            response = client.post(self.records_url,
                                   json=self.record_creation)
            assert response.status_code == status.HTTP_303_SEE_OTHER
            assert response.text == '{"detail":"No Subject with name:"}'


    @patch.object(DbHandler, "_get_career_subject_id", side_effect=raise_career_subject_does_not_exist)
    @patch.object(DbHandler, "_get_subject_id_by_name")
    @patch.object(DbHandler, "_get_student_career_by_ids")
    @patch.object(DbHandler, "_get_career_id_by_name")
    @patch.object(DbHandler, "_get_student_id_by_dni")
    def test_load_rec_unexisting_career_subject(self,
                                                get_student,
                                                get_career,
                                                get_student_career,
                                                get_subject,
                                                get_career_subject):
        """Test request with CareerSubjectDoesNotExist exception"""
        with TestClient(app) as client:
            get_student.return_value = 4
            get_career.return_value =4
            get_student_career.return_value =4
            get_subject.return_value = 4
            response = client.post(self.records_url,
                                   json=self.record_creation)
            assert response.status_code == status.HTTP_303_SEE_OTHER
            assert response.text == '{"detail":"No Career-Subject with name:"}'

    @patch.object(DbHandler, "_get_subject_enrollment_id")
    @patch.object(DbHandler, "_get_career_subject_id")
    @patch.object(DbHandler, "_get_subject_id_by_name")
    @patch.object(DbHandler, "_get_student_career_by_ids")
    @patch.object(DbHandler, "_get_career_id_by_name")
    @patch.object(DbHandler, "_get_student_id_by_dni")
    def test_load_complete_record(self,
                                  get_student,
                                  get_career,
                                  get_student_career,
                                  get_subject,
                                  get_career_subject,
                                  get_subject_enrollment):
        """Test request for load complete record"""
        with TestClient(app) as client:
            get_student.return_value = 4
            get_career.return_value =4
            get_student_career.return_value =4
            get_subject.return_value = 4
            get_career_subject.return_value = 4
            get_subject_enrollment.return_value = 4
            response = client.post(self.records_url,
                                   json=self.record_creation)
            assert response.status_code == status.HTTP_200_OK
            assert response.text == '{"id":4}'

    def test_load_incomplete_record(self):
        """Test request to records with an invalid record"""
        with TestClient(app) as client:
            response = client.post(self.records_url,
                                   json=self.invalid_record_creation)
            assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
            assert response.text == f'"{DATA_INVALID}"'


if __name__ == '__main__':
    unittest.main()
