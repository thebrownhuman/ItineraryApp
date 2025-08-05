import requests
import random
from typing import Dict, List, Any

class HotelService:
    """Service for handling hotel recommendations"""
    
    def __init__(self):
        # Since we don't have access to a real hotel API in this demo,
        # we'll create a mock service with realistic data
        self.mock_hotels = self._initialize_mock_hotels()
    
    def get_hotels(self, destination: str, budget: str, companions: int) -> List[Dict[str, Any]]:
        """
        Get hotel recommendations based on destination, budget, and number of companions
        """
        try:
            # Filter hotels by budget and capacity
            filtered_hotels = self._filter_hotels_by_criteria(destination, budget, companions)
            
            # Sort by rating and price
            sorted_hotels = sorted(filtered_hotels, key=lambda x: (-x['rating'], x['price_per_night']))
            
            # Return top 5 recommendations
            return sorted_hotels[:5]
            
        except Exception as e:
            raise Exception(f"Failed to fetch hotel data: {str(e)}")
    
    def _filter_hotels_by_criteria(self, destination: str, budget: str, companions: int) -> List[Dict[str, Any]]:
        """Filter hotels based on criteria"""
        budget_ranges = {
            'low': (2000, 4000),      # ₹2,000 - ₹4,000 per night
            'medium': (4000, 8000),   # ₹4,000 - ₹8,000 per night
            'high': (8000, 20000)     # ₹8,000 - ₹20,000 per night
        }
        
        min_price, max_price = budget_ranges.get(budget, (100, 200))
        
        # Required room capacity based on companions
        required_capacity = companions
        
        filtered = []
        for hotel in self.mock_hotels:
            # Check if hotel serves the destination (simplified)
            if destination.lower() in hotel['location'].lower() or hotel['city'].lower() in destination.lower():
                # Check budget range
                if min_price <= hotel['price_per_night'] <= max_price:
                    # Check capacity
                    if hotel['max_occupancy'] >= required_capacity:
                        filtered.append(hotel)
        
        # If no hotels found for specific destination, provide general recommendations
        if not filtered:
            for hotel in self.mock_hotels:
                if min_price <= hotel['price_per_night'] <= max_price:
                    if hotel['max_occupancy'] >= required_capacity:
                        # Adapt hotel to destination
                        adapted_hotel = hotel.copy()
                        adapted_hotel['location'] = f"Near {destination}"
                        adapted_hotel['city'] = destination
                        filtered.append(adapted_hotel)
        
        return filtered[:10]  # Limit to 10 options
    
    def _initialize_mock_hotels(self) -> List[Dict[str, Any]]:
        """Initialize mock hotel data"""
        return [
            {
                'id': 1,
                'name': 'Grand Palace Hotel',
                'rating': 4.8,
                'price_per_night': 12500,  # ₹12,500 per night
                'location': 'City Center',
                'city': 'Mumbai',
                'max_occupancy': 4,
                'amenities': ['WiFi', 'Pool', 'Spa', 'Restaurant', 'Gym', 'Room Service'],
                'accessibility': ['Elevator', 'Wheelchair Access', 'Accessible Bathroom'],
                'description': 'Luxury hotel in the heart of the city with excellent service',
                'image_url': 'https://via.placeholder.com/300x200',
                'distance_to_center': 0.5
            },
            {
                'id': 2,
                'name': 'Budget Inn Downtown',
                'rating': 3.9,
                'price_per_night': 3000,  # ₹3,000 per night
                'location': 'Downtown',
                'city': 'Delhi',
                'max_occupancy': 2,
                'amenities': ['WiFi', 'Continental Breakfast', 'Air Conditioning'],
                'accessibility': ['Elevator'],
                'description': 'Clean and comfortable budget-friendly accommodation',
                'image_url': 'https://via.placeholder.com/300x200',
                'distance_to_center': 1.2
            },
            {
                'id': 3,
                'name': 'Boutique Heritage Hotel',
                'rating': 4.5,
                'price_per_night': 7200,  # ₹7,200 per night
                'location': 'Historic District',
                'city': 'Jaipur',
                'max_occupancy': 3,
                'amenities': ['WiFi', 'Restaurant', 'Bar', 'Concierge', 'Library'],
                'accessibility': ['Elevator', 'Wheelchair Access'],
                'description': 'Charming boutique hotel with historical character',
                'image_url': 'https://via.placeholder.com/300x200',
                'distance_to_center': 0.8
            },
            {
                'id': 4,
                'name': 'Modern Business Hotel',
                'rating': 4.2,
                'price_per_night': 5600,  # ₹5,600 per night
                'location': 'Business District',
                'city': 'Bangalore',
                'max_occupancy': 2,
                'amenities': ['WiFi', 'Business Center', 'Gym', 'Restaurant', 'Laundry'],
                'accessibility': ['Elevator', 'Wheelchair Access', 'Accessible Bathroom'],
                'description': 'Contemporary hotel perfect for business travelers',
                'image_url': 'https://via.placeholder.com/300x200',
                'distance_to_center': 2.1
            },
            {
                'id': 5,
                'name': 'Seaside Resort',
                'rating': 4.7,
                'price_per_night': 16000,  # ₹16,000 per night
                'location': 'Beachfront',
                'city': 'Goa',
                'max_occupancy': 6,
                'amenities': ['WiFi', 'Pool', 'Beach Access', 'Spa', 'Restaurant', 'Bar', 'Water Sports'],
                'accessibility': ['Elevator', 'Wheelchair Access', 'Beach Wheelchair'],
                'description': 'Luxury beachfront resort with stunning ocean views',
                'image_url': 'https://via.placeholder.com/300x200',
                'distance_to_center': 5.2
            },
            {
                'id': 6,
                'name': 'Cozy Bed & Breakfast',
                'rating': 4.3,
                'price_per_night': 3800,  # ₹3,800 per night
                'location': 'Residential Area',
                'city': 'Kochi',
                'max_occupancy': 2,
                'amenities': ['WiFi', 'Breakfast Included', 'Garden', 'Parking'],
                'accessibility': ['Ground Floor Rooms'],
                'description': 'Intimate B&B with personalized service and homemade breakfast',
                'image_url': 'https://via.placeholder.com/300x200',
                'distance_to_center': 3.5
            },
            {
                'id': 7,
                'name': 'Mountain Lodge',
                'rating': 4.4,
                'price_per_night': 6400,  # ₹6,400 per night
                'location': 'Mountain View',
                'city': 'Manali',
                'max_occupancy': 4,
                'amenities': ['WiFi', 'Fireplace', 'Restaurant', 'Hiking Trails', 'Spa'],
                'accessibility': ['Elevator', 'Wheelchair Access'],
                'description': 'Rustic lodge with breathtaking mountain views',
                'image_url': 'https://via.placeholder.com/300x200',
                'distance_to_center': 15.0
            },
            {
                'id': 8,
                'name': 'Airport Transit Hotel',
                'rating': 3.8,
                'price_per_night': 3400,  # ₹3,400 per night
                'location': 'Near Airport',
                'city': 'Chennai',
                'max_occupancy': 3,
                'amenities': ['WiFi', 'Shuttle Service', 'Restaurant', '24/7 Front Desk'],
                'accessibility': ['Elevator', 'Wheelchair Access'],
                'description': 'Convenient hotel for travelers with early flights',
                'image_url': 'https://via.placeholder.com/300x200',
                'distance_to_center': 20.0
            }
        ]
    
    def get_hotel_recommendations_by_health_conditions(self, hotels: List[Dict], health_conditions: List[str]) -> List[Dict[str, Any]]:
        """Filter hotels based on health condition requirements"""
        if not health_conditions:
            return hotels
        
        accessibility_needed = []
        for condition in health_conditions:
            condition_lower = condition.lower()
            if 'leg' in condition_lower or 'mobility' in condition_lower:
                accessibility_needed.extend(['Wheelchair Access', 'Elevator', 'Accessible Bathroom'])
            elif 'heart' in condition_lower:
                accessibility_needed.append('Elevator')
        
        if not accessibility_needed:
            return hotels
        
        # Filter hotels that have required accessibility features
        filtered_hotels = []
        for hotel in hotels:
            hotel_accessibility = hotel.get('accessibility', [])
            if any(feature in hotel_accessibility for feature in accessibility_needed):
                # Add accessibility score
                hotel_copy = hotel.copy()
                hotel_copy['accessibility_score'] = len(set(accessibility_needed) & set(hotel_accessibility))
                filtered_hotels.append(hotel_copy)
        
        # Sort by accessibility score
        return sorted(filtered_hotels, key=lambda x: x.get('accessibility_score', 0), reverse=True)
