# -*- coding: utf-8 -*-
"""Api Leads test"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from starlette import status
from datetime import datetime

from main import app
from challenge.core.db_handler import DbHandler
from challenge.models.sql_models import Student

class ServiceTests(unittest.TestCase):
    """Test for Leads API Endpoints"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    leads_url = "/leads"
    lead_by_id = "/leads/1"
    lead_by_id_0 = "/leads/0"

    leads_result = [
        Student(student_id=1,
                dni   = "12345678",
                name  = "pepe",
                email = "pepe@example.com",
                phone = "+5433333333",
                date  = datetime.now())
    ]

    lead_creation = {
        "dni"  : "12345678",
        "name" : "pepe",
        "email": "pepe@example.com",
        "phone": "+5433333333"
    }

    invalid_lead_creation = {
        "dni"  : 12345678,
        "name" : "invalid_pepe",
    }

    @patch.object(DbHandler, "get_all_students")
    def test_get_leads(self, get_students):
        """Test request to the leads endpoint"""
        with TestClient(app) as client:
            get_students.return_value = self.leads_result
            response = client.get(f"{self.leads_url}")
            assert response.status_code == status.HTTP_200_OK
            assert (
                response.json()[0]["student_id"] == self.leads_result[0].student_id)

    @patch.object(DbHandler, "get_student_by_id")
    def test_get_lead_by_id(self, get_students):
        """Test request to lead with valid ID endpoint"""
        with TestClient(app) as client:
            get_students.return_value = self.leads_result[0]
            response = client.get(f"{self.lead_by_id}")
            assert response.status_code == status.HTTP_200_OK
            assert (
                response.json()["student_id"] == self.leads_result[0].student_id)

    def test_get_lead_by_id_0(self):
        """Test request to lead with invalid ID endpoint"""
        with TestClient(app) as client:
            response = client.get(f"{self.lead_by_id_0}")
            assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    @patch.object(DbHandler, "create_student")
    def test_create_valid_lead(self, create_students):
        """Test valid student creation"""
        with TestClient(app) as client:
            create_students.return_value = self.leads_result[0].student_id
            response = client.post(f"{self.leads_url}", json=self.lead_creation)
            assert response.status_code == status.HTTP_200_OK
            assert (
                response.json()["student_id"] == self.leads_result[0].student_id)

    @patch.object(DbHandler, "create_student")
    def test_create_invalid_lead(self, create_students):
        """Test invalid student creation"""
        with TestClient(app) as client:
            response = client.post(f"{self.leads_url}", json=self.invalid_lead_creation)
            assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE


if __name__ == '__main__':
    unittest.main()
