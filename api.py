from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
import subprocess
import xml_reader, os

app = FastAPI()

class CodeInput(BaseModel):
    code: str
    file_name: str

@app.post("/uploadFile")
async def upload_file(file: UploadFile, file_name: str):
    if file:
        try:
            with open(file.filename, "wb") as f:
                f.write(file.file.read())
                try:
                    os.system(f"srcml {file.filename} -o {file.filename}.xml")
                    return {"message": "Arquivo enviado com sucesso."}
                except Exception as e:
                    print(f"Erro ao executar srcml: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Arquivo não foi recebido.")  

@app.get("/getFile")
async def get_xml(file_name: str):
    try:
        with open(f"{file_name}.c.xml", "r") as xml_file:
            json_name = xml_reader.main(file_name+'.c.xml')
            try:
                with open(f"{json_name}.c.xml", "r") as json_file:
                    return json_file
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
