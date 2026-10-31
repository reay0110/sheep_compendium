import os
import sys

# Add the project root (sheep directory) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import TestClient to simulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)


# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON matches the expected data
    assert response.json() == {
        # Expected JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe",
    }


# Define a test function for adding a new sheep
def test_add_sheep():
    # Prepare the new sheep data in a dictionary format.
    # Marigold is the Suffolk ewe from the lab handout.
    sheep_data_name = {
        "id": 7,
        "name": "Marigold",
        "breed": "Suffolk",
        "sex": "ewe",
    }

    # Send a POST request to the endpoint "/sheep/" with the new sheep data.
    # Arguments should be your endpoint and new sheep data.
    response = client.post("/sheep/", json=sheep_data_name)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the response JSON matches the new sheep data
    assert response.json() == sheep_data_name

    # Verify that the sheep was actually added to the database by retrieving the new sheep by ID.
    # Include an assert statement to see if the new sheep data can be retrieved.
    get_response = client.get(f"/sheep/{sheep_data_name['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == sheep_data_name


def test_add_duplicate_sheep():
    # Spice is already stored under id 1, so a second insert is rejected.
    duplicate = {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe",
    }
    response = client.post("/sheep/", json=duplicate)
    assert response.status_code == 400


def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200

    sheep = response.json()
    assert isinstance(sheep, list)
    by_id = {item["id"]: item for item in sheep}
    assert {1, 2, 3, 4, 5, 6}.issubset(by_id)

    assert by_id[1] == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe",
    }


def test_update_sheep():
    # Blondie is stored as a ram. This request changes the sex and checks the write stuck.
    updated = {
        "id": 2,
        "name": "Blondie",
        "breed": "Polypay",
        "sex": "ewe",
    }
    response = client.put("/sheep/2", json=updated)
    assert response.status_code == 200
    assert response.json() == updated

    get_response = client.get("/sheep/2")
    assert get_response.status_code == 200
    assert get_response.json() == updated


def test_update_missing_sheep():
    missing = {
        "id": 99,
        "name": "Ghost",
        "breed": "Unknown",
        "sex": "ram",
    }
    response = client.put("/sheep/99", json=missing)
    assert response.status_code == 404


def test_delete_sheep():
    # Button is the Babydoll from the lab handout. Create it, then remove it.
    sheep_data_name = {
        "id": 8,
        "name": "Button",
        "breed": "Babydoll",
        "sex": "ram",
    }
    created = client.post("/sheep/", json=sheep_data_name)
    assert created.status_code == 201

    response = client.delete("/sheep/8")
    assert response.status_code == 200
    assert response.json() == sheep_data_name

    missing = client.get("/sheep/8")
    assert missing.status_code == 404


def test_delete_missing_sheep():
    response = client.delete("/sheep/99")
    assert response.status_code == 404
