# Create a TestClient using the FastAPI app
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from main import app

client = TestClient(app)

# Define a test function
def test_root_ok():
    response = client.get("/api")  # Send a GET request to the root endpoint
    assert response.status_code == HTTP_200_OK
