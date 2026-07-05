import os
import shutil

# Target base path (Upwork folder)
upwork_base = "E:/PROJECTS/INTERN/UpWork/project_documentations"

# Mapping of source directories to target subdirectory names and filename prefixes
mapping = [
    {
        "source_dir": "D:/projects/rishi/cns-mvp/docs",
        "target_sub": "1_cyber_nervous_system",
        "prefix": "cns_technical_documentation"
    },
    {
        "source_dir": "D:/projects/BugBoumty/docs",
        "target_sub": "2_bugbounty_ai",
        "prefix": "bugbounty_technical_documentation"
    },
    {
        "source_dir": "D:/projects/Trading/docs",
        "target_sub": "3_apex_quant",
        "prefix": "apex_quant_technical_documentation"
    },
    {
        "source_dir": "E:/PROJECTS/INTERN/locaton_tracking/docs",
        "target_sub": "4_safetracker",
        "prefix": "safetracker_technical_documentation"
    },
    {
        "source_dir": "E:/PROJECTS/INTERN/PROJECT_ONE/breach-simu/docs",
        "target_sub": "5_iot_guardian_pro",
        "prefix": "iot_guardian_technical_documentation"
    },
    {
        "source_dir": "D:/projects/RoBlockSec/docs",
        "target_sub": "6_nexalith_prime",
        "prefix": "nexalith_technical_documentation"
    }
]

print("Starting to copy and organize files inside Upwork folder...")

for item in mapping:
    src_dir = item["source_dir"]
    sub_name = item["target_sub"]
    prefix = item["prefix"]
    
    # Define target path
    target_path = os.path.join(upwork_base, sub_name)
    os.makedirs(target_path, exist_ok=True)
    print(f"\nCreated folder: {target_path}")
    
    # Extensions to copy
    extensions = [".md", ".docx", ".pdf"]
    for ext in extensions:
        filename = f"{prefix}{ext}"
        src_file = os.path.join(src_dir, filename)
        dest_file = os.path.join(target_path, filename)
        
        if os.path.exists(src_file):
            shutil.copy2(src_file, dest_file)
            print(f"  Copied {filename} -> {sub_name}/")
        else:
            print(f"  [WARNING] File not found: {src_file}")

print("\nFiles successfully organized and placed in the Upwork folder!")
