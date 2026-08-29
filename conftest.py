import sys
from pathlib import Path

# asyncio 플러그인 활성화
pytest_plugins = ("pytest_asyncio",)

# conftest.py가 위치한 폴더(프로젝트 최상위 루트) 경로를 sys.path[0]에 추가
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))