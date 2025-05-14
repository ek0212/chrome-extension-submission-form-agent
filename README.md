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