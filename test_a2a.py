#!/usr/bin/env python3
"""
Test script for A2A protocol compliance
"""

import requests
import json

def test_agent_card():
    """Test agent card endpoint"""
    print("🔍 Testing agent card endpoint...")
    try:
        response = requests.get("http://localhost:8000/.well-known/agent.json")
        if response.status_code == 200:
            agent_card = response.json()
            print("✅ Agent card retrieved successfully")
            print(f"   Agent Name: {agent_card.get('name')}")
            print(f"   Skills: {len(agent_card.get('skills', []))}")
            return True
        else:
            print(f"❌ Agent card failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Agent card error: {str(e)}")
        return False

def test_a2a_message():
    """Test A2A message/send method"""
    print("\n📨 Testing A2A message/send...")
    
    # Test QR generation
    qr_request = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": 1,
        "params": {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": "qr https://example.com"
                    }
                ]
            }
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/",
            json=qr_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                print("✅ QR generation test passed")
                print(f"   Response parts: {len(result['result'].get('parts', []))}")
                return True
            else:
                print(f"❌ QR generation failed: {result}")
                return False
        else:
            print(f"❌ QR generation HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ QR generation error: {str(e)}")
        return False

def test_barcode_message():
    """Test barcode generation"""
    print("\n📊 Testing barcode generation...")
    
    barcode_request = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": 2,
        "params": {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": "barcode 1234567890"
                    }
                ]
            }
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/",
            json=barcode_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                print("✅ Barcode generation test passed")
                return True
            else:
                print(f"❌ Barcode generation failed: {result}")
                return False
        else:
            print(f"❌ Barcode generation HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Barcode generation error: {str(e)}")
        return False

def test_help_message():
    """Test help message"""
    print("\n❓ Testing help message...")
    
    help_request = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "id": 3,
        "params": {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": "help"
                    }
                ]
            }
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/",
            json=help_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                print("✅ Help message test passed")
                return True
            else:
                print(f"❌ Help message failed: {result}")
                return False
        else:
            print(f"❌ Help message HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Help message error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing QR & Barcode Generator Agent A2A Compliance")
    print("=" * 60)
    
    tests = [
        test_agent_card,
        test_a2a_message,
        test_barcode_message,
        test_help_message
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Agent is A2A compliant.")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()