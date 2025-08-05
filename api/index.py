from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys
import json
import requests
import google.generativeai as genai
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-vercel')
CORS(app)

# Gemini AI Configuration
GEMINI_API_KEY = "AIzaSyALVGrgZqTECJZFwPDApEISygwIUEbxjuE"
genai.configure(api_key=GEMINI_API_KEY)

# Mock data and services embedded directly
class WeatherService:
    def get_weather(self, destination):
        # Open-Meteo API for free weather data
        try:
            # First get coordinates for the destination
            geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={destination}&count=1&language=en&format=json"
            geo_response = requests.get(geocoding_url, timeout=10)
            geo_data = geo_response.json()
            
            if not geo_data.get('results'):
                return self._get_fallback_weather(destination)
            
            location = geo_data['results'][0]
            lat, lon = location['latitude'], location['longitude']
            
            # Get weather data
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=auto"
            weather_response = requests.get(weather_url, timeout=10)
            weather_data = weather_response.json()
            
            current = weather_data['current']
            daily = weather_data['daily']
            
            # Map weather codes to descriptions
            weather_descriptions = {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
                55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain"
            }
            
            return {
                "destination": destination,
                "temperature": round(current['temperature_2m']),
                "description": weather_descriptions.get(current['weather_code'], "Unknown"),
                "humidity": current['relative_humidity_2m'],
                "wind_speed": round(current['wind_speed_10m']),
                "humidity_description": self._get_humidity_description(current['relative_humidity_2m']),
                "wind_description": self._get_wind_description(current['wind_speed_10m']),
                "forecast": [
                    {
                        "day": f"Day {i+1}",
                        "high": round(daily['temperature_2m_max'][i]),
                        "low": round(daily['temperature_2m_min'][i]),
                        "description": weather_descriptions.get(daily['weather_code'][i], "Unknown")
                    } for i in range(min(5, len(daily['temperature_2m_max'])))
                ]
            }
            
        except Exception as e:
            return self._get_fallback_weather(destination)
    
    def _get_humidity_description(self, humidity):
        if humidity < 40:
            return "Low (Dry)"
        elif humidity < 70:
            return "Moderate"
        else:
            return "High (Humid)"
    
    def _get_wind_description(self, wind_speed):
        if wind_speed < 10:
            return "Light breeze"
        elif wind_speed < 20:
            return "Moderate wind"
        else:
            return "Strong wind"
    
    def _get_fallback_weather(self, destination):
        return {
            "destination": destination,
            "temperature": 22,
            "description": "Partly cloudy",
            "humidity": 65,
            "wind_speed": 8,
            "humidity_description": "Moderate",
            "wind_description": "Light breeze",
            "forecast": [
                {"day": "Day 1", "high": 25, "low": 18, "description": "Sunny"},
                {"day": "Day 2", "high": 23, "low": 16, "description": "Partly cloudy"},
                {"day": "Day 3", "high": 26, "low": 19, "description": "Clear"},
                {"day": "Day 4", "high": 24, "low": 17, "description": "Cloudy"},
                {"day": "Day 5", "high": 22, "low": 15, "description": "Light rain"}
            ]
        }

