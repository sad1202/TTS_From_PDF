from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import uuid
from App.services.main_service import Main_service

router = APIRouter(prefix="/document", tags=["Document Processing"])
service = Main_service()

UPLOAD_DIR = "./storage/uploads"
OUTPUT_DIR = "./storage/outputs"

@router.post("/process")
async def process_document(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    temp_filename = f"{file_id}{ext}"
    input_path = os.path.join(UPLOAD_DIR, temp_filename)

    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file: {str(e)}")

    try:
        mp3_path = await service.run_async(input_path)
        print(mp3_path)
        if mp3_path and os.path.exists(mp3_path):
            
            return {
                "status": "success",
                "message": "Xử lý thành công",
                "file_name": os.path.basename(mp3_path),
                "download_url": f"/document/download/{os.path.basename(mp3_path)}"
            }
        else:
            raise HTTPException(status_code=500, detail="Không thể tạo file âm thanh")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename=filename)
    raise HTTPException(status_code=404, detail="File không tồn tại")