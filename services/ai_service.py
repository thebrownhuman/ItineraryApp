import os
import json
import requests
from typing import Dict, List, Any, Optional
from models.user_profile import UserProfile

class AIService:
    """Service for AI-powered itinerary generation"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
        
    def generate_itinerary(self, profile: UserProfile, weather_data: Dict, hotels: List[Dict]) -> Dict[str, Any]:
        """
        Generate a personalized itinerary using AI
        """
        try:
            # Prepare context for AI
            context = self._prepare_context(profile, weather_data, hotels)
            
            # Check which AI service to use
            print(f"🤖 AI Service - Gemini API Key: {'✅ Available' if self.gemini_api_key and self.gemini_api_key != 'your_gemini_api_key_here_optional' else '❌ Not configured'}")
            print(f"🤖 AI Service - Perplexity API Key: {'✅ Available' if self.perplexity_api_key and self.perplexity_api_key != 'your_perplexity_api_key_here_optional' else '❌ Not configured'}")
            
            # Try Gemini first, fallback to Perplexity
            if self.gemini_api_key and self.gemini_api_key != 'your_gemini_api_key_here_optional':
                print("🚀 Using Gemini AI for itinerary generation...")
                itinerary = self._generate_with_gemini(context)
                itinerary['generated_by'] = 'Gemini AI'
                return itinerary
            elif self.perplexity_api_key and self.perplexity_api_key != 'your_perplexity_api_key_here_optional':
                print("🚀 Using Perplexity AI for itinerary generation...")
                itinerary = self._generate_with_perplexity(context)
                itinerary['generated_by'] = 'Perplexity AI'
                return itinerary
            else:
                print("⚠️ No AI service configured, using fallback generation...")
                # Fallback to rule-based generation
                itinerary = self._generate_fallback_itinerary(profile, weather_data, hotels)
                return itinerary
            
        except Exception as e:
            print(f"❌ AI generation failed: {str(e)}")
            print("🔄 Falling back to rule-based generation...")
            # Always provide fallback itinerary
            return self._generate_fallback_itinerary(profile, weather_data, hotels)
    
    def _prepare_context(self, profile: UserProfile, weather_data: Dict, hotels: List[Dict]) -> str:
        """Prepare context for AI generation"""
        context = f"""
You are a professional travel planner. Create a detailed {profile.days}-day itinerary for {profile.name} traveling to {profile.destination}.

TRAVELER PROFILE:
- Name: {profile.name}
- Travel Type: {profile.travel_type} ({profile.companions} people total)
- Interests: {', '.join(profile.interests)}
- Budget Range: {profile.budget_range}
- Health Considerations: {', '.join(profile.health_conditions) if profile.health_conditions else 'None'}
- Accessibility Needs: {', '.join(profile.get_accessibility_needs()) if profile.get_accessibility_needs() else 'None'}

WEATHER INFORMATION:
Current: {weather_data['current']['temperature']}°C, {weather_data['current']['description']}
7-Day Forecast Available: Plan activities based on weather conditions

AVAILABLE HOTELS ({len(hotels)} options):
{self._format_hotels_for_context(hotels[:3])}

REQUIREMENTS:
1. Create a day-by-day itinerary that considers weather conditions
2. Match activities to traveler's interests and budget range
3. Account for health conditions and accessibility needs
4. Include specific time slots for activities
5. Recommend meals and dining options
6. Provide practical tips and travel advice
7. Include estimated costs in Indian Rupees (INR)

RESPONSE FORMAT:
Please respond with a detailed itinerary that includes:
- Day-by-day activities with specific times
- Weather-appropriate suggestions
- Meal recommendations
- Practical tips
- Budget estimates in INR

