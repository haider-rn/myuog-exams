import os
import json
from collections import defaultdict

# Your exact jsDelivr CDN link is already set up here!
CDN_BASE = "https://cdn.jsdelivr.net/gh/haider-rn/myuog-exams@master/"

# Dictionary to group multi-page exams together
exams_db = defaultdict(lambda: {"title": "", "keywords": "", "urls": []})

# Walk through all folders and subfolders
for root, dirs, files in os.walk("."):
    for file in sorted(files):
        if file.endswith(".webp"):
            # Strip extension and split filename
            clean_name = file.replace(".webp", "")
            parts = clean_name.split("_")
            
            # Make sure it follows our 5-part rule
            if len(parts) >= 5:
                course_code = parts[0]
                subject = parts[1]
                term = parts[2]
                year = parts[3]
                exam_type = parts[4]
                
                # Create a unique ID ignoring page numbers (groups pg1, pg2 together)
                exam_id = f"{course_code}_{subject}_{term}_{year}_{exam_type}"
                
                # Build User-Friendly Title
                title = f"{course_code} - {subject} {term} {year} {exam_type.replace('-', ' ')}"
                
                # Build Search Keywords (lowercase for matching)
                search_codes = course_code.replace("-", " ").lower()
                keywords = f"{search_codes} {subject.lower()} {term.lower()} {year} {exam_type.lower()}"
                
                # Add extra smart keywords
                if "mid" in exam_type.lower(): keywords += " midterm"
                if "final" in exam_type.lower(): keywords += " terminal"
                if "-m" in exam_type.lower(): keywords += " morning regular"
                if "-e" in exam_type.lower(): keywords += " evening replica self-support"
                
                # Construct exact CDN URL
                folder_name = os.path.basename(root)
                path_prefix = f"{folder_name}/" if folder_name and folder_name != "." else ""
                url = f"{CDN_BASE}{path_prefix}{file}"
                
                # Populate Database
                exams_db[exam_id]["title"] = title
                exams_db[exam_id]["keywords"] = keywords
                exams_db[exam_id]["urls"].append(url)

# Export flat JSON array, minified to save bandwidth
final_json = list(exams_db.values())
with open("exams.json", "w") as outfile:
    json.dump(final_json, outfile, separators=(',', ':'))

print(f"✅ Success! Generated exams.json with {len(final_json)} unique exams.")