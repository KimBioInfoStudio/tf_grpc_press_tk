import time
import redis
import grpc
import tensorflow as tf
from tensorflow_serving.apis import prediction_log_pb2
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
from argparse import ArgumentParser

def create_stub(hostport):
    channel = grpc.insecure_channel(hostport)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    return stub

def load_reqs(filePath):
    record_iterator = tf.io.tf_record_iterator(path=filePath)
    for string_record in record_iterator:
        p = prediction_log_pb2.PredictionLog.FromString(string_record)
        yield p.predict_log.request

def worker(stub, request, rhost, rport, rdb):
    conn = redis.Redis(host=rhost,port=rport,db=rdb)
    while conn.get("signal") != "stop":
        time.sleep(float(conn.get("sleeptm")))
        start = time.time()
        resp = stub.Predict(request,timeout=10)
        delta = (time.time() - start)
        conn.lpush('ela',delta)

def main():
    parser = ArgumentParser()
    parser.add_argument("-s","--hostport",type=str,default="localhsot",help="tensorflow model server `host:port` eg.  localhsot:8500 ")
    parser.add_argument("-f","--filePath",type=str,help="tensorflow records")
    parser.add_argument("-r","--rhost",type=str,default="localhost",help="redis host ip / domain")
    parser.add_argument("-p","--rport",type=int,default=6379,help="redis prot ")
    parser.add_argument("-d","--rdb",type=int,default=0,help="redis db")
    args = parser.parse_args()
    stub = create_stub(args.hostport)
    requests = load_reqs(args.filePath)
    request = [each for each in requests][0]
    worker(stub, request, args.rhost, args.rport, args.rdb)


if __name__ =="__main__":
    main()

