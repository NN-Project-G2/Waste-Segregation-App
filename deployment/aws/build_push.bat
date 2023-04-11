@echo off

cd /d %~dp0

set ACCOUNT_ID=765965856291
set REGION=ca-central-1
set APP_NAME_TAG="%ACCOUNT_ID%.dkr.ecr.%REGION%.amazonaws.com/waste-segregation-project:latest"

@REM remove --profile afifa to use default profile 
aws ecr get-login-password --region %REGION% --profile afifa | docker login --username AWS --password-stdin %ACCOUNT_ID%.dkr.ecr.%REGION%.amazonaws.com

@REM build the app image
docker build -t "%APP_NAME_TAG%" -f Dockerfile ../../. 

docker push "%APP_NAME_TAG%"
