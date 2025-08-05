import requests
import os
from typing import Dict, Any
from datetime import datetime, timedelta

class WeatherService:
    """Service for handling weather-related operations"""
    
    def __init__(self):
        # Using Open-Meteo - completely free, no API key required
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1"
    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Get current weather and 7-day forecast for a city using Open-Meteo API (completely free)
        """
        try:
            # First, get coordinates for the city
            coordinates = self._get_coordinates(city)
            lat, lon, city_name = coordinates
            
            # Get weather data from Open-Meteo
            weather_data = self._get_weather_data(lat, lon)
            
            # Get current weather
            current_weather = self._parse_current_weather(weather_data, city_name)
            
            # Get forecast
            forecast = self._parse_forecast(weather_data)
            
            return {
                'current': current_weather,
                'forecast': forecast,
                'travel_recommendations': self._get_travel_recommendations(current_weather, forecast)
            }
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}")
        except Exception as e:
            # Fallback to mock data if API fails
            return self._get_fallback_weather(city)
    
    def _get_coordinates(self, city: str) -> tuple:
        """Get coordinates for a city using Open-Meteo geocoding"""
        try:
            url = f"{self.geocoding_url}/search"
            params = {
                'name': city,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                return (
                    result['latitude'], 
                    result['longitude'], 
                    result['name']
                )
            else:
                # Return default coordinates for London if city not found
                return (51.5074, -0.1278, city)
                
        except Exception as e:
            print(f"Geocoding error: {e}")
            # Return default coordinates for London if geocoding fails
            return (51.5074, -0.1278, city)
    
    def _get_weather_data(self, lat: float, lon: float) -> Dict:
        """Get weather data from Open-Meteo"""
        url = f"{self.base_url}/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code',
            'daily': 'weather_code,temperature_2m_max,temperature_2m_min,wind_speed_10m_max',
            'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code',
            'timezone': 'auto',
            'forecast_days': 7
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        return response.json()
    
    def _parse_current_weather(self, data: Dict, city_name: str) -> Dict[str, Any]:
        """Parse current weather from Open-Meteo response"""
        current = data.get('current', {})
        
        return {
            'temperature': round(current.get('temperature_2m', 20), 1),
            'feels_like': round(current.get('temperature_2m', 20), 1),  # Open-Meteo doesn't provide feels_like
            'humidity': current.get('relative_humidity_2m', 50),
            'pressure': 1013,  # Default value as Open-Meteo free tier doesn't include pressure
            'description': self._get_weather_description(current.get('weather_code', 0)),
            'icon': self._get_weather_icon(current.get('weather_code', 0)),
            'wind_speed': round(current.get('wind_speed_10m', 5), 1),
            'visibility': 10,  # Default visibility
            'city': city_name,
            'country': ''  # Open-Meteo doesn't provide country in this endpoint
        }
    
    def _parse_forecast(self, data: Dict) -> list:
        """Parse forecast data from Open-Meteo response"""
        daily = data.get('daily', {})
        dates = daily.get('time', [])
        max_temps = daily.get('temperature_2m_max', [])
        min_temps = daily.get('temperature_2m_min', [])
        weather_codes = daily.get('weather_code', [])
        wind_speeds = daily.get('wind_speed_10m_max', [])
        
        forecast = []
        for i in range(min(len(dates), 7)):  # Get up to 7 days
            forecast.append({
                'date': dates[i],
                'temperature_max': round(max_temps[i] if i < len(max_temps) else 20, 1),
                'temperature_min': round(min_temps[i] if i < len(min_temps) else 15, 1),
                'description': self._get_weather_description(weather_codes[i] if i < len(weather_codes) else 0),
                'icon': self._get_weather_icon(weather_codes[i] if i < len(weather_codes) else 0),
                'humidity': 50,  # Default humidity
                'wind_speed': round(wind_speeds[i] if i < len(wind_speeds) else 5, 1)
            })
        
        return forecast
    
    def _get_weather_description(self, weather_code: int) -> str:
        """Convert Open-Meteo weather code to description"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(weather_code, "Unknown")
    
    def _get_weather_icon(self, weather_code: int) -> str:
        """Convert Open-Meteo weather code to icon"""
        if weather_code == 0:
            return "01d"  # Clear sky
        elif weather_code in [1, 2]:
            return "02d"  # Partly cloudy
        elif weather_code == 3:
            return "03d"  # Overcast
        elif weather_code in [45, 48]:
            return "50d"  # Fog
        elif weather_code in [51, 53, 55, 56, 57]:
            return "09d"  # Drizzle
        elif weather_code in [61, 63, 65, 66, 67, 80, 81, 82]:
            return "10d"  # Rain
        elif weather_code in [71, 73, 75, 77, 85, 86]:
            return "13d"  # Snow
        elif weather_code in [95, 96, 99]:
            return "11d"  # Thunderstorm
        else:
            return "01d"  # Default
    
    def _get_fallback_weather(self, city: str) -> Dict[str, Any]:
        """Fallback weather data when API fails"""
        return {
            'current': {
                'temperature': 22,
                'feels_like': 24,
                'humidity': 60,
                'pressure': 1013,
                'description': 'partly cloudy',
                'icon': '02d',
                'wind_speed': 5.2,
                'visibility': 10,
                'city': city,
                'country': ''
            },
            'forecast': [
                {
                    'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                    'temperature_max': 25 - i,
                    'temperature_min': 18 - i,
                    'description': 'partly cloudy',
                    'icon': '02d',
                    'humidity': 60,
                    'wind_speed': 5.0
                } for i in range(5)
            ],
            'travel_recommendations': {
                'clothing': ['Light layers', 'Comfortable walking shoes'],
                'activities': ['Perfect for outdoor sightseeing'],
                'precautions': ['Stay hydrated'],
                'best_times': ['Great weather for activities']
            }
        }
    
    def _get_travel_recommendations(self, current: Dict, forecast: list) -> Dict[str, Any]:
        """Generate travel recommendations based on weather"""
        recommendations = {
            'clothing': [],
            'activities': [],
            'precautions': [],
            'best_times': []
        }
        
        # Current weather recommendations
        temp = current['temperature']
        description = current['description'].lower()
        
        # Clothing recommendations
        if temp < 5:
            recommendations['clothing'].extend(['Heavy winter coat', 'Warm layers', 'Gloves and hat'])
        elif temp < 15:
            recommendations['clothing'].extend(['Light jacket', 'Long pants', 'Warm layers'])
        elif temp < 25:
            recommendations['clothing'].extend(['Light layers', 'Comfortable walking shoes'])
        else:
            recommendations['clothing'].extend(['Light clothing', 'Sun hat', 'Sunscreen'])
        
        # Weather-specific recommendations
        if 'rain' in description or 'drizzle' in description:
            recommendations['clothing'].append('Waterproof jacket')
            recommendations['precautions'].append('Carry umbrella')
            recommendations['activities'].append('Indoor attractions')
        
        if 'snow' in description:
            recommendations['clothing'].extend(['Waterproof boots', 'Warm socks'])
            recommendations['precautions'].append('Check road conditions')
        
        if current['wind_speed'] > 10:
            recommendations['precautions'].append('Strong winds expected')
        
        # Activity recommendations based on forecast
        clear_days = [day for day in forecast if 'clear' in day['description'].lower() or 'sun' in day['description'].lower()]
        if clear_days:
            recommendations['best_times'].append(f"Best outdoor activities on {clear_days[0]['date']}")
        
        return recommendations