Make it personalized, engaging, and practical for the traveler.
        """
        
        return context
    
    def _format_hotels_for_context(self, hotels: List[Dict]) -> str:
        """Format hotel information for AI context"""
        hotel_info = []
        for hotel in hotels:
            info = f"- {hotel['name']}: ${hotel['price_per_night']}/night, Rating: {hotel['rating']}, {hotel['location']}"
            hotel_info.append(info)
        return '\n'.join(hotel_info)
    
    def _generate_with_gemini(self, context: str) -> Dict[str, Any]:
        """Generate itinerary using Gemini AI via REST API"""
        try:
            # Use the correct model name for Gemini
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": context
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Gemini AI Response received: {ai_response[:100]}...")
                return self._parse_ai_response(ai_response)
            else:
                raise Exception("No content generated by Gemini")
            
        except Exception as e:
            print(f"❌ Gemini AI generation failed: {str(e)}")
            raise Exception(f"Gemini AI generation failed: {str(e)}")
    
    def _generate_with_perplexity(self, context: str) -> Dict[str, Any]:
        """Generate itinerary using Perplexity AI"""
        try:
            url = "https://api.perplexity.ai/chat/completions"
            
            payload = {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional travel planner. Create detailed, personalized itineraries in JSON format."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            headers = {
                "Authorization": f"Bearer {self.perplexity_api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            return self._parse_ai_response(ai_response)
            
        except Exception as e:
            raise Exception(f"Perplexity AI generation failed: {str(e)}")
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response and extract structured itinerary"""
        try:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: parse text response
                return self._parse_text_response(response_text)
                
        except json.JSONDecodeError:
            return self._parse_text_response(response_text)
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse text response into structured format"""
        lines = text.split('\n')
        days = []
        current_day = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('Day ') or line.startswith('**Day '):
                if current_day:
                    days.append(current_day)
                current_day = {
                    'day': len(days) + 1,
                    'title': line,
                    'activities': [],
                    'meals': [],
                    'notes': []
                }
            elif current_day and line:
                if any(time in line.lower() for time in ['morning', 'afternoon', 'evening', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']):
                    current_day['activities'].append(line)
                elif any(meal in line.lower() for meal in ['breakfast', 'lunch', 'dinner', 'meal', 'restaurant']):
                    current_day['meals'].append(line)
                else:
                    current_day['notes'].append(line)
        
        if current_day:
            days.append(current_day)
        
        return {
            'days': days,
            'total_days': len(days),
            'generated_by': 'AI Assistant',
            'recommendations': {
                'packing': ['Check weather forecast', 'Comfortable walking shoes', 'Portable charger'],
                'tips': ['Book attractions in advance', 'Keep emergency contacts handy', 'Stay hydrated']
            }
        }
    
    def _generate_fallback_itinerary(self, profile: UserProfile, weather_data: Dict, hotels: List[Dict]) -> Dict[str, Any]:
        """Generate a basic rule-based itinerary as fallback"""
        days = []
        
        # Base activities by interest
        activity_mapping = {
            'museums': ['Visit local museums', 'Art galleries tour', 'Historical sites'],
            'parks': ['City parks walk', 'Botanical gardens', 'Nature trails'],
            'restaurants': ['Local cuisine tour', 'Food market visit', 'Fine dining experience'],
            'shopping': ['Shopping district tour', 'Local markets', 'Souvenir shopping'],
            'nightlife': ['Evening entertainment', 'Local bars/clubs', 'Night tours'],
            'beaches': ['Beach relaxation', 'Water activities', 'Seaside walks'],
            'adventure': ['Adventure sports', 'Hiking trails', 'Outdoor activities'],
            'culture': ['Cultural sites', 'Traditional performances', 'Local festivals']
        }
        
        available_activities = []
        for interest in profile.interests:
            if interest.lower() in activity_mapping:
                available_activities.extend(activity_mapping[interest.lower()])
        
        # If no specific activities, add general ones
        if not available_activities:
            available_activities = [
                'City center exploration',
                'Local landmark visits',
                'Walking tours',
                'Local restaurant visits',
                'Market exploration'
            ]
        
        # Generate days
        for day_num in range(1, profile.days + 1):
            day_weather = weather_data['forecast'][min(day_num - 1, len(weather_data['forecast']) - 1)]
            
            # Choose activities based on weather
            if 'rain' in day_weather['description'].lower():
                day_activities = [act for act in available_activities if any(indoor in act.lower() for indoor in ['museum', 'gallery', 'market', 'restaurant', 'shopping'])]
            else:
                day_activities = available_activities
            
            # Select 3-4 activities for the day
            selected_activities = day_activities[:4] if len(day_activities) >= 4 else day_activities
            
            day = {
                'day': day_num,
                'title': f"Day {day_num} - Exploring {profile.destination}",
                'weather': day_weather,
                'activities': [
                    f"9:00 AM - {selected_activities[0] if selected_activities else 'Morning exploration'}",
                    f"12:00 PM - Lunch break",
                    f"2:00 PM - {selected_activities[1] if len(selected_activities) > 1 else 'Afternoon sightseeing'}",
                    f"5:00 PM - {selected_activities[2] if len(selected_activities) > 2 else 'Evening relaxation'}",
                    f"7:00 PM - Dinner"
                ],
                'meals': [
                    f"Breakfast at hotel or local cafe",
                    f"Lunch at recommended restaurant",
                    f"Dinner featuring local cuisine"
                ],
                'notes': [
                    f"Weather: {day_weather['description']}, {day_weather['temperature_min']}-{day_weather['temperature_max']}°C",
                    "Wear comfortable walking shoes",
                    "Carry water and snacks"
                ]
            }
            
            # Add accessibility notes if needed
            if profile.has_health_conditions():
                accessibility_needs = profile.get_accessibility_needs()
                if accessibility_needs:
                    day['notes'].append(f"Accessibility: Look for {', '.join(accessibility_needs)}")
            
            days.append(day)
        
        # Recommend best hotel
        recommended_hotel = hotels[0] if hotels else None
        
        return {
            'days': days,
            'total_days': len(days),
            'generated_by': 'Rule-based System',
            'recommended_hotel': recommended_hotel,
            'recommendations': {
                'packing': self._get_packing_recommendations(weather_data, profile),
                'tips': self._get_travel_tips(profile),
                'budget_estimate': self._estimate_budget(profile, hotels)
            }
        }
    
    def _get_packing_recommendations(self, weather_data: Dict, profile: UserProfile) -> List[str]:
        """Generate packing recommendations"""
        items = ['Comfortable walking shoes', 'Portable charger', 'Travel documents']
        
        # Weather-based items
        avg_temp = sum(day['temperature_min'] + day['temperature_max'] for day in weather_data['forecast']) / (2 * len(weather_data['forecast']))
        
        if avg_temp < 10:
            items.extend(['Warm jacket', 'Gloves and hat', 'Thermal layers'])
        elif avg_temp < 20:
            items.extend(['Light jacket', 'Sweater', 'Long pants'])
        else:
            items.extend(['Light clothing', 'Sunscreen', 'Hat'])
        
        # Rain check
        if any('rain' in day['description'].lower() for day in weather_data['forecast']):
            items.extend(['Umbrella', 'Waterproof jacket'])
        
        # Health-based items
        if profile.has_health_conditions():
            items.extend(['Medications', 'Medical documentation', 'Emergency contacts'])
        
        return items
    
    def _get_travel_tips(self, profile: UserProfile) -> List[str]:
        """Generate travel tips"""
        tips = [
            'Book popular attractions in advance',
            'Keep copies of important documents',
            'Learn basic local phrases',
            'Stay hydrated and take breaks'
        ]
        
        if profile.travel_type == 'group':
            tips.append('Establish meeting points in case of separation')
        
        if profile.has_health_conditions():
            tips.extend([
                'Locate nearest medical facilities',
                'Carry emergency medical information',
                'Plan for rest periods between activities'
            ])
        
        return tips
    
    def _estimate_budget(self, profile: UserProfile, hotels: List[Dict]) -> Dict[str, Any]:
        """Estimate budget for the trip"""
        daily_estimates = {
            'low': {'meals': 1200, 'activities': 800, 'transport': 600},      # ₹2,600/day total
            'medium': {'meals': 2000, 'activities': 1600, 'transport': 1000}, # ₹4,600/day total  
            'high': {'meals': 3200, 'activities': 2800, 'transport': 1600}    # ₹7,600/day total
        }
        
        estimates = daily_estimates.get(profile.budget_range, daily_estimates['medium'])
        
        daily_total = sum(estimates.values())
        total_activities = daily_total * profile.days
        
        hotel_cost = 0
        if hotels:
            avg_hotel_price = sum(h['price_per_night'] for h in hotels[:3]) / min(3, len(hotels))
            hotel_cost = avg_hotel_price * profile.days
        
        return {
            'daily_activities': daily_total,
            'total_activities': total_activities,
            'accommodation': hotel_cost,
            'estimated_total': total_activities + hotel_cost,
            'currency': 'INR',
            'breakdown': {
                'meals_per_day': estimates['meals'],
                'activities_per_day': estimates['activities'],
                'transport_per_day': estimates['transport']
            }
        }
