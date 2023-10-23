import subprocess
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
import xml_reader, os

app = FastAPI()

class CodeInput(BaseModel):
    code: str
    file_name: str

@app.post("/uploadFile")
async def upload_file(file: UploadFile):
    if file:
        try:
            folder_path = r"C:\Users\fabio\OneDrive\Área de Trabalho\tcc repo\uploadedFiles"
            file_path = os.path.join(folder_path, file.filename)
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            xml_output_path = os.path.join(folder_path, f"{file.filename}.xml")
            try:
                srcml_command = f'srcml "{file_path}" -o "{xml_output_path}"'
                subprocess.run(srcml_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                return {"message": "Arquivo enviado com sucesso."}
            except Exception as e:
                print(f"Erro ao executar srcml: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Arquivo não foi recebido.")

@app.get("/getFile")
async def get_json(file_name: str):
    try:
        folder_path = r"C:\Users\fabio\OneDrive\Área de Trabalho\tcc repo\uploadedFiles"
        xml_file_path = os.path.join(folder_path, f"{file_name}.c.xml")
        xml_file_name = file_name + ".c.xml"
        
        if not os.path.exists(xml_file_path):
            raise HTTPException(status_code=404, detail=f"Arquivo XML não encontrado: {xml_file_path}")
        
        json_name = xml_reader.main(xml_file_name)
        json_file_path = "jsonFiles/" + json_name

        if not os.path.exists(json_file_path):
            raise HTTPException(status_code=404, detail=f"Arquivo JSON não encontrado: {json_file_path}")
        
        with open(json_file_path, "r") as json_file:
            json_content = json_file.read()
        
        json_response = FileResponse(json_file_path)
        return json_response
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if  __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
