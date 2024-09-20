# -*- coding: utf-8 -*-
"""Api Leads test"""

import unittest
from fastapi.testclient import TestClient
from starlette import status

from main import app


class ServiceTests(unittest.TestCase):
    """Test for Root API Endpoints"""

    root = "/"

    def test_get_root(self):
        """Test request to the root endpoint"""
        with TestClient(app) as client:
            response = client.get(f"{self.root}")
            assert response.status_code == status.HTTP_200_OK
            assert (
                response.json()["title"]
                == "You have reached out to the App"
            )
            assert list(response.json().keys()) == ["title", "detail", "docs"]


if __name__ == '__main__':
    unittest.main()
