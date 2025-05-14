import pytest
from unittest.mock import patch, MagicMock
import langchain_flow
import json
import base64

@pytest.fixture(autouse=True)
def patch_client_complete(monkeypatch):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="mocked output"))]
    monkeypatch.setattr(langchain_flow.client, "complete", lambda *args, **kwargs: mock_response)
    yield

def test_agent_tool_success():
    agent_prompt = "Test Agent Prompt"
    user_input = "Test user input"
    output = langchain_flow.agent_tool(agent_prompt, user_input)
    assert output == "mocked output"

def test_agent_tool_no_choices(monkeypatch):
    def mock_complete(*args, **kwargs):
        mock_response = MagicMock()
        mock_response.choices = []
        return mock_response
    monkeypatch.setattr(langchain_flow.client, "complete", mock_complete)
    result = langchain_flow.agent_tool("Prompt", "Input")
    assert result.startswith("Error:")

def test_agent_tool_exception(monkeypatch):
    def mock_complete(*args, **kwargs):
        raise RuntimeError("Test error")
    monkeypatch.setattr(langchain_flow.client, "complete", mock_complete)
    result = langchain_flow.agent_tool("Prompt", "Input")
    assert result.startswith("Error:")

def test_run_agentic_flow_prints_outputs(capsys):
    context = "Test extension context"
    langchain_flow.run_agentic_flow(context)
    captured = capsys.readouterr()
    assert "Store Listing Agent Output" in captured.out
    assert "Privacy Practices Agent Output" in captured.out
    assert "Distribution Agent Output" in captured.out
    assert "mocked output" in captured.out

def test_parse_github_url_valid():
    url = "https://github.com/owner/repo"
    owner, repo = langchain_flow.parse_github_url(url)
    assert owner == "owner"
    assert repo == "repo"

def test_parse_github_url_invalid():
    with pytest.raises(ValueError):
        langchain_flow.parse_github_url("https://invalid-url.com")

@pytest.fixture
def mock_github_repo():
    mock_repo = MagicMock()
    mock_repo.stargazers_count = 100
    mock_repo.updated_at.isoformat.return_value = "2024-05-13T00:00:00Z"
    mock_repo.open_issues_count = 5

    manifest_content = MagicMock()
    manifest_content.content = base64.b64encode(json.dumps({
        "name": "Test Extension",
        "version": "1.0.0",
        "description": "A test extension",
        "manifest_version": 3,
        "permissions": ["tabs"]
    }).encode()).decode()

    readme_content = MagicMock()
    readme_content.content = base64.b64encode("# Test Extension\nThis is a test.".encode()).decode()

    mock_repo.get_contents = MagicMock(side_effect=lambda path: {
        "manifest.json": manifest_content,
        "README.md": readme_content
    }[path])

    return mock_repo

@pytest.fixture
def mock_github(mock_github_repo):
    with patch('github.Github') as mock_g:
        mock_g.return_value.get_repo.return_value = mock_github_repo
        yield mock_g

def test_analyze_github_repo_success(mock_github):
    result = langchain_flow.analyze_github_repo("https://github.com/owner/repo")
    result_json = json.loads(result)
    
    assert result_json["name"] == "Test Extension"
    assert result_json["version"] == "1.0.0"
    assert result_json["description"] == "A test extension"
    assert result_json["manifest_version"] == 3
    assert result_json["permissions"] == ["tabs"]
    assert result_json["stars"] == 100
    assert result_json["open_issues"] == 5

def test_analyze_github_repo_no_manifest(mock_github):
    mock_github.return_value.get_repo.return_value.get_contents.side_effect = Exception("File not found")
    result = langchain_flow.analyze_github_repo("https://github.com/owner/repo")
    assert result.startswith("Error")