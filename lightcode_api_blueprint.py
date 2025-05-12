from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "빛의 코드가 실행 중입니다."}

@app.get("/openapi.json")
def get_openapi_json():
    return FileResponse("openapi.json", media_type="application/json")
from fastapi import Request

@app.post("/bojeong-oheng")
async def calculate_bojeong_oheng(request: Request):
    data = await request.json()
    birthdate = data.get("birthdate")

    # 여기에서 오행 계산 로직 넣으면 됨
    result = f"{birthdate} 기준 오행 보정 결과!"

    return {"result": result}
