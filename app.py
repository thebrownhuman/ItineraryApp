from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import our modular services
from services.weather_service import WeatherService
from services.hotel_service import HotelService
from services.ai_service import AIService
from services.user_service import UserService
from models.user_profile import UserProfile

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
CORS(app)

# Initialize services
weather_service = WeatherService()
hotel_service = HotelService()
ai_service = AIService()
user_service = UserService()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/user/create', methods=['POST'])
def create_user_profile():
    """Create a new user profile"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'travel_type', 'destination', 'days', 'interests']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create user profile
        profile = UserProfile(
            name=data['name'],
            travel_type=data['travel_type'],
            companions=data.get('companions', 1),
            health_conditions=data.get('health_conditions', []),
            destination=data['destination'],
            days=int(data['days']),
            interests=data['interests'],
            budget_range=data.get('budget_range', 'medium')
        )
        
        # Store user profile
        user_id = user_service.create_profile(profile)
        
        return jsonify({
            'message': 'User profile created successfully',
            'user_id': user_id,
            'profile': profile.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/<destination>')
def get_weather(destination):
    """Get weather information for destination"""
    try:
        weather_data = weather_service.get_weather(destination)
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hotels/<destination>')
def get_hotels(destination):
    """Get hotel recommendations for destination"""
    try:
        budget = request.args.get('budget', 'medium')
        companions = int(request.args.get('companions', 1))
        
        hotels = hotel_service.get_hotels(destination, budget, companions)
        return jsonify(hotels)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/itinerary/generate', methods=['POST'])
def generate_itinerary():
    """Generate personalized itinerary"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # Get user profile
        profile = user_service.get_profile(user_id)
        if not profile:
            return jsonify({'error': 'User profile not found'}), 404
        
        # Get weather data
        weather_data = weather_service.get_weather(profile.destination)
        
        # Get hotel recommendations
        hotels = hotel_service.get_hotels(
            profile.destination, 
            profile.budget_range, 
            profile.companions
        )
        
        # Generate AI-powered itinerary
        itinerary = ai_service.generate_itinerary(
            profile, 
            weather_data, 
            hotels
        )
        
        return jsonify({
            'itinerary': itinerary,
            'weather': weather_data,
            'hotels': hotels
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Itinerary App API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
