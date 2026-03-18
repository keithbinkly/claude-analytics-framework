#!/usr/bin/env python3
"""
Migration Compliance Validator
Validates new models against project standards before handoff.

Usage: python tools/validate_migration_compliance.py --model-path path/to/model.sql
"""

import argparse
import os
import re
import sys
from pathlib import Path

class MigrationComplianceValidator:
    def __init__(self, model_path):
        self.model_path = Path(model_path)
        self.issues = []

    def validate(self):
        """Run all validation checks."""
        print(f"🔍 Validating: {self.model_path}")

        # Basic file checks
        self._check_file_exists()
        self._check_folder_structure()
        self._check_environment_limits()
        self._check_naming_conventions()

        # Content checks
        if self.model_path.exists():
            content = self.model_path.read_text()
            self._check_sql_content(content)

        # Report results
        self._report_results()

        return len(self.issues) == 0

    def _check_file_exists(self):
        """Check if file exists."""
        if not self.model_path.exists():
            self.issues.append(f"❌ File does not exist: {self.model_path}")
        else:
            print("✅ File exists")

    def _check_folder_structure(self):
        """Check if model is in correct folder structure."""
        # Get relative path from models directory
        try:
            models_dir = Path("/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise/models")
            if models_dir in self.model_path.parents:
                rel_path = self.model_path.relative_to(models_dir)
                path_parts = rel_path.parts

                # Check intermediate models
                if len(path_parts) >= 2 and path_parts[0] in ['intermediate', 'marts']:
                    if path_parts[0] == 'intermediate' and len(path_parts) >= 3:
                        if path_parts[1] == 'intermediate_NEW':
                            print(f"✅ Intermediate model in correct folder: {path_parts[1]}")
                        else:
                            self.issues.append(f"❌ Intermediate model not in intermediate_NEW/: {rel_path}")
                    elif path_parts[0] == 'marts' and len(path_parts) >= 3:
                        if path_parts[1] == 'marts_NEW':
                            print(f"✅ Mart model in correct folder: {path_parts[1]}")
                        else:
                            self.issues.append(f"❌ Mart model not in marts_NEW/: {rel_path}")
                    else:
                        self.issues.append(f"❌ Incorrect folder structure: {rel_path}")
                else:
                    self.issues.append(f"❌ Model not in models/intermediate/ or models/marts/: {rel_path}")
            else:
                self.issues.append(f"❌ Model not in models directory: {self.model_path}")
        except Exception as e:
            self.issues.append(f"❌ Error checking folder structure: {e}")

    def _check_environment_limits(self):
        """Check for environment-aware date limits."""
        if not self.model_path.exists():
            return

        content = self.model_path.read_text()

        # Look for date-related patterns that should have environment limits
        date_patterns = [
            r'\bwhere.*date\s*>=',
            r'\bwhere.*createdate\s*>=',
            r'\bwhere.*updated_at\s*>=',
            r'\bwhere.*business_dt\s*>=',
            r'\bwhere.*calendar_date\s*>='
        ]

        has_date_filter = any(re.search(pattern, content, re.IGNORECASE) for pattern in date_patterns)

        if has_date_filter:
            # Check for environment variable pattern
            env_limit_pattern = r"env_var\('DBT_CLOUD_ENVIRONMENT_TYPE'"
            if re.search(env_limit_pattern, content):
                print("✅ Environment-aware date limits found")
            else:
                self.issues.append("❌ Date filters found but no environment-aware limits (DBT_CLOUD_ENVIRONMENT_TYPE)")
        else:
            print("✅ No date filters requiring environment limits")

    def _check_naming_conventions(self):
        """Check naming conventions."""
        filename = self.model_path.name

        # Check for proper patterns
        if filename.startswith(('int_', 'mart_')) and filename.endswith('.sql'):
            print(f"✅ Proper naming convention: {filename}")
        else:
            self.issues.append(f"❌ Incorrect naming convention: {filename} (should be int_* or mart_*)")

    def _check_sql_content(self, content):
        """Check SQL content for common issues."""
        # Check for explicit type casting (user preference)
        if '::float' in content:
            self.issues.append("❌ Found ::float type casting (remove per user preference)")

        # Check for proper materialization config
        if '{{ config(' in content:
            print("✅ Materialization config found")
        else:
            self.issues.append("❌ No materialization config found")

        # Check for BI grants in mart models
        if 'mart_' in str(self.model_path):
            if 'grant select' in content.lower():
                print("✅ BI grants found in mart model")
            else:
                self.issues.append("❌ Mart model missing BI grants (svc_dbt_bi)")

    def _report_results(self):
        """Report validation results."""
        print(f"\n📊 Validation Results for {self.model_path}")
        print("=" * 50)

        if not self.issues:
            print("🎉 All checks passed!")
            print("✅ Ready for handoff")
        else:
            print(f"❌ Found {len(self.issues)} issues:")
            for issue in self.issues:
                print(f"  {issue}")

        print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description="Validate dbt model compliance")
    parser.add_argument('--model-path', required=True, help="Path to model file to validate")
    parser.add_argument('--batch', nargs='*', help="Validate multiple models")

    args = parser.parse_args()

    if args.batch:
        all_passed = True
        for model_path in args.batch:
            validator = MigrationComplianceValidator(model_path)
            passed = validator.validate()
            if not passed:
                all_passed = False
            print()  # Empty line between validations
        return 0 if all_passed else 1
    else:
        validator = MigrationComplianceValidator(args.model_path)
        passed = validator.validate()
        return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
