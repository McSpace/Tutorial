#!/bin/bash

# Sabre Flight Search Agent Test Script
# This script tests the API connectivity and basic functionality

echo "=========================================="
echo "Sabre Flight Search Agent - Test Suite"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3 is available
echo -n "Checking Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    exit 1
fi

# Check if required packages are installed
echo -n "Checking required packages... "
if python3 -c "import requests, lxml" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} requests and lxml installed"
else
    echo -e "${YELLOW}!${NC} Missing packages. Installing..."
    pip install -r requirements.txt
fi

echo ""
echo "=========================================="
echo "Running API Tests"
echo "=========================================="
echo ""

# Test 1: Basic Availability Search
echo "Test 1: Basic Availability Search"
echo "Command: 115JUNNYCLAX"
echo ""
python3 tools/sabre_api.py '115JUNNYCLAX'
TEST1_RESULT=$?
echo ""

if [ $TEST1_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Test 1 PASSED${NC}"
else
    echo -e "${RED}✗ Test 1 FAILED${NC}"
fi

echo ""
echo "=========================================="
echo ""

# Test 2: Search with Airline Modifier
echo "Test 2: Airline-Specific Search"
echo "Command: 115JUNNYCLAX¥AA"
echo ""
python3 tools/sabre_api.py '115JUNNYCLAX¥AA'
TEST2_RESULT=$?
echo ""

if [ $TEST2_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Test 2 PASSED${NC}"
else
    echo -e "${RED}✗ Test 2 FAILED${NC}"
fi

echo ""
echo "=========================================="
echo ""

# Test 3: JSON Output
echo "Test 3: JSON Output Format"
echo "Command: 115JUNNYCLAX --json"
echo ""
RESPONSE=$(python3 tools/sabre_api.py '115JUNNYCLAX' --json 2>/dev/null)
TEST3_RESULT=$?

if [ $TEST3_RESULT -eq 0 ]; then
    # Check if response is valid JSON
    echo "$RESPONSE" | python3 -m json.tool > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Test 3 PASSED - Valid JSON output${NC}"

        # Extract and display key fields
        echo ""
        echo "Response Summary:"
        echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"  Success: {data.get('success')}\")
print(f\"  Command: {data.get('command')}\")
if data.get('error'):
    print(f\"  Error: {data.get('error')}\")
else:
    response_text = data.get('response_text', '')
    lines = len(response_text.split('\n')) if response_text else 0
    print(f\"  Response Lines: {lines}\")
"
    else
        echo -e "${RED}✗ Test 3 FAILED - Invalid JSON${NC}"
    fi
else
    echo -e "${RED}✗ Test 3 FAILED${NC}"
fi

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo ""

PASSED=0
TOTAL=3

[ $TEST1_RESULT -eq 0 ] && ((PASSED++))
[ $TEST2_RESULT -eq 0 ] && ((PASSED++))
[ $TEST3_RESULT -eq 0 ] && ((PASSED++))

echo "Tests Passed: $PASSED/$TOTAL"
echo ""

if [ $PASSED -eq $TOTAL ]; then
    echo -e "${GREEN}All tests passed! Agent is ready to use.${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Check the output above for details.${NC}"
    echo ""
    echo "Common issues:"
    echo "  - Network connectivity to Sabre CERT environment"
    echo "  - Invalid API credentials"
    echo "  - Missing Python packages"
    echo ""
    echo "For troubleshooting, see README.md"
    exit 1
fi
