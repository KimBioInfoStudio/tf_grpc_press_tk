# Tensorflow Model Serving gRPC Workload Test Tool Kit
> this tool kit developed by baochenx.yang@intel.com for intel drd sae lab internal use only.

## PreInstall
- Redis>=5.0.7
- Python >= 3.6
- docker

## Setup Tensorflow Model server
- make sure latest version of docker have installed in your machine
    ```
    service docker  start 
    ```
- pull offical image
    ```
    docker pull tensorflow/serving:latest
    ```
- run in a docker 
    ```
    docker run -t -p 8500:8500 -p 8501:8501 -v /path/to/saved_model:/models/model_name -e MODEL_NAME=model_name tensorflow/serving & 
    ```
- run in bare 
    ```
    tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=model_name --model_base_path=path/to/model_name
    ```
- test
    ```
    python3 test.py
    ```
## Setup  Redis Server
- make sure redis have installed in your machine or a docker 
    ```
    redis-server
    ```
## Test
- Start Master
    ```
    python3 master.py -h
    ```
- start Worker
    ```
    runner.sh -h 
    ```
- stop master 
    ```
    ctrl + c
    ```
- stop worker
    ```
    pkill pthon3 
    ```


