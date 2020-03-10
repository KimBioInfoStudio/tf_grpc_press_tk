#! python3
# coding: utf-8
# author: baochenx.yang@intel.com
# copyrights 2019 intel all rights  reserved


import sys
import time
import numpy as np
import grpc
import tensorflow as tf
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from argparse import ArgumentParser
import threading
import multiprocessing as mp


def grpc_task(stub,request,res,sleep):
    while True:
        time.sleep(sleep)
        start = time.time()
        resp = stub.Predict(request)
        delta = (time.time() - start)
        res.append(delta)

def grpc_threading_main(tag,host,port,model_name,signature_name,data,inputs_name,jobs=8,step=float(1/10**6),qpstgt=1500,avgtgt=None):
    print("="*32,file=sys.stderr)
    print("Setting",file=sys.stderr)
    print("-"*32,file=sys.stderr)
    print("host: {}".format(host),file=sys.stderr)
    print("port: {}".format(port),file=sys.stderr)
    print("model name: {} ".format(model_name),file=sys.stderr)
    print("signature name: {}".format(signature_name),file=sys.stderr)
    print("data: {}".format(data),file=sys.stderr)
    print("inputs_name: {}".format(inputs_name),file=sys.stderr)
    print("jobs: {}".format(jobs),file=sys.stderr)
    print("step: {}".format(step),file=sys.stderr)
    print("qpstgt: {}".format(qpstgt),file=sys.stderr)
    print("avgtgt: {}".format(avgtgt),file=sys.stderr)
    print("~"*32,file=sys.stderr)
    print("Test Start, Use `CTRL + C` to Stop It.",file=sys.stderr)
    print("="*32,file=sys.stderr)
    channel = implementations.insecure_channel(host,int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = model_name
    request.model_spec.signature_name = signature_name
    tensor = tf.make_tensor_proto(data,dtype=tf.float32)
    request.inputs[inputs_name].CopyFrom(tensor)
    res = []
    sleeptm = 0
    tds = [] 
    for i in range(jobs):
        tds.append( threading.Thread(target=grpc_task,args=(stub,request,res,sleeptm)))
    for each in  tds:
        each.start()

    while True:
        start = len(res)
        time.sleep(1)
        end = len(res)
        qps = end - start
        avg = np.average(res[start:end])
        p50 = np.percentile(res[start:end],50)
        p90 = np.percentile(res[start:end],90)
        print("Tag: {} QPS: {:.1f} SLEEP: {} AVG: {:.6f}s P50: {:.6f}s P90: {:.6f}s ".format(tag,qps,sleeptm,avg,p50,p90))
        if (qpstgt !=None) & (avgtgt == None):
            if qps > qpstgt:
                sleeptm += step
            elif qps < qpstgt:
                sleeptm = max(0, sleeptm - step)
        elif (qpstgt == None) & (avgtgt != None):
            if avg > avgtgt:
                sleeptm = max(0, sleeptm - step)
            elif avg < avgtgt:
                sleeptm += step
        else:
            print("[ Error ] qpstgt or avgtgt should be set mutulally exclusive!")
        if sleeptm <= 0:
            print("[ Warn ] Pls add more therads for better perfmance!")

def grpc_threading_test():
    host = "localhost"
    port = "8500"
    model_name = "half_plus_two"
    signature_name = "serving_default"
    data = [100]
    inputs_name = "x"
    jobs = 1
    step = float(1/10**8)
    tag = 0
    grpc_threading_main(tag,host,port,model_name,signature_name,data,inputs_name,jobs,step,qpstgt=3000,avgtgt=None)

def main():
    parser = ArgumentParser()
    parser.add_argument("-t","--tag",type=str,default="0",help="a debug log tag")
    parser.add_argument("-s","--host",type=str,default="localhost",help="inference grpc server ip adddress / domain")
    parser.add_argument("-p","--port",type=int,default=8500,help="inference grpc server port")
    parser.add_argument("-m","--model_name",type=str,help="model name")
    parser.add_argument("-n","--signature_name",type=str,help="signature name")
    parser.add_argument("-d","--data",type=str,help="input data in a list like [100,200,300] ")
    parser.add_argument("-i","--inputs_name",type=str,help="input name")
    parser.add_argument("-j","--jobs",type=int,help="threads to use")
    parser.add_argument("-z","--step",type=float,help="time step")
    parser.add_argument("-q","--qpstgt",type=int,default=None,help="qps target")
    parser.add_argument('-l',"--avgtgt",type=int,default=None,help="avg lantency target")
    args = parser.parse_args()
    grpc_threading_main(args.tag,args.host,args.port,args.model_name,args.signature_name,eval(args.data),args.inputs_name,args.jobs,args.step,args.qpstgt,args.avgtgt)

if __name__ =="__main__":
    # main()
    grpc_threading_test()
