"""DSE Library Scraper - v4 (High Speed)
Features:
  1. Full concurrent probing with asyncio.gather
  2. Direct GET without HEAD probe
  3. Minimal delays for maximum speed
"""

import os
import asyncio
import aiohttp
import aiofiles
import json
import random
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional, Set, Dict, List, Tuple
from pathlib import Path

# ============ 配置 ============
BASE_URL = "https://dselib.com"
FILE_BASE_URL = "https://src.dselib.com/"
BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
# Mirror files into the same place the indexer expects
DOWNLOAD_DIR = REPO_ROOT / "frontend" / "public" / "downloads"
STATE_FILE = BASE_DIR / "scraper_state.json"
LOG_FILE = BASE_DIR / "scraper.log"

# 爬虫设置 - 极速模式
MAX_CONCURRENT = 30  # 高并发
MIN_DELAY = 0.05     # 最小延时
MAX_DELAY = 0.1
MAX_RETRIES = 2      # 减少重试次数加快速度
TIMEOUT = 20
BATCH_SIZE = 50      # 每批并发数量

# 科目列表
SUBJECTS = {
    'chi': {'name': 'Chinese', 'name_zh': '中文'},
    'eng': {'name': 'English', 'name_zh': '英文'},
    'm0': {'name': 'Mathematics', 'name_zh': '數學'},
    'citizen': {'name': 'Citizenship', 'name_zh': '公民與社會發展'},
    'ls': {'name': 'Liberal Studies', 'name_zh': '通識'},
    'phy': {'name': 'Physics', 'name_zh': '物理'},
    'chem': {'name': 'Chemistry', 'name_zh': '化學'},
    'bio': {'name': 'Biology', 'name_zh': '生物'},
    'm1': {'name': 'Mathematics M1', 'name_zh': '數學M1'},
    'm2': {'name': 'Mathematics M2', 'name_zh': '數學M2'},
    'bafs': {'name': 'BAFS', 'name_zh': '企業會計財務'},
    'econ': {'name': 'Economics', 'name_zh': '經濟'},
    'chihist': {'name': 'Chinese History', 'name_zh': '中國歷史'},
    'enghist': {'name': 'History', 'name_zh': '世界歷史'},
    'geog': {'name': 'Geography', 'name_zh': '地理'},
    'ict': {'name': 'ICT', 'name_zh': '資訊科技'},
    'ths': {'name': 'Tourism', 'name_zh': '旅遊與款待'},
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/pdf",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


class ScraperState:
    def __init__(self):
        self.downloaded_files: Set[str] = set()
        self.failed_urls: Dict[str, str] = {}
        self.progress: Dict[str, Dict] = {}
        self.seen_urls: Set[str] = set()

    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.downloaded_files = set(data.get('downloaded_files', []))
                    self.failed_urls = data.get('failed_urls', {})
                    self.progress = data.get('progress', {})
                    # 回填 seen_urls 兼容旧状态文件
                    self.seen_urls = set(data.get('seen_urls', []))
                    if not self.seen_urls:
                        self.seen_urls.update(self.downloaded_files)
                        self.seen_urls.update(self.failed_urls.keys())
                    log(f"[状态] 已加载: {len(self.downloaded_files)} 已下载")
            except Exception as e:
                log(f"[警告] 加载状态失败: {e}")

    def _ensure_subject_progress(self, subject_key: str, total_urls: int | None = None):
        """确保 progress[subject_key] 存在，并包含累计字段（支持断点续跑/重启不丢进度）"""
        p = self.progress.get(subject_key) or {}
        p.setdefault('completed', False)
        if total_urls is not None:
            p['total_urls'] = int(total_urls)
        p.setdefault('downloaded_total', 0)
        p.setdefault('failed_total', 0)
        p.setdefault('seen_total', 0)
        p.setdefault('timestamp', datetime.now().isoformat())
        self.progress[subject_key] = p

    def save(self):
        data = {
            'downloaded_files': list(self.downloaded_files),
            'failed_urls': self.failed_urls,
            'progress': self.progress,
            'seen_urls': list(self.seen_urls),
            'last_update': datetime.now().isoformat()
        }
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def log(message: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + "\n")


# 支持的语言和考试类型
LANGUAGES = ['eng', 'chi']

# 年份范围配置 - 全量探测
YEAR_RANGES = {
    'dse': list(range(2012, 2026)) + ['pp', 'sp'],  # DSE: 2012-2025 + 练习卷/样卷
    'ce': list(range(1980, 2012)),  # CE: 1980-2011
    # HKAL 在源站用 “1994al” 这样的后缀表示，直接生成带 al 后缀的年份
    'al': [f"{y}al" for y in range(1980, 2014)],  # AL: 1980-2013
}

# 常见文件名模式 - 扩展
FILE_PATTERNS = [
    'p1.pdf', 'p2.pdf', 'p3.pdf',
    'p1a.pdf', 'p1b.pdf', 'p2a.pdf', 'p2b.pdf',
    'p4.pdf', 'p5.pdf',
    'ans.pdf', 'per.pdf', 'ms.pdf',
    'p1_ans.pdf', 'p2_ans.pdf',
    'mc.pdf', 'mc_ans.pdf',
    'aud.mp3',
]


def parse_file_links(html: str, subject_key: str) -> List[Dict]:
    """Parse subject page, extract all PDF links"""
    soup = BeautifulSoup(html, 'html.parser')
    files = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'src.dselib.com' in href and (href.endswith('.pdf') or href.endswith('.mp3')):
            try:
                parts = href.replace('https://src.dselib.com/', '').split('/')
                if len(parts) >= 4:
                    subj, lang, year, filename = parts[0], parts[1], parts[2], parts[3]
                    if subj == subject_key:
                        # 根据年份判断考试类型
                        year_lower = year.lower()
                        exam_type = 'dse'
                        if year_lower.endswith('al'):
                            exam_type = 'al'
                        elif year_lower in ('sp', 'pp'):
                            exam_type = 'dse'
                        else:
                            try:
                                y = int(year)
                                exam_type = 'dse' if y >= 2012 else 'ce'
                            except:
                                exam_type = 'dse'
                        files.append({
                            'url': href,
                            'subject': subj,
                            'lang': lang,
                            'year': year,
                            'filename': filename,
                            'exam_type': exam_type,
                        })
            except Exception as e:
                pass
    
    return files


def generate_all_urls(subject_key: str, base_files: List[Dict]) -> List[Dict]:
    """生成全量探测URL - 覆盖所有年份、语言、考试类型"""
    all_files = []
    seen_urls = set(f['url'] for f in base_files)
    
    # 加入已解析的文件
    all_files.extend(base_files)
    
    # 全量探测: 遍历所有考试类型和年份
    for exam_type, years in YEAR_RANGES.items():
        for year in years:
            year_str = str(year)
            for lang in LANGUAGES:
                for filename in FILE_PATTERNS:
                    new_url = f"https://src.dselib.com/{subject_key}/{lang}/{year_str}/{filename}"
                    if new_url not in seen_urls:
                        seen_urls.add(new_url)
                        all_files.append({
                            'url': new_url,
                            'subject': subject_key,
                            'lang': lang,
                            'year': year_str,
                            'filename': filename,
                            'exam_type': exam_type,
                            'is_probe': True,
                        })
    
    return all_files


class Scraper:
    def __init__(self):
        self.state = ScraperState()
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        self.session: Optional[aiohttp.ClientSession] = None
        self.downloaded_count = 0
        self.found_count = 0
        
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, limit_per_host=MAX_CONCURRENT)
        timeout = aiohttp.ClientTimeout(total=TIMEOUT)
        self.session = aiohttp.ClientSession(headers=HEADERS, timeout=timeout, connector=connector)
        self.state.load()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        self.state.save()

    async def fetch_subject_page(self, subject_key: str) -> str:
        """获取科目页面HTML"""
        url = f"{BASE_URL}/{subject_key}"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            log(f"获取页面失败: {url} - {e}", "ERROR")
        return ""
            
    async def download_file(self, file_info: Dict, referer: str) -> bool:
        """直接下载文件 (无HEAD探测)

        重要：此处同时维护 state.progress[*]_total 累计字段，确保重启后进度不回退。
        """
        url = file_info['url']
        subject_key = file_info.get('subject')

        # 构建保存路径
        save_path = DOWNLOAD_DIR / file_info['subject'] / file_info['exam_type'] / file_info['lang'] / file_info['year'] / file_info['filename']

        # 已下载跳过
        if url in self.state.downloaded_files and save_path.exists():
            return True
        # 已失败或已尝试过跳过
        if url in self.state.failed_urls or url in self.state.seen_urls:
            return False

        try:
            async with self.semaphore:
                await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                headers = {**HEADERS, 'Referer': referer}
                async with self.session.get(url, headers=headers) as response:
                    if response.status == 200:
                        content_type = response.headers.get('Content-Type', '')
                        if 'pdf' in content_type.lower() or 'octet-stream' in content_type.lower():
                            save_path.parent.mkdir(parents=True, exist_ok=True)
                            content = await response.read()
                            async with aiofiles.open(save_path, 'wb') as f:
                                await f.write(content)

                            self.state.downloaded_files.add(url)
                            self.state.seen_urls.add(url)
                            self.downloaded_count += 1
                            if file_info.get('is_probe'):
                                self.found_count += 1

                            # 累计进度（subject_key 可能为空，做保护）
                            if subject_key:
                                self.state._ensure_subject_progress(subject_key)
                                p = self.state.progress[subject_key]
                                p['downloaded_total'] = int(p.get('downloaded_total', 0)) + 1
                                p['seen_total'] = int(p.get('seen_total', 0)) + 1
                                p['timestamp'] = datetime.now().isoformat()

                            return True

                    elif response.status == 404:
                        self.state.failed_urls[url] = '404'
                        self.state.seen_urls.add(url)
                        if subject_key:
                            self.state._ensure_subject_progress(subject_key)
                            p = self.state.progress[subject_key]
                            p['failed_total'] = int(p.get('failed_total', 0)) + 1
                            p['seen_total'] = int(p.get('seen_total', 0)) + 1
                            p['timestamp'] = datetime.now().isoformat()
                        return False

                    else:
                        # 其它状态码也算“已尝试/已见过”，避免无限重试拖慢速度
                        self.state.failed_urls[url] = str(response.status)
                        self.state.seen_urls.add(url)
                        if subject_key:
                            self.state._ensure_subject_progress(subject_key)
                            p = self.state.progress[subject_key]
                            p['failed_total'] = int(p.get('failed_total', 0)) + 1
                            p['seen_total'] = int(p.get('seen_total', 0)) + 1
                            p['timestamp'] = datetime.now().isoformat()
                        return False
        except Exception:
            # 异常也记录为失败/已见过（可按需改为不记录，但会导致重启后重复尝试）
            self.state.failed_urls[url] = 'exception'
            self.state.seen_urls.add(url)
            if subject_key:
                self.state._ensure_subject_progress(subject_key)
                p = self.state.progress[subject_key]
                p['failed_total'] = int(p.get('failed_total', 0)) + 1
                p['seen_total'] = int(p.get('seen_total', 0)) + 1
                p['timestamp'] = datetime.now().isoformat()
            return False

        return False

    async def scrape_subject(self, subject_key: str, subject_info: Dict):
        """爬取单个科目 - 高速并发版"""
        log(f"\n{'='*50}")
        log(f"开始爬取: {subject_info['name']} ({subject_info['name_zh']})")
        log(f"{'='*50}")

        self.downloaded_count = 0
        self.found_count = 0

        # Step 1: 获取科目页面
        referer = f"{BASE_URL}/{subject_key}"
        html = await self.fetch_subject_page(subject_key)
        if not html:
            log(f"[失败] 无法获取科目页面: {subject_key}", "ERROR")
            return

        # Step 2: 解析页面 + 生成全量URL
        base_files = parse_file_links(html, subject_key)
        log(f"[解析] 页面可见文件: {len(base_files)} 个")

        all_files = generate_all_urls(subject_key, base_files)
        log(f"[全量] 总探测URL: {len(all_files)} 个")

        # 初始化/更新 progress（断点续跑不会丢）
        self.state._ensure_subject_progress(subject_key, total_urls=len(all_files))
        # 确保 completed 重置为 False（如果上次未完全成功但误标记）
        self.state.progress[subject_key]['completed'] = False
        self.state.progress[subject_key]['timestamp'] = datetime.now().isoformat()
        self.state.save()

        # Step 3: 分批并发下载
        total = len(all_files)
        for i in range(0, total, BATCH_SIZE):
            batch = all_files[i:i + BATCH_SIZE]
            tasks = [self.download_file(f, referer) for f in batch]
            await asyncio.gather(*tasks)

            # 保存进度
            self.state.save()
            progress = min(i + BATCH_SIZE, total)
            log(f"[进度] {progress}/{total} ({progress/total*100:.1f}%) - 本次运行下载 {self.downloaded_count}, 新发现 {self.found_count}")

        log(f"完成 {subject_info['name']}: 本次运行下载 {self.downloaded_count} 个文件 (新发现 {self.found_count})")

        # 标记完成，同时保留累计字段
        self.state._ensure_subject_progress(subject_key, total_urls=len(all_files))
        self.state.progress[subject_key]['completed'] = True
        # 兼容旧前端字段：downloaded/found 仍填“本次运行”统计
        self.state.progress[subject_key]['downloaded'] = self.downloaded_count
        self.state.progress[subject_key]['found'] = self.found_count
        self.state.progress[subject_key]['timestamp'] = datetime.now().isoformat()
        self.state.save()
        
    async def run(self, subjects: List[str] = None):
        """主运行函数"""
        log("=" * 60)
        log("DSE Library Scraper v4 启动 (高速并发版)")
        log(f"目标: {BASE_URL}")
        log(f"并发数: {MAX_CONCURRENT}, 批量大小: {BATCH_SIZE}")
        log("=" * 60)
        
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        
        target_subjects = subjects or list(SUBJECTS.keys())
        
        for subject_key in target_subjects:
            if subject_key not in SUBJECTS:
                log(f"未知科目: {subject_key}", "WARN")
                continue
                
            await self.scrape_subject(subject_key, SUBJECTS[subject_key])
            
        log("\n" + "=" * 60)
        log("爬取完成!")
        log(f"总计下载: {len(self.state.downloaded_files)} 文件")
        log(f"失败数量: {len(self.state.failed_urls)}")
        log("=" * 60)


async def main():
    import sys
    
    # 可以指定要爬取的科目，例如: python scraper.py phy chem bio
    subjects = sys.argv[1:] if len(sys.argv) > 1 else None
    
    async with Scraper() as scraper:
        await scraper.run(subjects)


if __name__ == "__main__":
    asyncio.run(main())
