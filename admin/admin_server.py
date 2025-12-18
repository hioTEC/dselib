"""DSE Library 管理面板后端服务
提供脚本控制API，支持启动爬虫、索引器等操作
"""

import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime
from aiohttp import web

# 配置
HOST = '127.0.0.1'
PORT = 8088
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 存储运行中的进程
running_processes = {}


def log(message):
    """打印日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")


async def cors_middleware(app, handler):
    """CORS 中间件"""
    async def middleware_handler(request):
        if request.method == 'OPTIONS':
            return web.Response(headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            })
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return middleware_handler


# ============ API 路由 ============

def summarize_progress(state: dict) -> dict:
    """聚合进度信息，便于前端画进度条

    说明：
    - 旧实现直接依赖 state.progress[*].downloaded/found，但 scraper 重启后这些字段可能为 0，
      导致管理面板显示“进度丢失/计数不准”。
    - 新实现优先从持久化的 downloaded_files/failed_urls/seen_urls 推导“累计计数”，
      progress 仅作为补充（提供 total_urls 与 completed/timestamp）。
    """
    progress = state.get('progress', {}) or {}
    downloaded_files = state.get('downloaded_files', []) or []
    failed_urls = state.get('failed_urls', {}) or {}
    seen_urls = state.get('seen_urls', []) or []

    # 统计每科目累计 downloaded / failed / seen
    def _subject_from_url(u: str) -> str | None:
        # https://src.dselib.com/{subject}/{lang}/{year}/{file}
        if not isinstance(u, str):
            return None
        prefix = "https://src.dselib.com/"
        if not u.startswith(prefix):
            return None
        rest = u[len(prefix):]
        parts = rest.split("/")
        return parts[0] if parts and parts[0] else None

    subjects_set = set(progress.keys())
    subjects_set.update(filter(None, (_subject_from_url(u) for u in downloaded_files)))
    subjects_set.update(filter(None, (_subject_from_url(u) for u in failed_urls.keys())))
    subjects_set.update(filter(None, (_subject_from_url(u) for u in seen_urls)))

    per_subject = {k: {'downloaded': 0, 'failed': 0, 'seen': 0} for k in subjects_set}

    for u in downloaded_files:
        k = _subject_from_url(u)
        if k:
            per_subject.setdefault(k, {'downloaded': 0, 'failed': 0, 'seen': 0})
            per_subject[k]['downloaded'] += 1

    for u in failed_urls.keys():
        k = _subject_from_url(u)
        if k:
            per_subject.setdefault(k, {'downloaded': 0, 'failed': 0, 'seen': 0})
            per_subject[k]['failed'] += 1

    for u in seen_urls:
        k = _subject_from_url(u)
        if k:
            per_subject.setdefault(k, {'downloaded': 0, 'failed': 0, 'seen': 0})
            per_subject[k]['seen'] += 1

    subjects = []
    total_urls = 0
    total_downloaded = 0
    total_failed = 0
    total_seen = 0
    done = 0

    for key in sorted(subjects_set):
        info = progress.get(key, {}) or {}
        urls = info.get('total_urls', 0) or 0

        downloaded = per_subject.get(key, {}).get('downloaded', 0)
        failed = per_subject.get(key, {}).get('failed', 0)
        seen = per_subject.get(key, {}).get('seen', 0)

        completed = bool(info.get('completed'))
        # 进度优先用 seen/total_urls（更贴近“探测进度”）；若没有 seen 则用 downloaded
        denom = urls if urls else 0
        numerator = seen if seen else downloaded
        percent = round(numerator / denom * 100, 2) if denom else None

        subjects.append({
            'subject': key,
            'total_urls': urls,
            'downloaded': downloaded,
            'failed': failed,
            'seen': seen,
            'found': downloaded,  # 保持字段兼容：found 视为已下载（更可信）
            'percent': percent,
            'completed': completed,
            'timestamp': info.get('timestamp'),
        })

        total_urls += urls
        total_downloaded += downloaded
        total_failed += failed
        total_seen += seen
        if completed:
            done += 1

    overall_denom = total_urls
    overall_num = total_seen if total_seen else total_downloaded
    overall_percent = round(overall_num / overall_denom * 100, 2) if overall_denom else None

    return {
        'subjects': subjects,
        'overall': {
            'total_urls': total_urls,
            'downloaded': total_downloaded,
            'failed': total_failed,
            'seen': total_seen,
            'found': total_downloaded,
            'percent': overall_percent,
            'subjects_total': len(subjects),
            'subjects_done': done,
        }
    }


async def get_status(request):
    """获取系统状态"""
    state_file = os.path.join(BASE_DIR, 'scraper_state.json')
    state = {}
    
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except Exception as e:
            state = {'error': str(e)}
    
    # 检查进程状态
    processes = {}
    for name, proc in list(running_processes.items()):
        if proc.poll() is None:
            processes[name] = 'running'
        else:
            processes[name] = 'stopped'
            del running_processes[name]
    
    summary = summarize_progress(state)
    
    return web.json_response({
        'status': 'ok',
        'processes': processes,
        'state': {
            'downloaded_files': len(state.get('downloaded_files', [])),
            'failed_urls': len(state.get('failed_urls', {})),
            'last_update': state.get('last_update', None),
            'progress': state.get('progress', {}),
            'summary': summary
        },
        'files': {
            'downloaded': list(state.get('downloaded_files', []))[-100:],  # 最近100个
            'failed': dict(list(state.get('failed_urls', {}).items())[-50:])  # 最近50个
        }
    })


async def run_scraper(request):
    """启动爬虫"""
    data = await request.json() if request.body_exists else {}
    subjects = data.get('subjects', [])
    
    if 'scraper' in running_processes and running_processes['scraper'].poll() is None:
        return web.json_response({
            'status': 'error',
            'message': '爬虫已在运行中'
        }, status=400)
    
    cmd = [sys.executable, os.path.join(BASE_DIR, 'scraper.py')]
    if subjects:
        cmd.extend(subjects)
    
    log(f"启动爬虫: {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    running_processes['scraper'] = proc
    
    return web.json_response({
        'status': 'ok',
        'message': f'爬虫已启动，目标科目: {subjects if subjects else "全部"}'
    })


async def run_indexer(request):
    """运行索引器"""
    if 'indexer' in running_processes and running_processes['indexer'].poll() is None:
        return web.json_response({
            'status': 'error',
            'message': '索引器已在运行中'
        }, status=400)
    
    cmd = [sys.executable, os.path.join(BASE_DIR, 'indexer.py')]
    
    log(f"启动索引器: {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    running_processes['indexer'] = proc
    
    return web.json_response({
        'status': 'ok',
        'message': '索引器已启动'
    })


async def stop_process(request):
    """停止进程"""
    data = await request.json()
    name = data.get('name')
    
    if name in running_processes:
        proc = running_processes[name]
        if proc.poll() is None:
            proc.terminate()
            log(f"已停止: {name}")
            return web.json_response({
                'status': 'ok',
                'message': f'{name} 已停止'
            })
    
    return web.json_response({
        'status': 'error',
        'message': f'{name} 未在运行'
    }, status=400)


async def get_log(request):
    """获取日志内容"""
    log_file = os.path.join(BASE_DIR, 'scraper.log')
    lines = int(request.query.get('lines', 100))
    
    if not os.path.exists(log_file):
        return web.json_response({'log': ''})
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            content = ''.join(all_lines[-lines:])
        return web.json_response({'log': content})
    except Exception as e:
        return web.json_response({'log': f'读取日志失败: {e}'})


async def get_subjects(request):
    """获取可用科目列表"""
    # 从 scraper.py 导入科目列表
    subjects = {
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
    return web.json_response({'subjects': subjects})


async def clear_state(request):
    """清除爬虫状态"""
    state_file = os.path.join(BASE_DIR, 'scraper_state.json')
    
    if os.path.exists(state_file):
        # 备份后删除
        backup = state_file + '.bak'
        os.rename(state_file, backup)
        log(f"状态已清除，备份保存到: {backup}")
        return web.json_response({
            'status': 'ok',
            'message': '状态已清除'
        })
    
    return web.json_response({
        'status': 'ok',
        'message': '状态文件不存在'
    })


# ============ 应用启动 ============

def create_app():
    app = web.Application(middlewares=[cors_middleware])
    
    # 注册路由
    app.router.add_get('/api/status', get_status)
    app.router.add_get('/api/subjects', get_subjects)
    app.router.add_get('/api/log', get_log)
    app.router.add_post('/api/scraper/start', run_scraper)
    app.router.add_post('/api/indexer/start', run_indexer)
    app.router.add_post('/api/process/stop', stop_process)
    app.router.add_post('/api/state/clear', clear_state)
    
    return app


if __name__ == '__main__':
    print("=" * 50)
    print("DSE Library 管理后端服务")
    print(f"地址: http://{HOST}:{PORT}")
    print("=" * 50)
    print("\nAPI 列表:")
    print("  GET  /api/status      - 获取状态")
    print("  GET  /api/subjects    - 获取科目列表")
    print("  GET  /api/log         - 获取日志")
    print("  POST /api/scraper/start - 启动爬虫")
    print("  POST /api/indexer/start - 启动索引器")
    print("  POST /api/process/stop  - 停止进程")
    print("  POST /api/state/clear   - 清除状态")
    print("\n按 Ctrl+C 停止服务\n")
    
    app = create_app()
    web.run_app(app, host=HOST, port=PORT, print=None)
