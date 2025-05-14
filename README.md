# Chrome Extension Analyzer Agent Flow

This project demonstrates a multi-agent workflow using Azure OpenAI's ChatCompletions API that can analyze Chrome Extensions directly from their GitHub repositories. Simply provide a GitHub URL, and the system will automatically extract, analyze, and prepare your extension for the Chrome Web Store - no local files needed!

## Features

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
- **Store Listing Agent**: Handles all fields in the Chrome Web Store 'Store Listing' tab
- **Privacy Practices Agent**: Reviews privacy implications and required permissions
- **Distribution Agent**: Assesses distribution readiness and visibility options

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
1. Analyze the GitHub repository
2. Extract extension information
3. Generate store listing details
4. Review privacy practices
5. Assess distribution readiness

## Running Tests
To run the test suite:
```bash
pytest
```