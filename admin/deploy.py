#!/usr/bin/env python3
"""
增量同步脚本 - 将开发目录同步到生产环境
只复制有变化的文件，提高效率
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import Set, Tuple

# 配置
SOURCE_DIR = Path("/root/dselib/frontend")
TARGET_DIR = Path("/var/www/dselib")

def calculate_md5(filepath: Path) -> str:
    """计算文件MD5"""
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()

def should_sync(src: Path, dst: Path) -> bool:
    """判断是否需要同步"""
    # 目标文件不存在
    if not dst.exists():
        return True
    
    # 大小不同
    if src.stat().st_size != dst.stat().st_size:
        return True
    
    # 修改时间不同（允许1秒误差）
    if abs(src.stat().st_mtime - dst.stat().st_mtime) > 1:
        return True
    
    return False

def sync_file(src: Path, dst: Path) -> bool:
    """同步单个文件"""
    try:
        # 确保目标目录存在
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制文件
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"[错误] 同步失败: {src} -> {dst}: {e}")
        return False

def sync_directory(src_dir: Path, dst_dir: Path, exclude: Set[str] = None) -> Tuple[int, int, int]:
    """
    同步目录
    返回: (新增文件数, 更新文件数, 跳过文件数)
    """
    if exclude is None:
        exclude = {'.git', '__pycache__', '.DS_Store', 'node_modules', '.vscode'}
    
    added = 0
    updated = 0
    skipped = 0
    
    for src_path in src_dir.rglob('*'):
        # 跳过目录
        if src_path.is_dir():
            continue
        
        # 跳过排除的文件
        if any(part in exclude for part in src_path.parts):
            continue
        
        # 计算相对路径
        rel_path = src_path.relative_to(src_dir)
        dst_path = dst_dir / rel_path
        
        # 判断是否需要同步
        if should_sync(src_path, dst_path):
            if dst_path.exists():
                print(f"[更新] {rel_path}")
                updated += 1
            else:
                print(f"[新增] {rel_path}")
                added += 1
            
            sync_file(src_path, dst_path)
        else:
            skipped += 1
    
    return added, updated, skipped

def clean_orphaned_files(src_dir: Path, dst_dir: Path) -> int:
    """
    清理孤立文件（源目录中不存在但目标目录中存在的文件）
    返回: 删除的文件数
    """
    deleted = 0
    
    for dst_path in dst_dir.rglob('*'):
        if dst_path.is_dir():
            continue
        
        rel_path = dst_path.relative_to(dst_dir)
        src_path = src_dir / rel_path
        
        if not src_path.exists():
            print(f"[删除] {rel_path}")
            dst_path.unlink()
            deleted += 1
            
            # 删除空目录
            try:
                dst_path.parent.rmdir()
            except OSError:
                pass
    
    return deleted

def main():
    """主函数"""
    print("=" * 60)
    print("DSE Library 增量同步")
    print("=" * 60)
    print(f"源目录: {SOURCE_DIR}")
    print(f"目标目录: {TARGET_DIR}")
    print()
    
    # 确保目标目录存在
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    # 同步核心文件
    print("[1/3] 同步核心文件...")
    core_files = ['index.html', 'manifest.json', 'sw.js']
    core_added = 0
    core_updated = 0
    
    for filename in core_files:
        src = SOURCE_DIR / filename
        dst = TARGET_DIR / filename
        
        if not src.exists():
            print(f"[警告] 文件不存在: {filename}")
            continue
        
        if should_sync(src, dst):
            if dst.exists():
                print(f"[更新] {filename}")
                core_updated += 1
            else:
                print(f"[新增] {filename}")
                core_added += 1
            sync_file(src, dst)
    
    print(f"核心文件: 新增 {core_added}, 更新 {core_updated}")
    print()
    
    # 同步数据文件
    print("[2/3] 同步数据文件...")
    data_src = SOURCE_DIR / "public" / "data"
    data_dst = TARGET_DIR / "public" / "data"
    
    data_added, data_updated, data_skipped = sync_directory(data_src, data_dst)
    print(f"数据文件: 新增 {data_added}, 更新 {data_updated}, 跳过 {data_skipped}")
    print()
    
    # 同步试卷文件
    print("[3/3] 同步试卷文件...")
    sources_src = SOURCE_DIR / "public" / "sources"
    downloads_dst = TARGET_DIR / "public" / "downloads"
    
    pdf_added, pdf_updated, pdf_skipped = sync_directory(sources_src, downloads_dst)
    print(f"试卷文件: 新增 {pdf_added}, 更新 {pdf_updated}, 跳过 {pdf_skipped}")
    print()
    
    # 统计
    total_added = core_added + data_added + pdf_added
    total_updated = core_updated + data_updated + pdf_updated
    total_skipped = data_skipped + pdf_skipped
    
    print("=" * 60)
    print("同步完成!")
    print(f"新增文件: {total_added}")
    print(f"更新文件: {total_updated}")
    print(f"跳过文件: {total_skipped}")
    print("=" * 60)

if __name__ == "__main__":
    main()
