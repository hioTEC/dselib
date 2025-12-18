"""
DSE Library Indexer v2 - 索引生成器
目录结构: downloads/{subject}/{exam_type}/{lang}/{year}/{files}

文件类型:
- p1.pdf, p1a.pdf, p1b.pdf, p2.pdf, p3.pdf - 试卷
- ans.pdf - Marking Scheme (评卷参考)
- per.pdf - Examination Report (考试报告)
"""

import os
import json
import re
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

# ============ 配置 ============
BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
ROOT_DIR = REPO_ROOT / "papers"
OUTPUT_DIR = REPO_ROOT / "frontend" / "public" / "data"
MAIN_INDEX = "index.json"
MISSING_REPORT = "missing_report.json"
STATS_FILE = "stats.json"

# ============ 科目定义 ============
SUBJECTS = {
    'chi': {'name': 'Chinese', 'name_zh': '中文', 'category': 'Core', 'icon': 'fa-language', 'color': 'red'},
    'eng': {'name': 'English', 'name_zh': '英文', 'category': 'Core', 'icon': 'fa-font', 'color': 'orange'},
    'm0': {'name': 'Mathematics', 'name_zh': '數學', 'category': 'Core', 'icon': 'fa-calculator', 'color': 'blue'},
    'citizen': {'name': 'Citizenship', 'name_zh': '公民與社會發展', 'category': 'Core', 'icon': 'fa-users', 'color': 'teal'},
    'ls': {'name': 'Liberal Studies', 'name_zh': '通識教育', 'category': 'Core', 'icon': 'fa-newspaper', 'color': 'teal'},
    'phy': {'name': 'Physics', 'name_zh': '物理', 'category': 'Science', 'icon': 'fa-atom', 'color': 'purple'},
    'chem': {'name': 'Chemistry', 'name_zh': '化學', 'category': 'Science', 'icon': 'fa-flask', 'color': 'purple'},
    'bio': {'name': 'Biology', 'name_zh': '生物', 'category': 'Science', 'icon': 'fa-dna', 'color': 'purple'},
    'm1': {'name': 'Mathematics M1', 'name_zh': '數學延伸M1', 'category': 'Science', 'icon': 'fa-chart-line', 'color': 'blue'},
    'm2': {'name': 'Mathematics M2', 'name_zh': '數學延伸M2', 'category': 'Science', 'icon': 'fa-superscript', 'color': 'blue'},
    'bafs': {'name': 'BAFS', 'name_zh': '企業會計財務', 'category': 'Commerce', 'icon': 'fa-briefcase', 'color': 'yellow'},
    'econ': {'name': 'Economics', 'name_zh': '經濟', 'category': 'Commerce', 'icon': 'fa-chart-pie', 'color': 'yellow'},
    'chihist': {'name': 'Chinese History', 'name_zh': '中國歷史', 'category': 'Arts', 'icon': 'fa-scroll', 'color': 'pink'},
    'enghist': {'name': 'History', 'name_zh': '世界歷史', 'category': 'Arts', 'icon': 'fa-landmark', 'color': 'pink'},
    'geog': {'name': 'Geography', 'name_zh': '地理', 'category': 'Arts', 'icon': 'fa-globe-asia', 'color': 'green'},
    'ict': {'name': 'ICT', 'name_zh': '資訊及通訊科技', 'category': 'Technology', 'icon': 'fa-laptop-code', 'color': 'cyan'},
    'ths': {'name': 'Tourism', 'name_zh': '旅遊與款待', 'category': 'Others', 'icon': 'fa-plane', 'color': 'gray'},
}

# 考试类型
EXAM_TYPES = {
    'dse': {'name': 'HKDSE', 'full_name': '香港中學文憑考試', 'year_range': (2012, 2025)},
    'ce': {'name': 'HKCEE', 'full_name': '香港中學會考', 'year_range': (1978, 2011)},
    'al': {'name': 'HKAL', 'full_name': '香港高級程度會考', 'year_range': (1980, 2013)},
    'hyc': {'name': 'HYC Mock', 'full_name': '學友社模擬試卷', 'year_range': (2015, 2025)},
}

# 语言
LANGUAGES = {
    'eng': {'name': 'English', 'name_zh': '英文'},
    'chi': {'name': 'Chinese', 'name_zh': '中文'},
}

# 文件类型
FILE_TYPES = {
    'p1.pdf': {'type': 'paper', 'name': 'Paper 1', 'paper_num': 1},
    'p1a.pdf': {'type': 'paper', 'name': 'Paper 1A', 'paper_num': 1},
    'p1b.pdf': {'type': 'paper', 'name': 'Paper 1B', 'paper_num': 1},
    'p2.pdf': {'type': 'paper', 'name': 'Paper 2', 'paper_num': 2},
    'p3.pdf': {'type': 'paper', 'name': 'Paper 3', 'paper_num': 3},
    'p4.pdf': {'type': 'paper', 'name': 'Paper 4', 'paper_num': 4},
    'p5.pdf': {'type': 'paper', 'name': 'Paper 5', 'paper_num': 5},
    'ans.pdf': {'type': 'marking', 'name': 'Marking Scheme', 'paper_num': None},
    'per.pdf': {'type': 'report', 'name': 'Exam Report', 'paper_num': None},
    'aud.mp3': {'type': 'audio', 'name': 'Audio', 'paper_num': None},
}

