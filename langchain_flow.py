import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import logging
import re
from github import Github
import requests
import json
import base64

load_dotenv()

# Load environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

assert AZURE_OPENAI_ENDPOINT, "AZURE_OPENAI_ENDPOINT is not set."
assert AZURE_OPENAI_KEY, "AZURE_OPENAI_KEY is not set."
assert AZURE_OPENAI_MODEL, "AZURE_OPENAI_MODEL is not set."
assert AZURE_OPENAI_API_VERSION, "AZURE_OPENAI_API_VERSION is not set."

client = ChatCompletionsClient(
    endpoint=AZURE_OPENAI_ENDPOINT,
    credential=AzureKeyCredential(AZURE_OPENAI_KEY),
    api_version=AZURE_OPENAI_API_VERSION
)

# Constants for agent prompts
STORE_LISTING_FIELDS = [
    ("display_name", "Enter the extension's display name. It should be clear and related to the manifest name."),
    ("summary", "Write a concise tagline (max 132 characters) for the extension."),
    ("detailed_description", "Provide a full description of features, benefits, and usage. Use formatting for readability."),
    ("language", "Specify the primary language."),
    ("category", "Choose the most relevant category (e.g., Productivity, Developer Tools)."),
    ("official_website", "Provide the homepage or support page URL."),
    ("support_contact", "Provide a support contact (email or URL)."),
]

STORE_LISTING_EXAMPLE = '''{
  "display_name": "Tab Organizer",
  "summary": "Organize your tabs with one click.",
  "detailed_description": "Tab Organizer helps you manage and group your Chrome tabs efficiently. Features include...",
  "language": "en",
  "category": "Productivity",
  "official_website": "https://taborganizer.com",
  "support_contact": "support@taborganizer.com"
}'''

PRIVACY_PRACTICES_FIELDS = [
    ("single_purpose", "Clearly explain your extension's single core purpose."),
    ("permission_justifications", "For each permission, provide a detailed justification."),
    ("user_data_usage", "Disclose if and how user data is collected/used/shared."),
    ("privacy_policy_url", "Provide a direct link to your privacy policy."),
    ("remote_code", "Disclose if remote code is used."),
    ("content_security_policy", "State your Content Security Policy."),
]

PRIVACY_PRACTICES_EXAMPLE = '''{
  "single_purpose": "Tab Organizer helps users manage browser tabs.",
  "permission_justifications": {"tabs": "Needed to read and organize open tabs."},
  "user_data_usage": {"PII": "No", "analytics": "No"},
  "privacy_policy_url": "https://taborganizer.com/privacy",
  "remote_code": "No",
  "content_security_policy": "script-src 'self'; object-src 'none';"
}'''

DISTRIBUTION_FIELDS = [
    ("visibility", "Choose one: Public, Unlisted, Private."),
    ("countries", "List countries for distribution."),
    ("pricing_payments", "Describe pricing or payment setup if applicable."),
]

DISTRIBUTION_EXAMPLE = '''{
  "visibility": "Public",
  "countries": ["US", "CA", "GB"],
  "pricing_payments": "Free extension. No payments required."
}'''

STORE_LISTING_PROMPT = (
    "You are the Store Listing Agent. Fill out the Chrome Web Store 'Store Listing' tab.\n"
    "Based on the repository data provided, analyze the manifest.json, README.md, and repository information to fill out the store listing.\n"
    "For each of the following fields, provide a value as described. Return your answers as a JSON object with these keys: "
    f"{[field[0] for field in STORE_LISTING_FIELDS]}.\n"
    + "\n".join([f"- {field[0]}: {field[1]}" for field in STORE_LISTING_FIELDS]) +
    "\nIf a field is not applicable, use null or an empty string.\n"
    "Here is an example output:\n"
    f"{STORE_LISTING_EXAMPLE}"
)

PRIVACY_PRACTICES_PROMPT = (
    "You are the Privacy Practices Agent. Fill out the Chrome Web Store 'Privacy Practices' tab.\n"
    "Based on the repository data provided, analyze the manifest.json permissions, README.md, and any privacy-related files to assess privacy practices.\n"
    "Pay special attention to the permissions requested in manifest.json and any privacy policy or data handling documentation.\n"
    "For each of the following fields, provide a value as described. Return your answers as a JSON object with these keys: "
    f"{[field[0] for field in PRIVACY_PRACTICES_FIELDS]}.\n"
    + "\n".join([f"- {field[0]}: {field[1]}" for field in PRIVACY_PRACTICES_FIELDS]) +
    "\nIf a field is not applicable, use null or an empty string.\n"
    "Here is an example output:\n"
    f"{PRIVACY_PRACTICES_EXAMPLE}"
)

DISTRIBUTION_PROMPT = (
    "You are the Distribution Agent. Fill out the Chrome Web Store 'Distribution' tab.\n"
    "Based on the repository data provided, analyze the project's maturity, popularity (stars), and maintenance status (issues, last update).\n"
    "Consider the repository's visibility, documentation quality, and overall readiness for distribution.\n"
    "For each of the following fields, provide a value as described. Return your answers as a JSON object with these keys: "
    f"{[field[0] for field in DISTRIBUTION_FIELDS]}.\n"
    + "\n".join([f"- {field[0]}: {field[1]}" for field in DISTRIBUTION_FIELDS]) +
    "\nIf a field is not applicable, use null or an empty string.\n"
    "Here is an example output:\n"
    f"{DISTRIBUTION_EXAMPLE}"
)

