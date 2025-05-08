from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from dicom_processor import process_dicom

dicomCalculator = FastAPI()

#ignore CORS
dicomCalculator.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@dicomCalculator.post("/upload")
async def upload_dicom(dicom_file: UploadFile = File(...)):
    try:
        # TODO add proper validation
        if not dicom_file.filename.lower().endswith('.dcm'):
            raise ValueError("Invalid file format. Please upload a DICOM file.")
        
        # Read the uploaded file into memory
        file_content = await dicom_file.read()
        dicom_buffer = BytesIO(file_content)
        return process_dicom(dicom_buffer)

    except Exception as e:
        # TODO add error handling
        return {"error": str(e)}  