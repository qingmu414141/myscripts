import os
import json
import time
import hashlib
import requests
from pathlib import Path
from huggingface_hub import HfApi, list_repo_files
from tqdm import tqdm
import concurrent.futures
from urllib.parse import urlparse, unquote

def calculate_md5(file_path):
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def download_file(url, file_path, resume=False, expected_md5=None, max_retries=3):
    """
    支持断点续传的文件下载函数
    
    参数:
        url: 文件URL
        file_path: 本地文件路径
        resume: 是否尝试续传
        expected_md5: 预期的文件MD5值
        max_retries: 最大重试次数
    """
    headers = {}
    file_size = 0
    
    # 处理文件保存路径
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # 检查文件是否存在并获取大小（用于续传）
    if os.path.exists(file_path) and resume:
        file_size = os.path.getsize(file_path)
        headers = {'Range': f'bytes={file_size}-'}
    
    # 重试机制
    for attempt in range(max_retries):
        try:
            with requests.get(url, headers=headers, stream=True, timeout=30) as r:
                r.raise_for_status()
                
                # 处理不同响应状态
                total_size = int(r.headers.get('content-length', 0)) + file_size
                mode = 'ab' if file_size > 0 and resume else 'wb'
                
                # 进度条
                progress_bar = tqdm(
                    total=total_size, 
                    initial=file_size, 
                    unit='B', 
                    unit_scale=True,
                    desc=os.path.basename(file_path),
                    leave=False
                )
                
                # 写入文件
                with open(file_path, mode) as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))
                
                progress_bar.close()
                
                # 检查文件完整性
                if expected_md5:
                    actual_md5 = calculate_md5(file_path)
                    if actual_md5 != expected_md5:
                        raise ValueError(f"MD5 mismatch: expected {expected_md5}, got {actual_md5}")
                
                # 返回下载状态
                status = "resumed" if file_size > 0 else "downloaded"
                return file_path, status, total_size, actual_md5 if expected_md5 else None
        
        except (requests.RequestException, ValueError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                tqdm.write(f"下载失败 [{file_path}]，{str(e)}，{wait_time}秒后重试...")
                time.sleep(wait_time)
                continue
            else:
                raise RuntimeError(f"无法下载 {file_path}: {str(e)}") from e

def load_or_create_state(state_file):
    """加载或创建下载状态"""
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {'files': {}, 'repo': None}
    return {'files': {}, 'repo': None}

def save_state(state_file, state):
    """保存下载状态"""
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def get_file_url(repo_id, file_path, revision="main"):
    """生成文件下载URL"""
    # 处理中文文件名
    file_path = unquote(file_path)
    return f"https://huggingface.co/{repo_id}/resolve/{revision}/{file_path}"

def download_huggingface_repo(repo_id, save_dir=".", revision="main", max_workers=4, resume=True):
    """
    从Hugging Face下载仓库文件（支持断点续传）
    
    参数:
        repo_id: Hugging Face仓库ID (格式: "username/repo_name")
        save_dir: 本地保存目录 (默认: 当前目录)
        revision: 仓库分支/版本 (默认: "main")
        max_workers: 最大并发下载数量
        resume: 是否启用续传
    """
    # 设置状态文件路径
    state_file = os.path.join(save_dir, f"{repo_id.replace('/', '_')}_download_state.json")
    state = load_or_create_state(state_file)
    
    # 如果仓库信息变更，重置状态
    if state['repo'] != repo_id or not state.get('revision') == revision:
        tqdm.write(f"仓库信息变更或首次下载，初始化状态文件")
        state = {'files': {}, 'repo': repo_id, 'revision': revision}
        save_state(state_file, state)
    
    # 创建API实例并获取文件列表
    api = HfApi()
    all_files = list(list_repo_files(repo_id, revision=revision))
    
    # 过滤.git文件和目录
    files_to_download = [
        file for file in all_files 
        if not (".git" in file or file.endswith('/') or file.endswith('.gitattributes'))
    ]
    
    # 进度条计数器
    total_files = len(files_to_download)
    skipped = 0
    resumed = 0
    downloaded = 0
    failed = []
    
    # 创建进度条
    main_bar = tqdm(total=total_files, desc="总体进度")
    
    # 处理下载任务
    def process_file(file):
        nonlocal skipped, resumed, downloaded, failed
        
        file_path = os.path.join(save_dir, file)
        file_state = state['files'].get(file, {})
        url = get_file_url(repo_id, file, revision)
        
        # 检查文件是否需要下载
        if os.path.exists(file_path):
            if file_state.get('md5'):
                current_md5 = calculate_md5(file_path)
                if current_md5 == file_state['md5'] and os.path.getsize(file_path) == file_state['size']:
                    skipped += 1
                    main_bar.update(1)
                    return file, "skipped", file_state['size'], file_state['md5']
        
        # 执行下载
        try:
            result = download_file(
                url, 
                file_path, 
                resume=resume, 
                expected_md5=file_state.get('md5'),
                max_retries=3
            )
            file_path, status, size, md5 = result
            
            # 更新状态
            state['files'][file] = {
                'size': size,
                'md5': md5,
                'timestamp': int(time.time())
            }
            save_state(state_file, state)
            
            if status == "resumed":
                resumed += 1
            else:
                downloaded += 1
            
            return result
        
        except Exception as e:
            failed.append(file)
            raise e
        finally:
            main_bar.update(1)
    
    # 使用线程池并发下载
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(process_file, file): file 
            for file in files_to_download
        }
        
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as e:
                tqdm.write(f"文件下载失败 [{file}]: {str(e)}")
    
    main_bar.close()
    
    # 打印总结
    print("\n下载完成!")
    print(f"仓库: {repo_id} (版本: {revision})")
    print(f"保存路径: {os.path.abspath(save_dir)}")
    print(f"文件总数: {total_files}")
    print(f"跳过文件: {skipped}")
    print(f"续传文件: {resumed}")
    print(f"新下载文件: {downloaded}")
    
    if failed:
        print(f"失败文件: {len(failed)}")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='下载Hugging Face仓库')
    parser.add_argument('repo_id', type=str, help='Hugging Face仓库ID (格式: username/repo_name)')
    parser.add_argument('--save_dir', type=str, default='.', help='保存目录 (默认: 当前目录)')
    parser.add_argument('--revision', type=str, default='main', help='仓库版本或分支 (默认: main)')
    parser.add_argument('--workers', type=int, default=4, help='并发下载数量 (默认: 4)')
    parser.add_argument('--no-resume', action='store_true', help='禁用断点续传')
    args = parser.parse_args()
    
    download_huggingface_repo(
        repo_id=args.repo_id,
        save_dir=args.save_dir,
        revision=args.revision,
        max_workers=args.workers,
        resume=not args.no_resume
    )