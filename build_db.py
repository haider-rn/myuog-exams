import os
import json
from collections import defaultdict

CDN_BASE = "https://cdn.jsdelivr.net/gh/haider-rn/myuog-exams@master/"

# 🧠 THE BRAIN: Map acronyms to what students actually type
SUBJECT_EXPANSIONS = {
    "pf": "programming fundamental fundamentals",
    "oop": "object oriented programming",
    "dld": "digital logic design",
    "dbms": "database management system",
    "ds": "data structure structures",
    "apl": "assembly programming language",
    "apt": "advanced programming techniques",
    "wst": "web system technologies technology",
    "is": "information security",
    "se": "software engineering",
    "ai": "artificial intelligence",
    "sna": "social network analysis",
    "dm": "data mining",
    "ml": "machine learning",
    "mc": "multivariable calculus math",
    "la": "linear algebra math",
    "iti": "intro to it introduction",
    "els": "english language skills",
    "icp": "ideology constitution of pakistan",
    "cce": "civic community engagement",
    "rms": "role of media in sports",
    "stat": "statistics stats",
    "ffa": "fundamentals financial accounting",
    "fa": "financial accounting",
    "ent": "entrepreneurship",
    "ob": "organizational behavior",
    "brw": "basic reading writing",
    "e": "economics eco"
}

exams_db = defaultdict(lambda: {"title": "", "keywords": "", "urls": []})

for root, dirs, files in os.walk("."):
    for file in sorted(files):
        if file.endswith(".webp"):
            clean_name = file.replace(".webp", "")
            parts = clean_name.split("_")
            
            if len(parts) >= 5:
                course_code = parts[0]
                subject = parts[1]
                term = parts[2]
                year = parts[3]
                exam_type = parts[4]
                
                exam_id = f"{course_code}_{subject}_{term}_{year}_{exam_type}"
                title = f"{course_code} - {subject} {term} {year} {exam_type.replace('-', ' ')}"
                
                # 1. Base Keywords
                search_codes = course_code.replace("-", " ").lower()
                subj_lower = subject.lower()
                keywords = f"{search_codes} {course_code.lower()} {subj_lower} {term.lower()} {year} {exam_type.lower()}"
                
                # 2. Inject Full Subject Names
                if subj_lower in SUBJECT_EXPANSIONS:
                    keywords += f" {SUBJECT_EXPANSIONS[subj_lower]}"
                
                # 3. Smart Exam Type & Shift Injection
                type_lower = exam_type.lower()
                if "mid" in type_lower: keywords += " midterm mids"
                if "final" in type_lower: keywords += " terminal finals"
                # Use .endswith() so it only triggers if the file literally ends in -m or -e
                if type_lower.endswith("-m"): keywords += " morning regular"
                if type_lower.endswith("-e"): keywords += " evening replica self-support"
                
                # 4. Smart Professor Name Injection (Extracts name after the dash, e.g., Mid-Hina)
                if "-" in exam_type and not exam_type.endswith("-M") and not exam_type.endswith("-E"):
                    prof_name = exam_type.split("-")[1].lower()
                    # Add common prefixes students use
                    keywords += f" {prof_name} miss {prof_name} mam {prof_name} sir {prof_name}"
                
                folder_name = os.path.basename(root)
                path_prefix = f"{folder_name}/" if folder_name and folder_name != "." else ""
                url = f"{CDN_BASE}{path_prefix}{file}"
                
                exams_db[exam_id]["title"] = title
                exams_db[exam_id]["keywords"] = keywords
                exams_db[exam_id]["urls"].append(url)

final_json = list(exams_db.values())
with open("exams.json", "w") as outfile:
    json.dump(final_json, outfile, separators=(',', ':'))

print(f"✅ Success! Generated exams.json with {len(final_json)} unique exams.")