MAX_TOKENS = 2048

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_github_url(url: str) -> tuple:
    """Extract owner and repo name from GitHub URL."""
    pattern = r"github\.com[/:]([^/]+)/([^/]+)"
    match = re.search(pattern, url)
    if not match:
        raise ValueError("Invalid GitHub repository URL")
    return match.group(1), match.group(2).rstrip('.git')

def get_file_content_safe(repo, path):
    """Safely get content of a file from GitHub repo."""
    try:
        content = repo.get_contents(path)
        return base64.b64decode(content.content).decode()
    except:
        return None

def analyze_github_repo(repo_url: str) -> str:
    """Analyze a GitHub repository and extract Chrome extension information."""
    try:
        owner, repo_name = parse_github_url(repo_url)
        g = Github()  # Using public access for public repositories
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        # Get manifest.json content
        manifest_content = get_file_content_safe(repo, "manifest.json")
        if not manifest_content:
            return "Error: manifest.json not found or invalid"
        
        manifest_data = json.loads(manifest_content)
        
        # Get README content
        readme_content = get_file_content_safe(repo, "README.md") or ""
        
        # Get package.json if it exists
        package_json = get_file_content_safe(repo, "package.json")
        dependencies = {}
        if package_json:
            try:
                package_data = json.loads(package_json)
                dependencies = {
                    "dependencies": package_data.get("dependencies", {}),
                    "devDependencies": package_data.get("devDependencies", {})
                }
            except:
                dependencies = {}
        
        # Get privacy policy if it exists
        privacy_policy = get_file_content_safe(repo, "PRIVACY.md") or \
                        get_file_content_safe(repo, "PRIVACY_POLICY.md") or \
                        get_file_content_safe(repo, "privacy.md") or \
                        get_file_content_safe(repo, "privacy-policy.md")
        
        # Get license if it exists
        license_content = get_file_content_safe(repo, "LICENSE") or \
                         get_file_content_safe(repo, "LICENSE.md") or \
                         get_file_content_safe(repo, "license.txt")
        
        # Create context from repository data
        context = {
            "name": manifest_data.get("name", ""),
            "version": manifest_data.get("version", ""),
            "description": manifest_data.get("description", ""),
            "manifest_version": manifest_data.get("manifest_version", ""),
            "permissions": manifest_data.get("permissions", []),
            "host_permissions": manifest_data.get("host_permissions", []),
            "content_scripts": manifest_data.get("content_scripts", []),
            "background": manifest_data.get("background", {}),
            "readme": readme_content,
            "dependencies": dependencies,
            "privacy_policy": privacy_policy,
            "license": license_content,
            "repo_url": repo_url,
            "stars": repo.stargazers_count,
            "last_updated": repo.updated_at.isoformat(),
            "open_issues": repo.open_issues_count,
            "default_locale": manifest_data.get("default_locale", ""),
            "icons": manifest_data.get("icons", {})
        }

        return json.dumps(context, indent=2)

    except Exception as e:
        logger.error(f"Error analyzing GitHub repository: {e}")
        return f"Error analyzing repository: {str(e)}"

def agent_tool(agent_prompt: str, user_input: str) -> str:
    messages = [
        SystemMessage(content=agent_prompt),
        UserMessage(content=user_input)
    ]
    try:
        response = client.complete(
            messages=messages,
            max_tokens=MAX_TOKENS,
            model=AZURE_OPENAI_MODEL
        )
        assert response.choices, "No response choices returned from agent."
        return response.choices[0].message.content
    except Exception as error:
        logger.error(f"Agent failed: {error}")
        return f"Error: {error}"

def run_agentic_flow(extension_context: str):
    logger.info("Starting Store Listing Agent...")
    store_listing_output = agent_tool(STORE_LISTING_PROMPT, extension_context)
    print("\n=== Store Listing Agent Output ===\n")
    print(store_listing_output)

    logger.info("Starting Privacy Practices Agent...")
    privacy_practices_output = agent_tool(PRIVACY_PRACTICES_PROMPT, extension_context)
    print("\n=== Privacy Practices Agent Output ===\n")
    print(privacy_practices_output)

    logger.info("Starting Distribution Agent...")
    distribution_output = agent_tool(DISTRIBUTION_PROMPT, extension_context)
    print("\n=== Distribution Agent Output ===\n")
    print(distribution_output)

if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL of your Chrome Extension: ")
    assert repo_url.strip(), "Repository URL must not be empty."
    
    print("\nAnalyzing repository...")
    extension_context = analyze_github_repo(repo_url)
    
    if extension_context.startswith("Error"):
        print(f"Failed to analyze repository: {extension_context}")
    else:
        print("\nRepository analysis complete. Running agent flow...")
        run_agentic_flow(extension_context)