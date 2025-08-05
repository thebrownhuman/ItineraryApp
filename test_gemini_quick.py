import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_quick():
    """Quick test of Gemini API"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        return False
    
    print(f"🔑 Testing Gemini API key: {api_key[:15]}...")
    
    # Try the correct model name
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Create a simple 1-day itinerary for Delhi. Include 3 activities with times. Be concise."
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data:
                content = data['candidates'][0]['content']['parts'][0]['text']
                print("✅ Gemini API is working!")
                print("📝 Sample response:")
                print("-" * 50)
                print(content)
                print("-" * 50)
                return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_quick()
