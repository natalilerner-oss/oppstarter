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
    if python3 -c "import yaml; f=open('$workflow'); yaml.safe_load(f); f.close()" 2>/dev/null; then
        echo "✅ $workflow is valid"
    else
        echo "❌ Invalid YAML in $workflow"
        exit 1
    fi
    
    echo ""
done

echo "✅ All workflow files are valid!"
