#!/usr/bin/env python3
"""
Test script for QR & Barcode Generator Agent endpoints
"""

import requests
import json
import time

BASE_URL = 'http://localhost:8000'

def test_endpoint(method, path, data=None):
    """Test an endpoint and return the response"""
    url = f"{BASE_URL}{path}"
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        
        return {
            'status': response.status_code,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def run_tests():
    """Run comprehensive endpoint tests"""
    print('Testing QR & Barcode Generator Agent endpoints...\n')
    
    # Check if server is running
    print('Checking if server is running...')
    health_check = test_endpoint('GET', '/health')
    if 'error' in health_check:
        print('Server is not running. Please start it with: python run.py')
        return False
    
    print('Server is running, starting tests...\n')
    
    tests = [
        {
            'name': 'Home page with integration details (GET /)',
            'method': 'GET',
            'path': '/',
            'expected_keys': ['name', 'description', 'version', 'endpoints', 'commands', 'integration']
        },
        {
            'name': 'Health check (GET /health)',
            'method': 'GET', 
            'path': '/health',
            'expected_keys': ['status', 'timestamp', 'version']
        },
        {
            'name': 'Agent configuration (GET /.well-known/agent.json)',
            'method': 'GET',
            'path': '/.well-known/agent.json',
            'expected_keys': ['name', 'description', 'skills']
        },
        {
            'name': 'QR code generation (POST /)',
            'method': 'POST',
            'path': '/',
            'data': {'text': 'qr Hello World'},
            'expected_keys': ['text', 'type', 'image']
        },
        {
            'name': 'QR with custom size (POST /)',
            'method': 'POST',
            'path': '/',
            'data': {'text': 'qr size:20 Custom Size QR'},
            'expected_keys': ['text', 'type', 'image']
        },
        {
            'name': 'Barcode generation (POST /)',
            'method': 'POST',
            'path': '/',
            'data': {'text': 'barcode 1234567890'},
            'expected_keys': ['text', 'type', 'image']
        },
        {
            'name': 'Barcode with format (POST /)',
            'method': 'POST',
            'path': '/',
            'data': {'text': 'barcode format:ean13 123456789012'},
            'expected_keys': ['text', 'type', 'image']
        },
        {
            'name': 'Help command (POST /)',
            'method': 'POST',
            'path': '/',
            'data': {'text': 'help'},
            'expected_keys': ['text', 'type']
        },
        {
            'name': 'Direct QR API (POST /api/v1/qr)',
            'method': 'POST',
            'path': '/api/v1/qr',
            'data': {'text': 'Direct API Test', 'size': 15},
            'expected_keys': ['success', 'text', 'size', 'image']
        },
        {
            'name': 'Direct Barcode API (POST /api/v1/barcode)',
            'method': 'POST',
            'path': '/api/v1/barcode',
            'data': {'text': '1234567890', 'format': 'code128'},
            'expected_keys': ['success', 'text', 'format', 'image']
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(tests, 1):
        print(f"{i}. Testing {test['name']}")
        
        response = test_endpoint(test['method'], test['path'], test.get('data'))
        
        if 'error' in response:
            print(f"   ERROR: {response['error']}")
            failed += 1
            continue
            
        print(f"   Status: {response['status']}")
        
        if response['status'] != 200:
            print(f"   FAILED: Expected status 200, got {response['status']}")
            failed += 1
            continue
            
        # Check expected keys
        if 'expected_keys' in test:
            missing_keys = []
            for key in test['expected_keys']:
                if key not in response['data']:
                    missing_keys.append(key)
            
            if missing_keys:
                print(f"   FAILED: Missing keys: {missing_keys}")
                failed += 1
                continue
        
        # Special checks for home page
        if test['name'].startswith('Home page'):
            integration = response['data'].get('integration', {})
            if integration.get('platform') == 'Telex.im' and integration.get('protocol') == 'A2A':
                print(f"   PASSED: Integration details present")
                print(f"   Platform: {integration.get('platform')}")
                print(f"   Protocol: {integration.get('protocol')}")
                print(f"   Repository: {integration.get('repository')}")
            else:
                print(f"   FAILED: Missing or invalid integration details")
                failed += 1
                continue
        
        # Special checks for image generation
        if 'image' in test.get('expected_keys', []):
            if response['data'].get('type') == 'image' and response['data'].get('image', '').startswith('data:image/png;base64,'):
                print(f"   PASSED: Image generated successfully")
            else:
                print(f"   FAILED: Invalid image response")
                failed += 1
                continue
        
        print(f"   PASSED")
        passed += 1
        print()
    
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("SUCCESS: All tests passed! Your agent is ready for deployment.")
        return True
    else:
        print("FAILED: Some tests failed. Please fix the issues.")
        return False

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)