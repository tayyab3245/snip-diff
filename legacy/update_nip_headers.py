#!/usr/bin/env python3
"""
Targeted script to update only license headers in nip/ directory files.
Updates project description to AI workflow tool.
"""

import os
import re

def update_header_in_file(file_path):
    """Update only the license header section of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the license header section only
        # Looks for the header block that starts with copyright and ends before the first import/code
        header_pattern = r'("""[\s\S]*?Copyright[\s\S]*?""")'
        
        def replace_in_header(match):
            header_text = match.group(1)
            # Update the project description
            updated_header = header_text.replace(
                'Advanced File Difference Visualization Tool',
                'AI workflow tool for preparing code context outside agentic environments'
            )
            return updated_header
        
        # Apply the replacement only to header sections
        updated_content = re.sub(header_pattern, replace_in_header, content)
        
        # Only write if there was actually a change
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated header in: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Update headers in nip/ directory files only."""
    nip_dir = "nip"
    
    if not os.path.exists(nip_dir):
        print(f"Directory {nip_dir} not found!")
        return
    
    updated_count = 0
    
    # Walk through nip directory only
    for root, dirs, files in os.walk(nip_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if update_header_in_file(file_path):
                    updated_count += 1
    
    print(f"\nCompleted! Updated headers in {updated_count} files in nip/ directory.")

if __name__ == "__main__":
    main()
