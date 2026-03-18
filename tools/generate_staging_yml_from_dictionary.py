#!/usr/bin/env python3
"""
Generate dbt staging model YAML documentation from EDW data dictionary.

Usage:
    python generate_staging_yml_from_dictionary.py FCT_POSTED_TRANSACTION

This script reads r1_edw_dictionary.csv and generates YAML column documentation
that can be copied into your staging model's schema.yml file.

Example output:
    - name: posted_txn_uid
      description: "Unique Transaction Identifier assigned to the transaction in ODS"
      data_type: bigint
      meta:
        is_primary_key: true
"""

import csv
import sys
from pathlib import Path


def snake_case(name):
    """Convert column name to snake_case."""
    return name.lower()


def generate_yml_for_entity(edw_entity_name, dictionary_path):
    """Generate YAML documentation for a given EDW entity."""
    
    # Read the data dictionary
    with open(dictionary_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if row['EDW Entity'] == edw_entity_name]
    
    if not rows:
        print(f"❌ No fields found for entity: {edw_entity_name}")
        return
    
    print(f"# Generated from r1_edw_dictionary.csv for {edw_entity_name}")
    print(f"# Total fields: {len(rows)}\n")
    print("columns:")
    
    for row in rows:
        edw_attr = row['EDW Attribute']
        definition = row['Definition'].strip()
        data_type = row['Data Type'].lower()
        is_pk = row['PK'] == 'YES'
        is_fk = row['FK'] == 'YES'
        
        # Skip NULL attributes (calculated fields)
        if edw_attr == 'NULL':
            continue
        
        # Convert to snake_case for dbt
        column_name = snake_case(edw_attr)
        
        # Start column definition
        print(f"  - name: {column_name}")
        
        # Add description
        if definition:
            # Handle multi-line definitions
            if '\n' in definition:
                print(f'    description: |')
                for line in definition.split('\n'):
                    print(f'      {line}')
            else:
                # Escape quotes
                definition_escaped = definition.replace('"', '\\"')
                print(f'    description: "{definition_escaped}"')
        else:
            print(f'    description: ""')
        
        # Add metadata
        meta_items = []
        if is_pk:
            meta_items.append('is_primary_key: true')
        if is_fk:
            meta_items.append('is_foreign_key: true')
        if data_type:
            meta_items.append(f'edw_data_type: {data_type}')
        
        if meta_items:
            print('    meta:')
            for item in meta_items:
                print(f'      {item}')
        
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_staging_yml_from_dictionary.py <EDW_ENTITY_NAME>")
        print("\nExamples:")
        print("  FCT_POSTED_TRANSACTION")
        print("  FCT_AUTHORIZATION_TRANSACTION")
        print("  DIM_ACCOUNT")
        sys.exit(1)
    
    edw_entity = sys.argv[1].upper()
    
    # Find the dictionary file (assuming it's in seeds/)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    dictionary_path = repo_root / 'seeds' / 'r1_edw_dictionary.csv'
    
    if not dictionary_path.exists():
        print(f"❌ Dictionary not found at: {dictionary_path}")
        sys.exit(1)
    
    generate_yml_for_entity(edw_entity, dictionary_path)


if __name__ == '__main__':
    main()
