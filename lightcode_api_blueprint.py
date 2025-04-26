from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "빛의 코드가 실행 중입니다."}

@app.get("/openapi.json")
def get_openapi_json():
    return FileResponse("openapi.json", media_type="application/json")
