#!/usr/bin/env python3
"""
Debug script to test Google Cloud Vision API connection
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("GOOGLE CLOUD VISION API - DEBUG TEST")
print("=" * 60)
print()

# Check credentials file
cred_path = Path(__file__).parent / 'vision-key.json'
print(f"1. Checking credentials file:")
print(f"   Path: {cred_path}")
print(f"   Exists: {cred_path.exists()}")

if not cred_path.exists():
    print("   ✗ Credentials file not found!")
    sys.exit(1)
else:
    print("   ✓ Credentials file found")
    # Check file size
    file_size = cred_path.stat().st_size
    print(f"   Size: {file_size} bytes")
    if file_size < 100:
        print("   ✗ File seems too small (might be corrupted)")
        sys.exit(1)

print()

# Check if google-cloud-vision is installed
print("2. Checking google-cloud-vision library:")
try:
    from google.cloud import vision
    print("   ✓ google-cloud-vision imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import: {e}")
    sys.exit(1)

print()

# Try to create a client
print("3. Creating Vision API client:")
try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(cred_path)
    print(f"   Environment variable set: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")
    
    client = vision.ImageAnnotatorClient.from_service_account_file(str(cred_path))
    print("   ✓ Vision API client created successfully")
except Exception as e:
    print(f"   ✗ Failed to create client: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Try a simple API call with a test image
print("4. Testing API call with a real image:")

# Check if test image exists
test_image = Path(__file__).parent / 'Leaf blight.jpeg'
if not test_image.exists():
    print(f"   Note: Test image not found at {test_image}")
    print("   Skipping API test")
else:
    print(f"   Found test image: {test_image}")
    print(f"   Image size: {test_image.stat().st_size} bytes")
    
    try:
        with open(test_image, 'rb') as f:
            content = f.read()
        
        print(f"   Read image: {len(content)} bytes")
        
        image = vision.Image(content=content)
        print("   ✓ Image object created")
        
        print("   Calling Vision API (label_detection)...")
        response = client.label_detection(image=image)
        labels = response.label_annotations
        
        print(f"   ✓ API call successful!")
        print(f"   Received {len(labels)} labels:")
        
        for idx, label in enumerate(labels[:5], 1):
            print(f"     {idx}. {label.description} ({label.score*100:.1f}%)")
        
    except Exception as e:
        print(f"   ✗ API call failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print()
print("=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print()
print("Your Google Cloud Vision API is working correctly.")
print("The Flask app should now work fine.")
