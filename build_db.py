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
    "eco": "economics",
    "awd": "advance web development",
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
    "ise": "introduction to software engineering",
    "pdc": "parallel and distributed computing computer",
    "pp": "professional practices",
    "ps": "pakistan studies pak studies",
    "dsa": "data structures and algorithm",
    "coal": "computer organization and assembly language",
    "cc": "compiler construction",
    "ew": "expository writing",
    "de": "differential equations",
    "cn": "computer networks network",
    "soa": "service oriented architecture",
    "ca": "computer architecture",
    "toa&fl": "theory of automata and formal languages",
    "mad": "mobile application development",
    "idl": "intro to deep learning",
    "btw": "business and technical writing",
    "fe": "functional english",
    "ict": "application of information communication technologies",
    "cag": "calculus and analytical geometry",
    "pas": "probability and statistics",
    "adminm": "administration and management",
    "dbam": "database administration and management",
    "or": "operation research",
    "itpm": "it project management",
    "cs": "cyber security",
    "pom": "principles of marketing",
    "ap": "applied physics",
    "spm": "software project management"
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
                exam_type = parts[4] # e.g. "Mid-E-Usman"
                
                # 🚨 THE FIX: Group by everything EXCEPT the _pg1 / _pg2 suffix.
                # This keeps different professors/shifts completely separate!
                exam_id = "_".join(parts[:5]) 
                
                title = f"{course_code} - {subject} {term} {year} {exam_type.replace('-', ' ')}"
                
                # 1. Base Keywords
                search_codes = course_code.replace("-", " ").lower()
                subj_lower = subject.lower()
                keywords = f"{search_codes} {course_code.lower()} {subj_lower} {term.lower()} {year} {exam_type.split('-')[0].lower()}"
                
                # 2. Inject Full Subject Names
                if subj_lower in SUBJECT_EXPANSIONS:
                    keywords += f" {SUBJECT_EXPANSIONS[subj_lower]}"
                
                # 3. Smart Exam Type & Shift Injection
                suffix_full = "_".join(parts[4:]).lower() 
                
                if "mid" in suffix_full: keywords += " midterm mids"
                if "final" in suffix_full: keywords += " terminal finals"
                shift_tokens = suffix_full.split("-")
                
                if "m" in shift_tokens: keywords += " morning regular"
                if "e" in shift_tokens: keywords += " evening replica self-support"
                
                # 4. Smart Professor Name Injection
                if "-" in suffix_full:
                    prof_part = suffix_full.split("-")[-1] 
                    if prof_part not in ["m", "e"]: 
                        keywords += f" {prof_part} miss {prof_part} mam {prof_part} sir {prof_part}"
                
                folder_name = os.path.basename(root)
                path_prefix = f"{folder_name}/" if folder_name and folder_name != "." else ""
                url = f"{CDN_BASE}{path_prefix}{file}"
                
                if not exams_db[exam_id]["title"]:
                    exams_db[exam_id]["title"] = title
                    unique_keywords = " ".join(list(set(keywords.split())))
                    exams_db[exam_id]["keywords"] = unique_keywords
                
                exams_db[exam_id]["urls"].append(url)

final_json = list(exams_db.values())
with open("exams.json", "w") as outfile:
    json.dump(final_json, outfile, separators=(',', ':'))

print(f"✅ Success! Generated exams.json with {len(final_json)} unique exams.")