from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "빛의 코드가 실행 중입니다."}
