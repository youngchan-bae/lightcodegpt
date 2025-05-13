# rename_korean_files.py
import os

rename_map = {
    "메인.파이": "main.py",
    "오픈API.json": "openapi.json",
    "요구 사항.txt": "requirements.txt",
    "요구 사항.txt.txt": "delete_this.txt",
    "문서.txt": "guide.md",
    "prompt_templates.md.txt": "prompt_templates.md"
}

for old_name, new_name in rename_map.items():
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"✅ {old_name} → {new_name}")
    else:
        print(f"❌ {old_name} 파일 없음")
