# Deep Learning Serving Server Workload Performance Test Tools Kit

> Those Tools Developed for Intel  Internal Use Only.

## Setup gRPC server
- make sure docker have installed on your  machine
- start docker service
    ```
    sudo service docker start
    ```
- pull tensorflow serving latest  images
    ```
    sudo docker pull tensorflow/serving:latest
    ```
- clone offical source code form github
    ```
    git clone https://github.com/tensorflow/serving.git
    ```
- strat offical demo
    ```
    TESTDATA="$(pwd)/serving/tensorflow_serving/servables/tensorflow/testdata"
    docker run -t -p 8501:8501  -p 8500:8500 \
               -v "$TESTDATA/saved_model_half_plus_two_cpu:/models/half_plus_two" \
                -e MODEL_NAME=half_plus_two \
                       tensorflow/serving &
    ```
- test restful api via curl
    ```
    curl --noproxy localhost -d "{\"instances\":[1000,2000,3000]}" -X POST http://localhost:8501/v1/models/half_plus_two:predict
    # cong ! if u got respson as below:
    # { "predictions": [2.5, 3.0, 4.5] }
    ```
- *[Warnning]* MAKE SURE DO NOT SET PRXOY TO http://localhost
    ```
    export no_proxy="localhost,127.0.0.1"
    ```
## Preinstall
- Python >= 3.6 & venv
    ```
    python3 -m venv dl_perf_tk
    cd dl_perf_tk
    source ./bin/activate
    ```
## Install
- install Python Package
    ```
    git clone root@192.168.14.231:/home/kim/workload/tf_model_grpc_server_test_tk
    cd tf_model_grpc_server_test_tk
    python3 -m pip install -r requirements.txt
    ```

## Usage
- use python std module threading
    ```
    python3 grpc_tf_model_server_performance_test_threading.py -h
    ```
-  use python std module multiprocessing
    ```
    python3 grpc_tf_model_server_performance_test_multiprocess.py -h
    ```
- use python 3rd party module  gevent
    ```
    python3 grpc_tf_model_server_performance_test_gevent.py -h
    ```
- use shell warper multi process
    ```
    bash run.sh  -h
    ```

