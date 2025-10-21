#!/usr/bin/env python3
"""
File Storage API Test Script

This script demonstrates how to use the file storage API endpoints.
Run this script to test the file upload and retrieval functionality.

Usage:
    python test_api.py

Make sure to:
1. Set your JWT token in the TOKEN variable
2. Update the BASE_URL if your server is running on a different port
3. Have a test file ready for upload
"""

import requests
import json
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "your_jwt_token_here"  # Replace with your actual JWT token
TEST_FILE_PATH = "test_image.jpg"  # Replace with path to a test file

# Headers for authenticated requests
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def test_file_upload():
    """Test file upload endpoint."""
    print("Testing file upload...")
    
    # Check if test file exists
    if not os.path.exists(TEST_FILE_PATH):
        print(f"Test file {TEST_FILE_PATH} not found. Please create a test file first.")
        return None
    
    # Prepare file upload
    url = f"{BASE_URL}/api/files/upload/"
    files = {
        'file': open(TEST_FILE_PATH, 'rb')
    }
    data = {
        'description': 'Test file upload',
        'is_public': True
    }
    
    # Remove Content-Type from headers for file upload
    upload_headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.post(url, files=files, data=data, headers=upload_headers)
        files['file'].close()
        
        if response.status_code == 201:
            result = response.json()
            print("✅ File upload successful!")
            print(f"File Reference: {result['file_reference']}")
            print(f"File URL: {result['file_url']}")
            return result['file_reference']
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def test_get_file_info(file_reference):
    """Test file information retrieval."""
    print(f"\nTesting file info retrieval for {file_reference}...")
    
    url = f"{BASE_URL}/api/files/{file_reference}/"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ File info retrieval successful!")
            print(f"File Name: {result['file_data']['file_name']}")
            print(f"Storage Location: {result['file_data']['storage_location']}")
            print(f"MIME Type: {result['file_data']['mime_type']}")
            print(f"File Size: {result['file_data']['file_size']} bytes")
            return True
        else:
            print(f"❌ File info retrieval failed: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def test_serve_file(file_reference):
    """Test file serving endpoint."""
    print(f"\nTesting file serving for {file_reference}...")
    
    url = f"{BASE_URL}/api/files/{file_reference}/serve/"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code in [200, 302]:  # 302 for redirects to Cloudinary
            print("✅ File serving successful!")
            if response.status_code == 302:
                print(f"Redirected to: {response.headers.get('Location', 'Unknown')}")
            else:
                print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            return True
        else:
            print(f"❌ File serving failed: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def test_list_user_files():
    """Test listing user files."""
    print("\nTesting user files listing...")
    
    url = f"{BASE_URL}/api/files/files/"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ User files listing successful!")
            print(f"Total files: {result['count']}")
            for file_data in result['files'][:3]:  # Show first 3 files
                print(f"  - {file_data['file_name']} ({file_data['storage_location']})")
            return True
        else:
            print(f"❌ User files listing failed: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def test_file_stats():
    """Test file statistics endpoint."""
    print("\nTesting file statistics...")
    
    url = f"{BASE_URL}/api/files/stats/"
    
    try:
        response = requests.get(url)  # No auth required for stats
        
        if response.status_code == 200:
            result = response.json()
            print("✅ File statistics retrieval successful!")
            stats = result['stats']
            print(f"Total files: {stats['total_files']}")
            print(f"Local storage: {stats['by_storage']['local']}")
            print(f"Cloudinary storage: {stats['by_storage']['cloudinary']}")
            print(f"Images: {stats['by_type']['images']}")
            print(f"Videos: {stats['by_type']['videos']}")
            print(f"Documents: {stats['by_type']['documents']}")
            return True
        else:
            print(f"❌ File statistics failed: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def test_delete_file(file_reference):
    """Test file deletion."""
    print(f"\nTesting file deletion for {file_reference}...")
    
    url = f"{BASE_URL}/api/files/{file_reference}/delete/"
    
    try:
        response = requests.delete(url, headers=HEADERS)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ File deletion successful!")
            print(result['message'])
            return True
        else:
            print(f"❌ File deletion failed: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def main():
    """Run all API tests."""
    print("🚀 Starting File Storage API Tests")
    print("=" * 50)
    
    # Check configuration
    if TOKEN == "your_jwt_token_here":
        print("❌ Please set your JWT token in the TOKEN variable")
        return
    
    if not os.path.exists(TEST_FILE_PATH):
        print(f"❌ Please create a test file at {TEST_FILE_PATH}")
        return
    
    # Test file statistics (no auth required)
    test_file_stats()
    
    # Test file upload
    file_reference = test_file_upload()
    if not file_reference:
        print("❌ Cannot continue without successful file upload")
        return
    
    # Test file info retrieval
    test_get_file_info(file_reference)
    
    # Test file serving
    test_serve_file(file_reference)
    
    # Test user files listing
    test_list_user_files()
    
    # Ask user if they want to delete the test file
    print(f"\n🗑️  Test file uploaded with reference: {file_reference}")
    delete_choice = input("Do you want to delete the test file? (y/N): ").lower().strip()
    
    if delete_choice in ['y', 'yes']:
        test_delete_file(file_reference)
    else:
        print(f"Test file kept with reference: {file_reference}")
    
    print("\n✅ API tests completed!")


if __name__ == "__main__":
    main()
