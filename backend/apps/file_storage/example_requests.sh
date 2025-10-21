#!/bin/bash

# File Storage API Example Requests
# Replace the variables below with your actual values

BASE_URL="http://localhost:8000"
JWT_TOKEN="your_jwt_token_here"
FILE_REFERENCE="550e8400-e29b-41d4-a716-446655440000"  # Replace with actual file reference
TEST_FILE="test_image.jpg"  # Replace with path to your test file

echo "File Storage API Example Requests"
echo "================================="

# 1. Upload a file
echo "1. Uploading a file..."
curl -X POST "${BASE_URL}/api/files/upload/" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -F "file=@${TEST_FILE}" \
  -F "description=Test file upload" \
  -F "is_public=true" \
  | jq '.'

echo -e "\n"

# 2. Get file information
echo "2. Getting file information..."
curl -X GET "${BASE_URL}/api/files/${FILE_REFERENCE}/" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  | jq '.'

echo -e "\n"

# 3. Serve file (redirects to Cloudinary for images/videos)
echo "3. Serving file..."
curl -X GET "${BASE_URL}/api/files/${FILE_REFERENCE}/serve/" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -I

echo -e "\n"

# 4. List user files
echo "4. Listing user files..."
curl -X GET "${BASE_URL}/api/files/files/" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  | jq '.'

echo -e "\n"

# 5. List user files with filters
echo "5. Listing user files (Cloudinary only)..."
curl -X GET "${BASE_URL}/api/files/files/?storage_location=cloudinary" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  | jq '.'

echo -e "\n"

# 6. List user files (images only)
echo "6. Listing user files (images only)..."
curl -X GET "${BASE_URL}/api/files/files/?mime_type=image/" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  | jq '.'

echo -e "\n"

# 7. Get file statistics
echo "7. Getting file statistics..."
curl -X GET "${BASE_URL}/api/files/stats/" \
  -H "Content-Type: application/json" \
  | jq '.'

echo -e "\n"

# 8. Delete a file (uncomment to use)
# echo "8. Deleting a file..."
# curl -X DELETE "${BASE_URL}/api/files/${FILE_REFERENCE}/delete/" \
#   -H "Authorization: Bearer ${JWT_TOKEN}" \
#   -H "Content-Type: application/json" \
#   | jq '.'

echo "Example requests completed!"
echo ""
echo "Note: Make sure to:"
echo "1. Replace JWT_TOKEN with your actual JWT token"
echo "2. Replace FILE_REFERENCE with an actual file reference from upload"
echo "3. Replace TEST_FILE with path to an actual test file"
echo "4. Install jq for JSON formatting: sudo apt-get install jq (Linux) or brew install jq (macOS)"
