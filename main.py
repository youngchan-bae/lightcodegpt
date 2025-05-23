from fastapi import FastAPI
from lightcode_api_blueprint import app as lightcode_app

app = FastAPI()

@app.get("/")
def root():
    return {"message": "빛의 코드가 실행 중입니다."}

# 기존 API 연결
app.mount("/", lightcode_app)


