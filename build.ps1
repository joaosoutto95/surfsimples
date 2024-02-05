Write-Host(" ================================ ")
Write-Host(" == SURF SIMPLES GENERATOR BUILD == ")
Write-Host(" ================================ ")

# build da imagem
docker build . -t surfsimples

# remove container existente
docker rm -f surfsimples_container

# executa um novo container
docker run -d --name surfsimples_container surfsimples
