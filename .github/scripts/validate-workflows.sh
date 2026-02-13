#!/bin/bash

# Workflow Validation Script
# This script validates GitHub Actions workflow files

set -e

echo "🔍 Validating GitHub Actions workflows..."
echo ""

# Validate each workflow file
for workflow in .github/workflows/*.yml; do
    echo "Checking $workflow..."
    
    # Validate YAML syntax using Python with proper file handling
    python3 << EOF
import yaml
try:
    with open('$workflow') as f:
        yaml.safe_load(f)
    print("✅ $workflow is valid")
except Exception as e:
    print(f"❌ Invalid YAML in $workflow: {e}")
    exit(1)
EOF
    
    if [ $? -ne 0 ]; then
        exit 1
    fi
    
    echo ""
done

echo "✅ All workflow files are valid!"
