#!/usr/bin/env python3
"""
DSE Library Maintain Script - 维护脚本
自动扫描 sources/ 目录，动态识别科目、考试类型、语言、年份
支持任意目录结构，无需修改代码
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ============ 配置 ============
BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
SOURCES_DIR = REPO_ROOT / "frontend" / "public" / "sources"
OUTPUT_DIR = REPO_ROOT / "frontend" / "public" / "data"
SUBJECTS_DIR = OUTPUT_DIR / "subjects"
PRODUCTION_DIR = Path("/var/www/dselib")
CONFIG_FILE = BASE_DIR / "subject_config.json"

# ============ 加载配置 ============
def load_config():
    """加载科目配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "subjects": {},
        "categories": {},
        "languages": {},
        "file_types": {},
        "special_years": {}
    }

CONFIG = load_config()

# ============ 工具函数 ============
def calculate_md5(file_path: Path) -> str:
    """计算文件MD5"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_year_display(year: str) -> str:
    """获取年份显示名称"""
    special_years = CONFIG.get("special_years", {})
    if year in special_years:
        return special_years[year]
    if year.lower().endswith('al'):
        return f"{year[:-2]} AL"
    return year

def get_file_type_info(filename: str) -> Dict:
    """获取文件类型信息"""
    file_types = CONFIG.get("file_types", {})
    return file_types.get(filename.lower(), {
        "type": "other",
        "type_name": filename,
        "paper_num": None
    })

def get_subject_info(subject_key: str) -> Dict:
    """获取科目信息"""
    subjects = CONFIG.get("subjects", {})
    return subjects.get(subject_key, {
        "name": subject_key.upper(),
        "name_zh": subject_key,
        "category": "Others",
        "icon": "fa-folder"
    })

def get_language_info(lang_key: str) -> Dict:
    """获取语言信息"""
    languages = CONFIG.get("languages", {})
    return languages.get(lang_key, {
        "name": lang_key.upper(),
        "name_zh": lang_key
    })

# ============ 核心扫描逻辑 ============
class DSEIndexer:
    def __init__(self):
        self.sources_dir = SOURCES_DIR
        self.output_dir = OUTPUT_DIR
        self.subjects_dir = SUBJECTS_DIR
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'by_subject': {},
            'by_exam_type': {},
            'last_updated': datetime.now().isoformat()
        }
        
    def scan_all(self):
        """扫描所有文件"""
        print("=" * 60)
        print("DSE Library Maintain Script")
        print(f"扫描目录: {self.sources_dir}")
        print("=" * 60)
        
        if not self.sources_dir.exists():
            print(f"[错误] 目录不存在: {self.sources_dir}")
            return {}
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.subjects_dir.mkdir(parents=True, exist_ok=True)
        
        subjects_data = {}
        
        # 遍历科目目录
        for subject_dir in sorted(self.sources_dir.iterdir()):
            if not subject_dir.is_dir():
                continue
            
            subject_key = subject_dir.name
            subject_info = get_subject_info(subject_key)
            
            print(f"\n[处理] {subject_info['name']} ({subject_info['name_zh']})")
            
            subject_data = self.scan_subject(subject_key, subject_dir, subject_info)
            subjects_data[subject_key] = subject_data
            
            # 保存单个科目索引
            self.save_subject_index(subject_key, subject_data)
        
        # 生成主索引
        self.generate_main_index(subjects_data)
        
        # 生成统计信息
        self.save_stats()
        
        print("\n" + "=" * 60)
        print(f"✅ 索引生成完成！")
        print(f"   总文件数: {self.stats['total_files']}")
        print(f"   总大小: {self.stats['total_size'] / 1024 / 1024:.2f} MB")
        print(f"   输出目录: {self.output_dir}")
        print("=" * 60)
        
        return subjects_data
    
    def scan_subject(self, subject_key: str, subject_dir: Path, subject_info: Dict) -> Dict:
        """扫描单个科目"""
        subject_data = {
            'key': subject_key,
            'name': subject_info['name'],
            'name_zh': subject_info['name_zh'],
            'category': subject_info['category'],
            'icon': subject_info['icon'],
            'exams': {}
        }
        
        # 遍历考试类型目录（动态识别）
        for exam_dir in sorted(subject_dir.iterdir()):
            if not exam_dir.is_dir():
                continue
            
            exam_type = exam_dir.name
            print(f"  - 考试类型: {exam_type}")
            
            exam_data = self.scan_exam_type(exam_type, exam_dir)
            if exam_data['years']:  # 只保存有数据的考试类型
                subject_data['exams'][exam_type] = exam_data
        
        return subject_data
    
    def scan_exam_type(self, exam_type: str, exam_dir: Path) -> Dict:
        """扫描考试类型"""
        exam_data = {
            'name': exam_type.upper(),
            'full_name': exam_type,
            'years': {}
        }
        
        # 遍历语言目录（动态识别）
        for lang_dir in sorted(exam_dir.iterdir()):
            if not lang_dir.is_dir():
                continue
            
            lang_key = lang_dir.name
            
            # 遍历年份目录（动态识别）
            for year_dir in sorted(lang_dir.iterdir()):
                if not year_dir.is_dir():
                    continue
                
                year = year_dir.name
                
                if year not in exam_data['years']:
                    exam_data['years'][year] = {
                        'display': get_year_display(year),
                        'languages': {}
                    }
                
                year_data = exam_data['years'][year]
                
                # 扫描文件
                files = self.scan_files(year_dir)
                if files:  # 只保存有文件的语言
                    lang_info = get_language_info(lang_key)
                    year_data['languages'][lang_key] = {
                        'name': lang_info['name'],
                        'files': files
                    }
        
        return exam_data
    
    def scan_files(self, year_dir: Path) -> List[Dict]:
        """扫描年份目录下的文件"""
        files = []
        
        for file_path in sorted(year_dir.iterdir()):
            if not file_path.is_file():
                continue
            
            filename = file_path.name
            file_size = file_path.stat().st_size
            
            # 计算相对路径（相对于 frontend 目录）
            try:
                relative_path = file_path.relative_to(REPO_ROOT / "frontend")
            except ValueError:
                relative_path = file_path
            
            # 获取文件类型信息
            file_type_info = get_file_type_info(filename)
            
            # 计算MD5
            md5_hash = calculate_md5(file_path)
            
            file_info = {
                'name': filename,
                'path': str(relative_path).replace('\\', '/'),
                'size': file_size,
                'type': file_type_info['type'],
                'type_name': file_type_info['type_name'],
                'paper_num': file_type_info['paper_num'],
                'md5': md5_hash
            }
            
            files.append(file_info)
            
            # 更新统计
            self.stats['total_files'] += 1
            self.stats['total_size'] += file_size
        
        return files
    
    def save_subject_index(self, subject_key: str, subject_data: Dict):
        """保存单个科目索引"""
        output_file = self.subjects_dir / f"{subject_key}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(subject_data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ 保存索引: {output_file.name}")
    
    def generate_main_index(self, subjects_data: Dict):
        """生成主索引"""
        main_index = {
            'subjects': {},
            'categories': CONFIG.get('categories', {}),
            'last_updated': datetime.now().isoformat()
        }
        
        # 按分类组织科目
        for subject_key, subject_data in subjects_data.items():
            category = subject_data['category']
            if category not in main_index['subjects']:
                main_index['subjects'][category] = []
            
            main_index['subjects'][category].append({
                'key': subject_key,
                'name': subject_data['name'],
                'name_zh': subject_data['name_zh'],
                'icon': subject_data['icon']
            })
        
        # 保存主索引
        output_file = self.output_dir / "index.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(main_index, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 保存主索引: {output_file}")
    
    def save_stats(self):
        """保存统计信息"""
        output_file = self.output_dir / "stats.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存统计: {output_file}")

# ============ 同步功能 ============
def sync_to_production():
    """同步到生产环境"""
    print("\n" + "=" * 60)
    print("同步到生产环境")
    print("=" * 60)
    
    # 同步核心文件
    core_files = ['index.html', 'manifest.json', 'sw.js']
    frontend_dir = REPO_ROOT / "frontend"
    
    for filename in core_files:
        src = frontend_dir / filename
        dst = PRODUCTION_DIR / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✓ 同步: {filename}")
    
    # 同步数据文件
    data_src = frontend_dir / "public" / "data"
    data_dst = PRODUCTION_DIR / "public" / "data"
    
    if data_dst.exists():
        shutil.rmtree(data_dst)
    shutil.copytree(data_src, data_dst)
    print(f"✓ 同步数据: public/data/")
    
    # 同步试卷文件
    sources_src = frontend_dir / "public" / "sources"
    downloads_dst = PRODUCTION_DIR / "public" / "downloads"
    
    if downloads_dst.exists():
        shutil.rmtree(downloads_dst)
    shutil.copytree(sources_src, downloads_dst)
    
    # 统计PDF数量
    pdf_count = len(list(downloads_dst.rglob("*.pdf")))
    print(f"✓ 同步试卷: public/downloads/ ({pdf_count} 个PDF)")
    
    print("\n✅ 同步完成！")
    print(f"   生产目录: {PRODUCTION_DIR}")

# ============ 主函数 ============
def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "index":
            # 只生成索引
            indexer = DSEIndexer()
            indexer.scan_all()
        
        elif command == "sync":
            # 只同步
            sync_to_production()
        
        elif command == "all":
            # 生成索引并同步
            indexer = DSEIndexer()
            indexer.scan_all()
            sync_to_production()
        
        else:
            print(f"未知命令: {command}")
            print("用法: python3 maintain.py [index|sync|all]")
    
    else:
        # 默认：生成索引并同步
        indexer = DSEIndexer()
        indexer.scan_all()
        sync_to_production()

if __name__ == "__main__":
    main()
