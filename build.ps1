Write-Host(" ================================ ")
Write-Host(" == ZAP WAVES GENERATOR BUILD == ")
Write-Host(" ================================ ")

# build da imagem
docker build . -t zap_waves

# remove container existente
docker rm -f zap_waves_container

# executa um novo container
docker run -d --name zap_waves_container zap_waves
