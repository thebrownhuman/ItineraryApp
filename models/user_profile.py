from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class UserProfile:
    """User profile data model"""
    name: str
    travel_type: str  # 'alone', 'couple', 'group'
    companions: int
    health_conditions: List[str]
    destination: str
    days: int
    interests: List[str]
    budget_range: str  # 'low', 'medium', 'high'
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self):
        """Convert profile to dictionary"""
        return {
            'name': self.name,
            'travel_type': self.travel_type,
            'companions': self.companions,
            'health_conditions': self.health_conditions,
            'destination': self.destination,
            'days': self.days,
            'interests': self.interests,
            'budget_range': self.budget_range,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def has_health_conditions(self):
        """Check if user has any health conditions"""
        return len(self.health_conditions) > 0
    
    def get_accessibility_needs(self):
        """Get accessibility requirements based on health conditions"""
        accessibility_needs = []
        
        for condition in self.health_conditions:
            condition_lower = condition.lower()
            if 'leg' in condition_lower or 'mobility' in condition_lower:
                accessibility_needs.append('wheelchair_accessible')
                accessibility_needs.append('elevator_access')
            elif 'heart' in condition_lower:
                accessibility_needs.append('low_intensity_activities')
                accessibility_needs.append('medical_facilities_nearby')
            elif 'lung' in condition_lower or 'respiratory' in condition_lower:
                accessibility_needs.append('air_quality_consideration')
                accessibility_needs.append('avoid_high_altitude')
        
        return list(set(accessibility_needs))  # Remove duplicates
