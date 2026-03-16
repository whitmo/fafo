#!/bin/bash

# Simple script to generate a smoke test shell script

APPLICATION_URL=""
EXPECTED_STATUS=200
EXPECTED_CONTENT=""
OUTPUT_FILE=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --url) APPLICATION_URL="$2"; shift ;;
        --status) EXPECTED_STATUS="$2"; shift ;;
        --content) EXPECTED_CONTENT="$2"; shift ;;
        --output) OUTPUT_FILE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$APPLICATION_URL" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: $0 --url <application_url> --output <output_file> [--status <expected_status>] [--content <expected_content>]"
    exit 1
fi

SCRIPT_DIR=$(dirname "$0")
TEMPLATE_PATH="${SCRIPT_DIR}/../assets/smoke_test_template_sh.txt"

if [ ! -f "$TEMPLATE_PATH" ]; then
    echo "Error: Template file not found at '${TEMPLATE_PATH}'."
    exit 1
fi

cp "$TEMPLATE_PATH" "$OUTPUT_FILE"

# Replace placeholders
sed -i '' "s|{{APPLICATION_URL}}|$APPLICATION_URL|g" "$OUTPUT_FILE"
sed -i '' "s/{{EXPECTED_STATUS}}/$EXPECTED_STATUS/g" "$OUTPUT_FILE"
sed -i '' "s|{{EXPECTED_CONTENT_SNIPPET}}|$EXPECTED_CONTENT|g" "$OUTPUT_FILE"

chmod +x "$OUTPUT_FILE"

echo "Success: Smoke test script generated at '${OUTPUT_FILE}' for URL '${APPLICATION_URL}'."