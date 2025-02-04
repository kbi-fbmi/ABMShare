DOCKER_NAME="zeppelin-$USER"
PORT=8080
echo "Running Zeppelin on port https://127.0.0.1:$PORT"
docker run -p 127.0.0.1:$PORT:8080 --rm \
-v $PWD/logs:/logs \
-v $PWD/outputs:/outputs \
-v $PWD/notebooks:/notebooks \
-e ZEPPELIN_LOG_DIR='/logs' \
-e ZEPPELIN_NOTEBOOK_DIR='/notebooks' \
--name $DOCKER_NAME apache/zeppelin:0.10.0