# 特殊年份
SPECIAL_YEARS = {
    'pp': 'Practice Paper',
    'sp': 'Sample Paper',
}

# 分类
CATEGORIES = {
    'Core': {'icon': 'fa-book', 'color': 'blue', 'name_zh': '核心科目'},
    'Science': {'icon': 'fa-flask', 'color': 'purple', 'name_zh': '理科'},
    'Commerce': {'icon': 'fa-briefcase', 'color': 'yellow', 'name_zh': '商科'},
    'Arts': {'icon': 'fa-palette', 'color': 'pink', 'name_zh': '文科'},
    'Technology': {'icon': 'fa-laptop', 'color': 'cyan', 'name_zh': '科技'},
    'Others': {'icon': 'fa-folder', 'color': 'gray', 'name_zh': '其他'},
}


def calculate_md5(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def normalize_year_to_int(year: str) -> Optional[int]:
    """Normalize year strings (e.g., 1994al) to integer for stats/summaries"""
    if year in SPECIAL_YEARS:
        return None
    y = year.lower()
    if y.endswith('al'):
        y = y[:-2]
    try:
        return int(y)
    except:
        return None


def get_year_display(year: str, exam_type: str = None) -> str:
    """获取年份显示名称"""
    if year in SPECIAL_YEARS:
        return SPECIAL_YEARS[year]
    if year.lower().endswith('al'):
        return f"{year[:-2]} AL"
    # HYC Mock 年份显示为 "2022 Mock"
    if exam_type and exam_type.lower() == 'hyc':
        return f"{year} Mock"
    return year


def generate_index():
    """生成索引"""
    print("=" * 60)
    print("DSE Library Indexer v2 启动")
    print(f"扫描目录: {ROOT_DIR}")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    subjects_data: Dict[str, Dict] = {}
    stats = {
        'total_files': 0,
        'total_size': 0,
        'by_exam_type': {},
        'by_category': {},
        'by_subject': {},
        'by_year': {},
        'last_updated': datetime.now().isoformat()
    }
    missing_data = {}
    
    if not os.path.exists(ROOT_DIR):
        print(f"[错误] 目录不存在: {ROOT_DIR}")
        return
        
    # 遍历科目
    for subject_key in os.listdir(ROOT_DIR):
        subject_path = os.path.join(ROOT_DIR, subject_key)
        if not os.path.isdir(subject_path):
            continue
            
        # 获取科目信息
        subject_info = SUBJECTS.get(subject_key, {
            'name': subject_key,
            'name_zh': subject_key,
            'category': 'Others',
            'icon': 'fa-folder',
            'color': 'gray'
        })
        
        print(f"\n[处理] {subject_info['name']} ({subject_info['name_zh']})")
        
        subject_data = {
            'key': subject_key,
            'name': subject_info['name'],
            'name_zh': subject_info['name_zh'],
            'category': subject_info['category'],
            'icon': subject_info['icon'],
            'color': subject_info['color'],
            'exams': {},  # exam_type -> {years: {year -> {lang -> [files]}}}
            'file_count': 0,
            'total_size': 0,
            'years_summary': {}
        }
        
        # 遍历考试类型
        for exam_type in os.listdir(subject_path):
            exam_path = os.path.join(subject_path, exam_type)
            if not os.path.isdir(exam_path):
                continue
                
            exam_type_lower = exam_type.lower()
            exam_info = EXAM_TYPES.get(exam_type_lower, {
                'name': exam_type.upper(),
                'full_name': exam_type,
                'year_range': (1980, 2025)
            })
            
            if exam_type_lower not in subject_data['exams']:
                subject_data['exams'][exam_type_lower] = {
                    'name': exam_info['name'],
                    'full_name': exam_info['full_name'],
                    'years': {}
                }
                
            exam_data = subject_data['exams'][exam_type_lower]
            
            # 遍历语言
            for lang in os.listdir(exam_path):
                lang_path = os.path.join(exam_path, lang)
                if not os.path.isdir(lang_path):
                    continue
                    
                lang_lower = lang.lower()
                
                # 遍历年份
                for year in os.listdir(lang_path):
                    year_path = os.path.join(lang_path, year)
                    if not os.path.isdir(year_path):
                        continue
                        
                    if year not in exam_data['years']:
                        exam_data['years'][year] = {
                            'display': get_year_display(year, exam_type_lower),
                            'languages': {}
                        }
                        
                    year_data = exam_data['years'][year]
                    
                    if lang_lower not in year_data['languages']:
                        year_data['languages'][lang_lower] = {
                            'name': LANGUAGES.get(lang_lower, {}).get('name', lang),
                            'files': []
                        }
                        
                    lang_data = year_data['languages'][lang_lower]
                    
                    # 遍历文件
                    for filename in os.listdir(year_path):
                        file_path = os.path.join(year_path, filename)
                        if not os.path.isfile(file_path):
                            continue
                            
                        file_size = os.path.getsize(file_path)
                        relative_path = os.path.relpath(file_path, start=REPO_ROOT / "frontend")
                        
                        file_type_info = FILE_TYPES.get(filename.lower(), {
                            'type': 'other',
                            'name': filename,
                            'paper_num': None
                        })
                        
                        file_info = {
                            'name': filename,
                            'path': relative_path.replace('\\', '/'),
                            'size': file_size,
                            'type': file_type_info['type'],
                            'type_name': file_type_info['name'],
                            'paper_num': file_type_info['paper_num'],
                            'md5': calculate_md5(file_path)
                        }
                        
                        lang_data['files'].append(file_info)
                        subject_data['file_count'] += 1
                        subject_data['total_size'] += file_size
                        
                        # 更新统计
                        stats['total_files'] += 1
                        stats['total_size'] += file_size
                        stats['by_exam_type'][exam_type_lower] = stats['by_exam_type'].get(exam_type_lower, 0) + 1
                        stats['by_category'][subject_info['category']] = stats['by_category'].get(subject_info['category'], 0) + 1
                        stats['by_subject'][subject_key] = stats['by_subject'].get(subject_key, 0) + 1
                        norm_year = normalize_year_to_int(year)
                        if norm_year is not None:
                            stats['by_year'][str(norm_year)] = stats['by_year'].get(str(norm_year), 0) + 1
                            
        subjects_data[subject_key] = subject_data
        print(f"  -> {subject_data['file_count']} 文件, {len(subject_data['exams'])} 考试类型")
        
    # 生成输出
    
    # 1. 分科目JSON
    subjects_dir = os.path.join(OUTPUT_DIR, 'subjects')
    os.makedirs(subjects_dir, exist_ok=True)
    
    for subject_key, subject_data in subjects_data.items():
        subject_file = os.path.join(subjects_dir, f"{subject_key}.json")
        with open(subject_file, 'w', encoding='utf-8') as f:
            json.dump(subject_data, f, ensure_ascii=False, indent=2)
            
    print(f"\n[输出] 科目数据: {len(subjects_data)} 个文件")
    
    # 2. 主索引
    import copy
    index_subjects = []
    
    for subject_key, subject_data in subjects_data.items():
        index_subjects.append(subject_data)
        
        # 年份汇总
        for exam_type, exam_data in subject_data['exams'].items():
            years = []
            for y in exam_data['years'].keys():
                norm = normalize_year_to_int(y)
                if norm is not None:
                    years.append(norm)
            if years:
                subject_data['years_summary'][exam_type] = {
                    'min': min(years),
                    'max': max(years),
                    'count': len(set(years))
                }
        
    # 按分类分组
    categories_list = []
    for cat_name, cat_info in CATEGORIES.items():
        cat_subjects = [s['key'] for s in index_subjects if s['category'] == cat_name]
        if cat_subjects:
            categories_list.append({
                'name': cat_name,
                'name_zh': cat_info['name_zh'],
                'icon': cat_info['icon'],
                'color': cat_info['color'],
                'subjects': cat_subjects
            })
            
    index_data = {
        'subjects': index_subjects,
        'categories': categories_list,
        'exam_types': [
            {
                'key': key,
                'name': info['name'],
                'full_name': info['full_name'],
                'year_range': info['year_range']
            }
            for key, info in EXAM_TYPES.items()
        ],
        'languages': [
            {'key': key, 'name': info['name'], 'name_zh': info['name_zh']}
            for key, info in LANGUAGES.items()
        ],
        'stats': stats
    }
    
    with open(os.path.join(OUTPUT_DIR, MAIN_INDEX), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    print(f"[输出] 主索引: {MAIN_INDEX}")
    
    # 3. 缺漏报告
    with open(os.path.join(OUTPUT_DIR, MISSING_REPORT), 'w', encoding='utf-8') as f:
        json.dump(missing_data, f, ensure_ascii=False, indent=2)
    print(f"[输出] 缺漏报告: {MISSING_REPORT}")
    
    # 4. 统计信息
    with open(os.path.join(OUTPUT_DIR, STATS_FILE), 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"[输出] 统计信息: {STATS_FILE}")
    
    print("\n" + "=" * 60)
    print("索引生成完成!")
    print(f"总计科目: {len(subjects_data)}")
    print(f"总计文件: {stats['total_files']}")
    print(f"总计大小: {stats['total_size'] / 1024 / 1024:.2f} MB")
    print("=" * 60)


if __name__ == "__main__":
    generate_index()
