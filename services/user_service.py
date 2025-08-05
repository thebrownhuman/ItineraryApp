import uuid
from typing import Dict, Optional
from models.user_profile import UserProfile

class UserService:
    """Service for managing user profiles"""
    
    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would be a database
        self.profiles = {}
    
    def create_profile(self, profile: UserProfile) -> str:
        """
        Create a new user profile and return user ID
        """
        user_id = str(uuid.uuid4())
        self.profiles[user_id] = profile
        return user_id
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile by ID
        """
        return self.profiles.get(user_id)
    
    def update_profile(self, user_id: str, profile: UserProfile) -> bool:
        """
        Update existing user profile
        """
        if user_id in self.profiles:
            self.profiles[user_id] = profile
            return True
        return False
    
    def delete_profile(self, user_id: str) -> bool:
        """
        Delete user profile
        """
        if user_id in self.profiles:
            del self.profiles[user_id]
            return True
        return False
    
    def list_profiles(self) -> Dict[str, Dict]:
        """
        List all user profiles (for admin purposes)
        """
        return {
            user_id: profile.to_dict() 
            for user_id, profile in self.profiles.items()
        }
    
    def validate_profile_data(self, data: Dict) -> Dict[str, str]:
        """
        Validate user profile data and return errors if any
        """
        errors = {}
        
        # Required fields validation
        required_fields = ['name', 'travel_type', 'destination', 'days', 'interests']
        for field in required_fields:
            if not data.get(field):
                errors[field] = f"{field} is required"
        
        # Specific validations
        if data.get('days'):
            try:
                days = int(data['days'])
                if days < 1 or days > 30:
                    errors['days'] = "Days must be between 1 and 30"
            except (ValueError, TypeError):
                errors['days'] = "Days must be a valid number"
        
        if data.get('companions'):
            try:
                companions = int(data['companions'])
                if companions < 1 or companions > 20:
                    errors['companions'] = "Companions must be between 1 and 20"
            except (ValueError, TypeError):
                errors['companions'] = "Companions must be a valid number"
        
        if data.get('travel_type') and data['travel_type'] not in ['alone', 'couple', 'group']:
            errors['travel_type'] = "Travel type must be 'alone', 'couple', or 'group'"
        
        if data.get('budget_range') and data['budget_range'] not in ['low', 'medium', 'high']:
            errors['budget_range'] = "Budget range must be 'low', 'medium', or 'high'"
        
        return errors
