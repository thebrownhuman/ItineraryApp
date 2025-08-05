#!/usr/bin/env python3
"""
Quick test script to verify Gemini API key is working
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test if Gemini API key is working"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'your_gemini_api_key_here_optional':
        print("❌ No Gemini API key found")
        return False
    
    print(f"🔑 Testing Gemini API key: {api_key[:10]}...")
    
    # Test API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello! Can you generate a simple travel tip for Delhi?"
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                content = data['candidates'][0]['content']['parts'][0]['text']
                print("✅ Gemini API is working!")
                print(f"📝 Sample response: {content[:100]}...")
                return True
            else:
                print("❌ API responded but no content generated")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini API Integration...")
    test_gemini_api()
