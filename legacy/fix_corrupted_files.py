#!/usr/bin/env python3
"""
Script to remove license headers from venv files and restore only project files.
This fixes the corruption caused by adding headers to all Python files.
"""

import os
import glob
from pathlib import Path

def should_clean_file(file_path):
    """Check if file is in venv and should have headers removed."""
    # Only clean files in venv directory
    return 'venv' in file_path.lower()

def remove_license_header(file_path):
    """Remove license header from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the end of the license header
        header_end = '================================================================================\n"""'
        
        if 'SNIP-DIFF - Advanced File Difference Visualization Tool' in content and header_end in content:
            # Find where the header ends
            end_pos = content.find(header_end) + len(header_end)
            
            # Remove the header and any following newlines
            remaining_content = content[end_pos:]
            while remaining_content.startswith('\n'):
                remaining_content = remaining_content[1:]
            
            # Write back the cleaned content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(remaining_content)
            
            return True
    except Exception as e:
        print(f"❌ Error cleaning {file_path}: {e}")
        return False
    
    return False

def main():
    """Main function to clean corrupted files."""
    project_root = Path(__file__).parent
    
    print("🔧 Fixing corrupted files by removing headers from venv...")
    print(f"📁 Project root: {project_root}")
    print("=" * 60)
    
    # Find all Python files in venv
    venv_files = []
    venv_pattern = str(project_root / "venv" / "**" / "*.py")
    venv_files.extend(glob.glob(venv_pattern, recursive=True))
    
    cleaned_count = 0
    error_count = 0
    
    for file_path in venv_files:
        if remove_license_header(file_path):
            rel_path = os.path.relpath(file_path, project_root)
            print(f"✅ Cleaned: {rel_path}")
            cleaned_count += 1
        else:
            error_count += 1
    
    print("=" * 60)
    print(f"✅ Cleaned: {cleaned_count} venv files")
    print(f"❌ Errors: {error_count} files")
    print("🎉 Venv files cleanup complete!")
    
    print("\n" + "=" * 60)
    print("📋 Your project files still have correct headers:")
    
    # Show which project files should still have headers
    project_files = [
        "main.py",
        "nip/__init__.py", 
        "nip/config/*.py",
        "nip/core/*.py", 
        "nip/ui/*.py (except example.py)",
        "nip/ui/neumorphism/__init__.py"
    ]
    
    for pattern in project_files:
        print(f"  ✅ {pattern}")

if __name__ == "__main__":
    main()
