<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# AI Itinerary Planner - Copilot Instructions

This is a full-stack travel itinerary planning application with a Python Flask backend and JavaScript frontend.

## Project Structure
- **Backend**: Flask API with modular services (weather, hotels, AI, user management)
- **Frontend**: Vanilla JavaScript with responsive CSS
- **APIs**: OpenWeatherMap, Gemini AI, Perplexity AI integration
- **Features**: User profiling, weather integration, hotel recommendations, AI-powered itinerary generation

## Key Components
- `app.py`: Main Flask application with API endpoints
- `services/`: Modular backend services for different functionalities
- `models/`: Data models and business logic
- `templates/`: HTML templates for the frontend
- `static/`: CSS and JavaScript files

## Development Guidelines
- Follow Flask best practices for API development
- Use modular service architecture for maintainability
- Implement proper error handling and fallback mechanisms
- Ensure responsive design for mobile compatibility
- Include accessibility considerations for users with health conditions

## API Integration
- Weather data from OpenWeatherMap API
- AI-powered content generation with Gemini/Perplexity
- Fallback systems for reliability when APIs are unavailable

## Code Style
- Use descriptive variable names and function names
- Add comprehensive error handling
- Include docstrings for all functions and classes
- Follow PEP 8 style guidelines for Python code
- Use consistent formatting for JavaScript and CSS
