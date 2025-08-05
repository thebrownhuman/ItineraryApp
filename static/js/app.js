// Global variables
let currentStep = 1;
let userData = {};
let generatedItinerary = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateStepIndicator();
});

// Initialize event listeners
function initializeEventListeners() {
    // Travel type change handler
    document.getElementById('travelType').addEventListener('change', function() {
        const companionsGroup = document.getElementById('companionsGroup');
        const companionsInput = document.getElementById('companions');
        
        if (this.value === 'alone') {
            companionsGroup.style.display = 'none';
            companionsInput.value = 1;
        } else if (this.value === 'couple') {
            companionsGroup.style.display = 'block';
            companionsInput.value = 2;
        } else if (this.value === 'group') {
            companionsGroup.style.display = 'block';
            companionsInput.value = 3;
        }
    });

    // Health conditions other checkbox handler
    document.addEventListener('change', function(e) {
        if (e.target.name === 'health_conditions' && e.target.value === 'other') {
            const otherInput = document.getElementById('otherHealthCondition');
            otherInput.style.display = e.target.checked ? 'block' : 'none';
        }
    });

    // Form validation on input change
    document.addEventListener('input', validateCurrentStep);
    document.addEventListener('change', validateCurrentStep);
}

// Navigation functions
function nextStep(step) {
    if (validateStep(step)) {
        collectStepData(step);
        currentStep++;
        showStep(currentStep);
        updateStepIndicator();
    }
}

function prevStep(step) {
    currentStep--;
    showStep(currentStep);
    updateStepIndicator();
}

function showStep(stepNumber) {
    // Hide all steps
    document.querySelectorAll('.form-step').forEach(step => {
        step.classList.remove('active');
    });
    
    // Show current step
    document.getElementById(`step${stepNumber}`).classList.add('active');
}

function updateStepIndicator() {
    document.querySelectorAll('.step').forEach((step, index) => {
        const stepNumber = index + 1;
        step.classList.remove('active', 'completed');
        
        if (stepNumber < currentStep) {
            step.classList.add('completed');
        } else if (stepNumber === currentStep) {
            step.classList.add('active');
        }
    });
}

// Validation functions
function validateStep(step) {
    switch(step) {
        case 1:
            return validatePersonalInfo();
        case 2:
            return validateTravelDetails();
        case 3:
            return validatePreferences();
        default:
            return true;
    }
}

function validatePersonalInfo() {
    const name = document.getElementById('name').value.trim();
    const travelType = document.getElementById('travelType').value;
    
    if (!name) {
        showError('Please enter your name');
        return false;
    }
    
    if (!travelType) {
        showError('Please select your travel type');
        return false;
    }
    
    return true;
}

function validateTravelDetails() {
    const destination = document.getElementById('destination').value.trim();
    const days = document.getElementById('days').value;
    const budget = document.getElementById('budget').value;
    
    if (!destination) {
        showError('Please enter your destination');
        return false;
    }
    
    if (!days || days < 1 || days > 30) {
        showError('Please enter a valid number of days (1-30)');
        return false;
    }
    
    if (!budget) {
        showError('Please select your budget range');
        return false;
    }
    
    return true;
}

function validatePreferences() {
    const interests = document.querySelectorAll('input[name="interests"]:checked');
    
    if (interests.length === 0) {
        showError('Please select at least one interest');
        return false;
    }
    
    return true;
}

function validateCurrentStep() {
    // Real-time validation feedback could be added here
    return true;
}

// Data collection functions
function collectStepData(step) {
    switch(step) {
        case 1:
            collectPersonalInfo();
            break;
        case 2:
            collectTravelDetails();
            break;
        case 3:
            collectPreferences();
            break;
    }
}

function collectPersonalInfo() {
    userData.name = document.getElementById('name').value.trim();
    userData.travel_type = document.getElementById('travelType').value;
    userData.companions = parseInt(document.getElementById('companions').value);
    
    // Collect health conditions
    const healthConditions = [];
    document.querySelectorAll('input[name="health_conditions"]:checked').forEach(checkbox => {
        if (checkbox.value === 'other') {
            const otherValue = document.querySelector('input[name="other_health_condition"]').value.trim();
            if (otherValue) {
                healthConditions.push(otherValue);
            }
        } else {
            healthConditions.push(checkbox.value);
        }
    });
    userData.health_conditions = healthConditions;
}

function collectTravelDetails() {
    userData.destination = document.getElementById('destination').value.trim();
    userData.days = parseInt(document.getElementById('days').value);
    userData.budget_range = document.getElementById('budget').value;
}

function collectPreferences() {
    const interests = [];
    document.querySelectorAll('input[name="interests"]:checked').forEach(checkbox => {
        interests.push(checkbox.value);
    });
    userData.interests = interests;
}

