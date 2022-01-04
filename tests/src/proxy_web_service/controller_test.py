from flask.testing import FlaskClient


def test_get_key(test_client: FlaskClient):
    """Test the get method of the local cache."""
    response = test_client.get("/proxy/", query_string={"key": "hello"})
    response2 = test_client.get("/proxy/", query_string={"key": "hello"})

    assert response.status_code == 200
    assert response.json == {"cached_value": "world"}
