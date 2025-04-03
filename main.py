from fastapi import FastAPI, File, UploadFile, HTTPException
from fastai.vision.all import load_learner, PILImage
from pathlib import Path
import pathlib
import uvicorn

app = FastAPI()

# Monkey patch to map WindowsPath to PosixPath
temp = pathlib.WindowsPath
pathlib.WindowsPath = pathlib.PosixPath

# Load the model
MODEL_PATH = Path("export.pkl")
learn = load_learner(MODEL_PATH)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Architecture Style Classification API!"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Read the uploaded image
        img = PILImage.create(await file.read())
        
        # Get predictions
        pred_class, pred_idx, outputs = learn.predict(img)

        return {
            "predicted_class": str(pred_class),
            "predicted_index": int(pred_idx),
            "probabilities": outputs.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Restore the original WindowsPath to avoid future errors
    pathlib.WindowsPath = temp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)