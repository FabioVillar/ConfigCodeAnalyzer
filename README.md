# tcc
Comando para gerar um xml pelo terminal:
    srcml test.c -o test.c.xml     
Comando para fazer um POST Request usando a API:
    Invoke-WebRequest -Uri "http://localhost:8000/uploadFile" -Method POST -InFile "trash\test.c" -ContentType "multipart/form-data" -Headers @{"file_name"="test"}

Comando para fazer um GET Request usando a API:
    Invoke-RestMethod -Uri "http://localhost:8000/get_xml?file_name=example_file" -Method Get