class HotelService:
    def __init__(self):
        self.hotels = [
            {
                "name": "Grand Palace Hotel",
                "location": "City Center",
                "rating": 4.8,
                "price_per_night": 8500,
                "amenities": ["WiFi", "Pool", "Gym", "Spa", "Restaurant", "Room Service", "Parking"],
                "description": "Luxury hotel in the heart of the city with premium amenities and world-class service.",
                "distance_to_center": 0.5,
                "address": "123 Central Avenue, Downtown District",
                "google_maps_url": "https://maps.google.com/?q=Grand+Palace+Hotel+City+Center",
                "booking_sites": [
                    {"name": "Booking.com", "url": "https://booking.com/"},
                    {"name": "Expedia", "url": "https://expedia.com/"},
                    {"name": "Hotels.com", "url": "https://hotels.com/"}
                ],
                "tripadvisor_rating": "4.5/5",
                "accessibility_features": ["Wheelchair accessible", "Elevator", "Accessible parking"]
            },
            {
                "name": "Boutique Garden Inn",
                "location": "Arts Quarter",
                "rating": 4.6,
                "price_per_night": 6200,
                "amenities": ["WiFi", "Garden", "Restaurant", "Bar", "Laundry", "Concierge"],
                "description": "Charming boutique hotel with beautiful gardens and personalized service.",
                "distance_to_center": 1.2,
                "address": "456 Garden Street, Arts Quarter",
                "google_maps_url": "https://maps.google.com/?q=Boutique+Garden+Inn+Arts+Quarter",
                "booking_sites": [
                    {"name": "Airbnb", "url": "https://airbnb.com/"},
                    {"name": "Booking.com", "url": "https://booking.com/"},
                    {"name": "TripAdvisor", "url": "https://tripadvisor.com/"}
                ],
                "tripadvisor_rating": "4.3/5",
                "accessibility_features": ["Ground floor rooms", "Wide doorways"]
            },
            {
                "name": "Business Executive Suites",
                "location": "Financial District",
                "rating": 4.4,
                "price_per_night": 7200,
                "amenities": ["WiFi", "Business Center", "Gym", "Restaurant", "Meeting Rooms", "Airport Shuttle"],
                "description": "Modern business hotel perfect for corporate travelers with excellent facilities.",
                "distance_to_center": 2.0,
                "address": "789 Business Plaza, Financial District",
                "google_maps_url": "https://maps.google.com/?q=Business+Executive+Suites+Financial+District",
                "booking_sites": [
                    {"name": "Corporate Travel", "url": "https://booking.com/"},
                    {"name": "Expedia", "url": "https://expedia.com/"},
                    {"name": "Hotels.com", "url": "https://hotels.com/"}
                ],
                "tripadvisor_rating": "4.2/5",
                "accessibility_features": ["Business center", "Conference facilities", "Accessible bathrooms"]
            },
            {
                "name": "Coastal View Resort",
                "location": "Waterfront",
                "rating": 4.7,
                "price_per_night": 9500,
                "amenities": ["WiFi", "Beach Access", "Pool", "Spa", "Water Sports", "Restaurant", "Bar"],
                "description": "Stunning waterfront resort with breathtaking views and luxury amenities.",
                "distance_to_center": 3.5,
                "address": "321 Coastal Highway, Waterfront District",
                "google_maps_url": "https://maps.google.com/?q=Coastal+View+Resort+Waterfront",
                "booking_sites": [
                    {"name": "Resort Direct", "url": "https://booking.com/"},
                    {"name": "Expedia", "url": "https://expedia.com/"},
                    {"name": "TripAdvisor", "url": "https://tripadvisor.com/"}
                ],
                "tripadvisor_rating": "4.6/5",
                "accessibility_features": ["Beach wheelchair", "Pool lift", "Accessible rooms"]
            }
        ]
    
    def get_hotels(self, destination, budget='medium', companions=1):
        try:
            # Price adjustments based on budget
            budget_multipliers = {'low': 0.7, 'medium': 1.0, 'high': 1.5}
            multiplier = budget_multipliers.get(budget, 1.0)
            
            # Adjust prices and filter based on budget
            adjusted_hotels = []
            for hotel in self.hotels:
                adjusted_hotel = hotel.copy()
                adjusted_hotel['price_per_night'] = int(hotel['price_per_night'] * multiplier)
                adjusted_hotels.append(adjusted_hotel)
            
            return adjusted_hotels
            
        except Exception as e:
            return []

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_itinerary(self, profile, weather_data, hotels):
        try:
            prompt = f"""
            Create a detailed travel itinerary for {profile['days']} days in {profile['destination']} for {profile['name']}.
            
            Traveler Profile:
            - Name: {profile['name']}
            - Travel Type: {profile['travel_type']}
            - Companions: {profile.get('companions', 1)}
            - Interests: {', '.join(profile['interests'])}
            - Budget: {profile.get('budget_range', 'medium')}
            - Health Considerations: {', '.join(profile.get('health_conditions', [])) if profile.get('health_conditions') else 'None'}
            
            Current Weather: {weather_data['temperature']}°C, {weather_data['description']}
            
            Please create a day-by-day itinerary with:
            1. Morning, afternoon, and evening activities
            2. Specific places to visit based on interests
            3. Local food recommendations
            4. Transportation tips
            5. Budget-conscious suggestions for {profile.get('budget_range', 'medium')} budget
            6. Weather-appropriate activities
            
            Format as JSON with this structure:
            {
                "days": [
                    {
                        "day": 1,
                        "title": "Day title",
                        "morning": "Morning activities",
                        "afternoon": "Afternoon activities", 
                        "evening": "Evening activities",
                        "food_recommendations": ["restaurant1", "restaurant2"],
                        "transportation": "Transportation info",
                        "budget_tips": "Budget advice"
                    }
                ]
            }
            """
            
            response = self.model.generate_content(prompt)
            
            # Try to parse JSON from response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            try:
                itinerary_data = json.loads(response_text)
                return itinerary_data
            except json.JSONDecodeError:
                # Fallback to simple parsing if JSON fails
                return self._create_fallback_itinerary(profile, weather_data)
                
        except Exception as e:
            return self._create_fallback_itinerary(profile, weather_data)
    
    def _create_fallback_itinerary(self, profile, weather_data):
        days_data = []
        for day in range(1, profile['days'] + 1):
            days_data.append({
                "day": day,
                "title": f"Explore {profile['destination']} - Day {day}",
                "morning": f"Visit local attractions and {profile['interests'][0] if profile['interests'] else 'sightseeing'}",
                "afternoon": f"Experience {profile['interests'][1] if len(profile['interests']) > 1 else 'cultural sites'} and local cuisine",
                "evening": "Relax and enjoy local nightlife or cultural events",
                "food_recommendations": ["Local restaurant", "Street food market", "Rooftop dining"],
                "transportation": "Use local public transport or walking for nearby attractions",
                "budget_tips": f"Look for {profile.get('budget_range', 'medium')}-range options and local deals"
            })
        
        return {"days": days_data}

# Initialize services
weather_service = WeatherService()
hotel_service = HotelService()
ai_service = AIService()

# Simple in-memory storage for demo
user_profiles = {}

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
        user_id = f"user_{len(user_profiles) + 1}"
        profile = {
            'user_id': user_id,
            'name': data['name'],
            'travel_type': data['travel_type'],
            'companions': data.get('companions', 1),
            'health_conditions': data.get('health_conditions', []),
            'destination': data['destination'],
            'days': int(data['days']),
            'interests': data['interests'],
            'budget_range': data.get('budget_range', 'medium')
        }
        
        # Store user profile
        user_profiles[user_id] = profile
        
        return jsonify({
            'message': 'User profile created successfully',
            'user_id': user_id,
            'profile': profile
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
        profile = user_profiles.get(user_id)
        if not profile:
            return jsonify({'error': 'User profile not found'}), 404
        
        # Get weather data
        weather_data = weather_service.get_weather(profile['destination'])
        
        # Get hotel recommendations
        hotels = hotel_service.get_hotels(
            profile['destination'], 
            profile['budget_range'], 
            profile['companions']
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
    return jsonify({'status': 'healthy', 'message': 'Itinerary App API is running on Vercel'})

# Export the app for Vercel
app = app
