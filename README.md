# Agentic Flow to Fill Out Chrome Extension Submission Forms

This project demonstrates a multi-agent workflow using Azure OpenAI's ChatCompletions API that can analyze Chrome Extensions directly from their GitHub repositories and supply the requisite fields to get submission approval in the Chrome Web Store. 

## Features

### Automated Form Submission Preparation
- **Complete Store Listing**: Automatically generates all required store listing fields
- **Privacy Documentation**: Creates privacy-related documentation and justifications
- **Distribution Setup**: Determines optimal distribution settings based on extension analysis
- **Submission Readiness**: Helps fill all Chrome Web Store requirements before submission

### Seamless GitHub Integration
- **Zero Local Setup**: Analyze any Chrome Extension directly from its GitHub repository - no cloning required
- **Smart File Detection**: Automatically finds and parses key files like manifest.json, README.md, and privacy policies
- **Deep Repository Analysis**: Examines repository metadata, stars, issues, and update frequency to assess project health
- **Comprehensive Dependency Analysis**: Automatically detects and analyzes package.json dependencies

### Chrome Extension Analysis
- Analyzes Chrome Extensions directly from GitHub repositories
- Extracts and validates manifest.json
- Reviews permissions and privacy implications
- Assesses distribution readiness
- Analyzes dependencies and code structure

### Multi-Agent Workflow
- **Store Listing Agent**: Crafts compelling store listings with accurate descriptions, categories, and metadata
- **Privacy Practices Agent**: Generates comprehensive privacy documentation and permission justifications
- **Distribution Agent**: Recommends optimal visibility settings and distribution strategy

## Tools and Frameworks Used
- **Azure OpenAI Service**: Provides access to powerful language models via Azure's cloud platform
- **Azure AI Inference**: Python SDK for interacting with Azure OpenAI models
- **PyGithub**: For GitHub repository analysis

## Requirements
- Python 3.8+
- Azure OpenAI resource and deployment
- GitHub access for repository analysis

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with:
   ```env
   AZURE_OPENAI_ENDPOINT=<your-azure-openai-endpoint>
   AZURE_OPENAI_KEY=<your-azure-openai-key>
   AZURE_OPENAI_MODEL=<your-deployment-name>
   AZURE_OPENAI_API_VERSION=<api-version>
   ```

## Usage
Run the main script and provide a GitHub repository URL when prompted:
```bash
python agent_flow.py
```

The script will:
1. Analyze the GitHub repository and extract extension details
2. Generate a complete store listing with compelling descriptions
3. Create detailed privacy documentation and permission justifications
4. Recommend optimal distribution settings
5. Provide submission-ready content for all Chrome Web Store form fields

This automated process saves hours of manual form filling and ensures all Chrome Web Store requirements are met. Simply copy the generated content into the corresponding store submission forms.

## Example

Here's an example of analyzing a simple Chrome extension that adds dark mode to websites:

```bash
$ python agent_flow.py
Enter GitHub repository URL: https://github.com/example/dark-mode-extension

Analyzing repository...
✓ Repository analysis complete
✓ Manifest.json validated
✓ Dependencies analyzed
✓ Privacy implications reviewed

Generated Extension Data (JSON):
------------------------
{
    "store_listing": {
        "name": "Dark Mode Pro",
        "short_description": "Transform any website into a comfortable dark theme with one click.",
        "detailed_description": "Dark Mode Pro intelligently converts websites to dark mode while preserving readability and design integrity. Perfect for night-time browsing and reducing eye strain.",
        "category": "Accessibility"
    },
    "privacy": {
        "permissions": {
            "activeTab": {
                "justification": "Required to modify current webpage's styling",
                "data_access": "DOM elements and styles only",
                "data_retention": "None - modifications are temporary"
            }
        },
        "data_collection": null,
        "external_apis": [],
        "storage": {
            "type": "local",
            "purpose": "User preferences only",
            "data_stored": ["theme_settings", "enabled_status"]
        }
    },
    "distribution": {
        "visibility": "Public",
        "target_regions": "*",
        "pricing": {
            "model": "Free",
            "trial_period": null
        },
        "update_frequency": "As needed"
    }

All required fields have been generated and are ready to copy into the Chrome Web Store submission form.
```

This example shows how the tool:
1. Analyzes a Chrome extension repository
2. Generates appropriate store listing content
3. Creates privacy documentation based on the extension's permissions
4. Recommends distribution settings
5. Provides submission-ready content formatted for the Chrome Web Store

The generated content can be directly copied into the Chrome Web Store Developer Dashboard for submission.