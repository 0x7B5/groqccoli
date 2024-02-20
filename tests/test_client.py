import pytest
from unittest.mock import patch, MagicMock
from groqccoli import Client


@pytest.fixture
def client():
    return Client()


@patch("client_module.requests.post")
def test_create_chat(mock_post, client):
    # Mock response from the API
    mock_response = MagicMock()
    mock_response.iter_lines.return_value = iter(
        [
            '{"result": {"content": "Response Content", "stats": {"timeGenerated": 10, "tokensGenerated": 20, "timeProcessed": 30, "tokensProcessed": 40}}}'
        ]
    )
    mock_post.return_value = mock_response

    # Call the method
    chat = client.create_chat("User Prompt")

    # Assertions
    assert chat.content == "Response Content"
    assert chat.stats.time_generated == 10
    assert chat.stats.tokens_generated == 20
    assert chat.stats.time_processed == 30
    assert chat.stats.tokens_processed == 40


@patch("client_module.requests.get")
def test_get_anon_token(mock_get, client):
    # Mock response from the API
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "Mocked Access Token"}
    mock_get.return_value = mock_response

    # Call the method
    anon_token = client._get_anon_token()

    # Assertions
    assert anon_token == "Mocked Access Token"


def test_get_user_agent(client):
    # Call the method
    user_agent = client._get_user_agent()

    # Assertions
    assert isinstance(user_agent, str)
    assert len(user_agent) > 0
