# AI Itinerary Planner

A comprehensive travel itinerary planning application that uses AI to create personalized travel plans based on user preferences, health conditions, weather forecasts, and budget considerations.

## Features

### 🎯 **Personalized Planning**
- Collects detailed user information (name, travel type, health conditions, interests)
- Supports solo travelers, couples, and groups
- Considers accessibility needs based on health conditions

### 🌤️ **Weather Integration** 
- Real-time weather data from Open-Meteo API (completely free!)
- 7-day weather forecast for destination
- Weather-based activity recommendations
- Clothing and packing suggestions

### 🏨 **Smart Hotel Recommendations**
- Budget-based hotel filtering (low, medium, high)
- Accessibility-compliant accommodations
- Rating and amenity-based suggestions
- Capacity matching for group size

### 🤖 **AI-Powered Itineraries**
- Integration with Gemini AI and Perplexity AI
- Fallback rule-based system for reliability
- Day-by-day activity planning
- Meal and dining recommendations
- Budget estimation and breakdown

### 💼 **Comprehensive Recommendations**
- Packing lists based on weather and activities
- Travel tips and safety considerations
- Budget breakdowns and cost estimates
- Accessibility accommodations

## Technology Stack

### Backend (Python Flask)
- **Flask**: Web framework for API development
- **Flask-CORS**: Cross-origin resource sharing
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for external APIs
- **google-generativeai**: Gemini AI integration

### Frontend (JavaScript/HTML/CSS)
- **Vanilla JavaScript**: Interactive user interface
- **Responsive CSS**: Mobile-friendly design
- **Font Awesome**: Icon library
- **Modern CSS Grid/Flexbox**: Layout system

### External APIs
- **Open-Meteo**: Free weather data and forecasts (no API key required!)
- **Google Gemini AI**: AI-powered itinerary generation (optional)
- **Perplexity AI**: Alternative AI service (optional)

## Project Structure

```
itenery_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── models/
│   ├── __init__.py
│   └── user_profile.py   # User data model
├── services/
│   ├── __init__.py
│   ├── weather_service.py    # Weather API integration
│   ├── hotel_service.py      # Hotel recommendations
│   ├── ai_service.py         # AI itinerary generation
│   └── user_service.py       # User management
├── templates/
│   └── index.html        # Main application template
└── static/
    ├── css/
    │   └── style.css     # Application styles
    └── js/
        └── app.js        # Frontend JavaScript
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd itenery_app
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
copy .env.example .env  # On Windows
# cp .env.example .env  # On macOS/Linux
```

Edit `.env` file and add your API keys:
```env
# NO API KEYS REQUIRED - Using completely free APIs!
GEMINI_API_KEY=your_gemini_api_key_here_optional
PERPLEXITY_API_KEY=your_perplexity_api_key_here_optional
FLASK_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
```

### 5. API Key Setup (Optional)

#### Weather Data
✅ **No setup required!** The app uses **Open-Meteo API** which is completely free and requires no registration or API keys.

#### AI Services (Optional - for enhanced itineraries)
1. **Google Gemini AI** (Optional): Get API key at [Google AI Studio](https://aistudio.google.com/)
2. **Perplexity AI** (Optional): Get API key at [perplexity.ai](https://www.perplexity.ai/)

**Note**: The app works completely without any API keys! Weather data comes from Open-Meteo (free), and there's a built-in rule-based itinerary system. AI APIs just make the itineraries more creative and detailed.

### 6. Run the Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## API Endpoints

### User Management
- **POST** `/api/user/create` - Create user profile
- **GET** `/api/user/<user_id>` - Get user profile

### Weather Service
- **GET** `/api/weather/<destination>` - Get weather forecast

### Hotel Service
- **GET** `/api/hotels/<destination>?budget=<range>&companions=<number>` - Get hotel recommendations

### Itinerary Generation
- **POST** `/api/itinerary/generate` - Generate complete itinerary

### Health Check
- **GET** `/api/health` - Service health status

## Usage Guide

### 1. Personal Information
- Enter your name
- Select travel type (alone, couple, group)
- Specify number of companions
- Indicate any health conditions for accessibility planning

### 2. Travel Details
- Enter destination city
- Specify trip duration (1-30 days)
- Select budget range (low, medium, high)

### 3. Interests & Preferences
- Choose from 8 interest categories:
  - Museums & Galleries
  - Parks & Nature
  - Food & Dining
  - Shopping
  - Nightlife
  - Beaches
  - Adventure Sports
  - Culture & History

### 4. Generated Itinerary
- View weather forecast and recommendations
- Browse recommended hotels with amenities
- Review day-by-day itinerary with activities
- Get packing lists and travel tips
- See budget estimates and breakdowns

## Features in Detail

### Health Condition Support
The application considers various health conditions:
- **Mobility Issues**: Wheelchair accessible venues, elevator access
- **Heart Conditions**: Low-intensity activities, nearby medical facilities
- **Respiratory Issues**: Air quality considerations, altitude restrictions

### Budget Planning
Three budget tiers with different daily estimates:
- **Low Budget**: ₹2,000-4,000/day (meals: ₹1,200, activities: ₹800, transport: ₹600)
- **Medium Budget**: ₹4,000-8,000/day (meals: ₹2,000, activities: ₹1,600, transport: ₹1,000)
- **High Budget**: ₹8,000+/day (meals: ₹3,200, activities: ₹2,800, transport: ₹1,600)

### AI Integration
- **Primary**: Gemini AI for natural language processing
- **Secondary**: Perplexity AI as backup service
- **Fallback**: Rule-based system ensures functionality without AI APIs

## Development

### Adding New Features
1. **Services**: Add new service files in `/services/` directory
2. **Models**: Define data models in `/models/` directory
3. **API Endpoints**: Add routes in `app.py`
4. **Frontend**: Update templates and static files

### Testing
The application includes error handling and fallback mechanisms:
- API failures gracefully fallback to alternative services
- Form validation prevents invalid submissions
- Weather and hotel data includes mock data for testing

### Deployment Considerations
- Set `FLASK_DEBUG=False` in production
- Use a production WSGI server (gunicorn, uwsgi)
- Implement proper database storage (currently uses in-memory storage)
- Add authentication and user sessions for multi-user support

## Troubleshooting

### Common Issues
1. **API Key Errors**: Verify all API keys are correctly set in `.env`
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Port Conflicts**: Change the port in `app.py` if 5000 is in use
4. **Weather Data**: App works with mock data if OpenWeatherMap API is unavailable

### Error Messages
- The application provides user-friendly error messages
- Check browser console for detailed error information
- Review Flask server logs for backend issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please refer to the LICENSE file for details.

## Support

For issues, questions, or contributions, please create an issue in the project repository.

---

**Happy Travels!** 🌍✈️