// Itinerary generation
async function generateItinerary() {
    if (!validateStep(3)) {
        return;
    }
    
    collectStepData(3);
    
    currentStep = 4;
    showStep(currentStep);
    updateStepIndicator();
    
    // Show loading state
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('itineraryResult').style.display = 'none';
    
    try {
        // Create user profile
        const userResponse = await fetch('/api/user/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        if (!userResponse.ok) {
            throw new Error('Failed to create user profile');
        }
        
        const userResult = await userResponse.json();
        const userId = userResult.user_id;
        
        // Generate itinerary
        const itineraryResponse = await fetch('/api/itinerary/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_id: userId })
        });
        
        if (!itineraryResponse.ok) {
            throw new Error('Failed to generate itinerary');
        }
        
        const result = await itineraryResponse.json();
        generatedItinerary = result;
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Error generating itinerary:', error);
        showError('Failed to generate itinerary. Please try again.');
        
        // Show a fallback message
        document.getElementById('loadingState').innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #ffc107; margin-bottom: 20px;"></i>
                <h2>Oops! Something went wrong</h2>
                <p>We're having trouble generating your itinerary right now. Please check your internet connection and try again.</p>
                <button type="button" class="btn btn-primary" onclick="generateItinerary()" style="margin-top: 20px;">
                    <i class="fas fa-redo"></i> Try Again
                </button>
            </div>
        `;
    }
}

// Display functions
function displayResults(data) {
    // Hide loading state
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('itineraryResult').style.display = 'block';
    
    // Display weather
    displayWeather(data.weather);
    
    // Display hotels
    displayHotels(data.hotels);
    
    // Display itinerary
    displayItinerary(data.itinerary);
}

function displayWeather(weather) {
    const weatherContainer = document.getElementById('weatherInfo');
    
    let weatherHTML = `
        <div class="weather-info">
            <div class="weather-card">
                <h4>Current Weather</h4>
                <div class="temperature">${Math.round(weather.current.temperature)}°C</div>
                <div class="description">${weather.current.description}</div>
                <div style="margin-top: 10px; color: #6c757d; font-size: 0.9rem;">
                    Feels like ${Math.round(weather.current.feels_like)}°C<br>
                    Humidity: ${weather.current.humidity}%<br>
                    Wind: ${weather.current.wind_speed} m/s
                </div>
            </div>
    `;
    
    // Add forecast cards
    weather.forecast.slice(0, 4).forEach(day => {
        weatherHTML += `
            <div class="weather-card">
                <h4>${formatDate(day.date)}</h4>
                <div class="temperature">${Math.round(day.temperature_max)}°/${Math.round(day.temperature_min)}°</div>
                <div class="description">${day.description}</div>
                <div style="margin-top: 10px; color: #6c757d; font-size: 0.9rem;">
                    Humidity: ${day.humidity}%
                </div>
            </div>
        `;
    });
    
    weatherHTML += '</div>';
    
    // Add weather recommendations
    if (weather.travel_recommendations) {
        weatherHTML += '<div style="margin-top: 20px;"><h5>Weather Recommendations:</h5>';
        if (weather.travel_recommendations.clothing && weather.travel_recommendations.clothing.length > 0) {
            weatherHTML += `<p><strong>Clothing:</strong> ${weather.travel_recommendations.clothing.join(', ')}</p>`;
        }
        if (weather.travel_recommendations.precautions && weather.travel_recommendations.precautions.length > 0) {
            weatherHTML += `<p><strong>Precautions:</strong> ${weather.travel_recommendations.precautions.join(', ')}</p>`;
        }
        weatherHTML += '</div>';
    }
    
    weatherContainer.innerHTML = weatherHTML;
}

function displayHotels(hotels) {
    const hotelsContainer = document.getElementById('hotelsInfo');
    
    if (!hotels || hotels.length === 0) {
        hotelsContainer.innerHTML = '<p>No hotel recommendations available for this destination.</p>';
        return;
    }
    
    let hotelsHTML = '<div class="hotels-grid">';
    
    hotels.slice(0, 3).forEach(hotel => {
        const stars = '★'.repeat(Math.floor(hotel.rating));
        
        hotelsHTML += `
            <div class="hotel-card">
                <h4>${hotel.name}</h4>
                <div class="hotel-rating">${stars} ${hotel.rating}</div>
                <div class="hotel-price">₹${hotel.price_per_night.toLocaleString('en-IN')}/night</div>
                <p style="color: #6c757d; margin-bottom: 10px;">${hotel.location}</p>
                <p style="font-size: 0.9rem; margin-bottom: 15px;">${hotel.description}</p>
                <div class="hotel-amenities">
                    ${hotel.amenities.map(amenity => `<span class="amenity-tag">${amenity}</span>`).join('')}
                </div>
                ${hotel.accessibility && hotel.accessibility.length > 0 ? 
                    `<div style="margin-top: 10px;">
                        <small style="color: #28a745;"><i class="fas fa-wheelchair"></i> ${hotel.accessibility.join(', ')}</small>
                    </div>` : ''
                }
            </div>
        `;
    });
    
    hotelsHTML += '</div>';
    hotelsContainer.innerHTML = hotelsHTML;
}

function displayItinerary(itinerary) {
    const itineraryContainer = document.getElementById('itineraryDetails');
    const recommendationsContainer = document.getElementById('recommendationsInfo');
    
    if (!itinerary || !itinerary.days) {
        itineraryContainer.innerHTML = '<p>Failed to generate itinerary. Please try again.</p>';
        return;
    }
    
    // Display itinerary days
    let itineraryHTML = '<div class="itinerary-days">';
    
    itinerary.days.forEach(day => {
        itineraryHTML += `
            <div class="day-card">
                <div class="day-header">
                    <div>
                        <div class="day-number">${day.day}</div>
                    </div>
                    <div class="day-weather">
                        ${day.weather ? `${day.weather.description}, ${day.weather.temperature_min}°-${day.weather.temperature_max}°C` : ''}
                    </div>
                </div>
                
                <h4 style="margin-bottom: 15px; color: #333;">${day.title}</h4>
                
                <div class="day-activities">
                    <h5><i class="fas fa-clock"></i> Activities</h5>
                    ${day.activities.map(activity => `
                        <div class="activity-item">
                            <span class="activity-time">${extractTime(activity)}</span>
                            <span>${removeTime(activity)}</span>
                        </div>
                    `).join('')}
                </div>
                
                ${day.meals && day.meals.length > 0 ? `
                    <div class="day-activities">
                        <h5><i class="fas fa-utensils"></i> Meals</h5>
                        ${day.meals.map(meal => `
                            <div class="activity-item">
                                <span>${meal}</span>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${day.notes && day.notes.length > 0 ? `
                    <div style="margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                        <h6 style="margin-bottom: 10px; color: #667eea;"><i class="fas fa-info-circle"></i> Notes</h6>
                        ${day.notes.map(note => `<p style="margin-bottom: 5px; font-size: 0.9rem;">${note}</p>`).join('')}
                    </div>
                ` : ''}
            </div>
        `;
    });
    
    itineraryHTML += '</div>';
    itineraryContainer.innerHTML = itineraryHTML;
    
    // Display recommendations
    if (itinerary.recommendations) {
        let recommendationsHTML = '<div class="recommendations-grid">';
        
        if (itinerary.recommendations.packing) {
            recommendationsHTML += `
                <div class="recommendation-card">
                    <h5><i class="fas fa-suitcase"></i> Packing List</h5>
                    <ul class="recommendation-list">
                        ${itinerary.recommendations.packing.map(item => `<li>${item}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        if (itinerary.recommendations.tips) {
            recommendationsHTML += `
                <div class="recommendation-card">
                    <h5><i class="fas fa-lightbulb"></i> Travel Tips</h5>
                    <ul class="recommendation-list">
                        ${itinerary.recommendations.tips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        if (itinerary.recommendations.budget_estimate) {
            const budget = itinerary.recommendations.budget_estimate;
            recommendationsHTML += `
                <div class="recommendation-card">
                    <h5><i class="fas fa-calculator"></i> Budget Estimate</h5>
                    <div style="font-size: 1.1rem; margin-bottom: 10px;">
                        <strong>Total: ₹${Math.round(budget.estimated_total).toLocaleString('en-IN')}</strong>
                    </div>
                    <ul class="recommendation-list">
                        <li>Activities: ₹${Math.round(budget.total_activities).toLocaleString('en-IN')}</li>
                        <li>Accommodation: ₹${Math.round(budget.accommodation).toLocaleString('en-IN')}</li>
                        <li>Daily average: ₹${Math.round(budget.daily_activities).toLocaleString('en-IN')}</li>
                    </ul>
                </div>
            `;
        }
        
        recommendationsHTML += '</div>';
        recommendationsContainer.innerHTML = recommendationsHTML;
    }
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
}

function extractTime(activity) {
    const timeMatch = activity.match(/(\d{1,2}:\d{2}\s*(AM|PM)?)/i);
    return timeMatch ? timeMatch[0] : '';
}

function removeTime(activity) {
    return activity.replace(/^\d{1,2}:\d{2}\s*(AM|PM)?\s*-?\s*/i, '');
}

function showError(message) {
    // Create and show error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #dc3545;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        max-width: 300px;
    `;
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i> ${message}
        <button onclick="this.parentElement.remove()" style="background: none; border: none; color: white; float: right; margin-left: 10px; cursor: pointer;">×</button>
    `;
    
    document.body.appendChild(errorDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) {
            errorDiv.remove();
        }
    }, 5000);
}

// Action functions
function startOver() {
    currentStep = 1;
    userData = {};
    generatedItinerary = null;
    
    // Reset all forms
    document.querySelectorAll('form').forEach(form => form.reset());
    document.getElementById('companionsGroup').style.display = 'none';
    document.getElementById('otherHealthCondition').style.display = 'none';
    
    showStep(currentStep);
    updateStepIndicator();
}

function printItinerary() {
    // Hide unnecessary elements for printing
    const elementsToHide = document.querySelectorAll('.step-indicator, .form-actions, .btn');
    elementsToHide.forEach(el => el.style.display = 'none');
    
    // Print
    window.print();
    
    // Restore elements
    elementsToHide.forEach(el => el.style.display = '');
}
