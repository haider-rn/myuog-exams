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
    "ds": "discrete structures data structures",
    "apl": "advanced programming language",
    "apt": "advanced programming techniques",
    "wst": "web system and technology",
    "is": "information security",
    "se": "software engineering",
    "ai": "artificial intelligence",
    "sna": "system and network administration",
    "dm": "data mining",
    "ml": "machine learning",
    "mc": "multivariable calculus math",
    "la": "linear algebra math",
    "iti": "information technology infrastructure",
    "els": "english language skills",
    "icp": "ideology and constitution of pakistan",
    "cce": "civic and community engagement",
    "rms": "role of media in sports",
    "stat": "introduction to statistics",
    "ffa": "fundamentals financial accounting",
    "fa": "financial accounting",
    "ent": "entrepreneurship",
    "ob": "organizational behavior",
    "brw": "business report writing",
    "eco": "economics eco",
    "awb": "advance web development",
    "os": "operating systems",
    "sre": "software requirement engineering",
    "db": "database systems",
    "vp": "visual programming",
    "vss": "virtual systems and services",
    "wt": "web technologies",
    "ms": "modeling and simulation",
    "dw": "data warehousing",
    "oc": "organic chemistry",
    "tafl": "theory of automata & formal languages",
    "atw": "academic and technical writing",
    "isl": "islamic studies islamiat",
    "ise": "Introduction to software engineering",
    "pdc": "parallel and distributed computing computer",
    "pp": "professional practices",
    "pk": "pakistan studies pak studies",
    "dsa": "data structures and algorithm",
    "coal": "computer organization and assembly language",
    "cc": "compiler construction",
    "ew": "expository writing",
    "de": "differential equations"
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
                
                # Strip out "-M" or "-E" or Prof names from the exam_type for grouping
                base_type = exam_type.split("-")[0]
                
                exam_id = f"{course_code}_{subject}_{term}_{year}_{base_type}"
                title = f"{course_code} - {subject} {term} {year} {exam_type.replace('-', ' ')}"
                
                # 1. Base Keywords
                search_codes = course_code.replace("-", " ").lower()
                subj_lower = subject.lower()
                keywords = f"{search_codes} {course_code.lower()} {subj_lower} {term.lower()} {year} {base_type.lower()}"
                
                # 2. Inject Full Subject Names
                if subj_lower in SUBJECT_EXPANSIONS:
                    keywords += f" {SUBJECT_EXPANSIONS[subj_lower]}"
                
                # 3. Smart Exam Type & Shift Injection
                suffix_full = "_".join(parts[4:]).lower() # Grabs everything after the Year
                
                if "mid" in suffix_full: keywords += " midterm mids"
                if "final" in suffix_full: keywords += " terminal finals"
                if suffix_full.endswith("-m"): keywords += " morning regular"
                if suffix_full.endswith("-e"): keywords += " evening replica self-support"
                
                # 4. Smart Professor Name Injection (Fixes multi-page bug)
                if "-" in suffix_full:
                    prof_part = suffix_full.split("-")[-1] # Gets whatever is after the last hyphen
                    if prof_part not in ["m", "e"]: # Make sure it's an actual name, not Morning/Evening
                        keywords += f" {prof_part} miss {prof_part} mam {prof_part} sir {prof_part}"
                
                folder_name = os.path.basename(root)
                path_prefix = f"{folder_name}/" if folder_name and folder_name != "." else ""
                url = f"{CDN_BASE}{path_prefix}{file}"
                
                # Since multiple pages loop through, only set title/keywords once, but append URLs
                if not exams_db[exam_id]["title"]:
                    exams_db[exam_id]["title"] = title
                    # Deduplicate keywords just to keep JSON tiny
                    unique_keywords = " ".join(list(set(keywords.split())))
                    exams_db[exam_id]["keywords"] = unique_keywords
                
                exams_db[exam_id]["urls"].append(url)

final_json = list(exams_db.values())
with open("exams.json", "w") as outfile:
    # Use separators to remove whitespace and keep the file as small as possible
    json.dump(final_json, outfile, separators=(',', ':'))

print(f"✅ Success! Generated exams.json with {len(final_json)} unique exams.")