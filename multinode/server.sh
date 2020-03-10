numactl --cpubind 0 --membind 0 /home/kim/source/serving/bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server --port=8500 --rest_api_port=8501 --model_name=wd_20190516_click --model_base_path=/models/wd_20190516_click
#docker run -t -p 8500:8500 -p 8501:8501 -v /home/kim/workload/tf_grpc_server_test_tk/model:/models/wd_20190516_click -e MODEL_NAME=wd_20190516_click tensorflow/serving &


