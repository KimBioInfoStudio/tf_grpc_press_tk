#!python3
# coding: utf-8 
# author: baochenx.yang@intel.com 
# copyrights 2019 intel drd sae  all rights reserverd.


import redis
import time
import numpy as np
from argparse import ArgumentParser


def init_redis_db(rhost,rport,rdb):
    conn = redis.Redis(host=rhost,port=rport,db=rdb)
    signal = "start"
    conn.setnx("signal",signal)
    sleeptm = 0
    conn.setnx('sleeptm',sleeptm)
    conn.lpush('ela',0)


def master(mode,target,rhost,rport,rdb,step):
    ## init redis server
    conn = redis.Redis(host=rhost,port=rport,db=rdb)
    signal = "start"
    conn.setnx("signal",signal)
    sleeptm = 0 
    conn.setnx('sleeptm',sleeptm)
    conn.lpush('ela',0)
    before = time.time()
    ## qps/latency calculator
    while conn.get("signal") != "stop":
        start = conn.llen('ela')
        time.sleep(1)
        end = conn.llen('ela')
        res = [float(each) for each in conn.lrange('ela',start,end)]
        qps = end - start 
        avg = np.average(res)
        p50 = np.percentile(res,50)
        p90 = np.percentile(res,90)
        p99 = np.percentile(res,99)
        print("QPS: {:.1f} SLEEP: {}ms AVG: {:.6f}ms P50: {:.6f}ms P90: {:.6f}ms P99: {:.6f}".format(qps,sleeptm*1000,avg*1000,p50*1000,p90*1000,p99*1000))
        ## grid search sleeptm regressor 
        latency = {"avg":avg,"p50":p50,"p90":p90,"p99":p99}
        if mode ==  "qps":
            if qps > target:
                sleeptm += step
                conn.set("sleeptm",sleeptm)
            elif qps < target:
                sleeptm = max(0, sleeptm - step)
                conn.set("sleeptm",sleeptm)
        elif mode in latency.keys():
            if latency[mode] > target:
                sleeptm = max(0, sleeptm - step)
                conn.set("sleeptm", sleeptm)
            elif latency[mode]  < target:
                sleeptm += step
                conn.set("sleeptm",sleeptm)

        if sleeptm <= 10**(-7):
            print("[ Warn ] Please add more worker/therad for better perfmance!")
    after = time.time()

def main():
    parser = ArgumentParser()
    parser.add_argument("-m","--mode",type=str,default="qps",help="Test Mode in [qps,avg,p50,p90,p99]")
    parser.add_argument("-t","--target",type=float,default="10000",help="Test QPS/Latency Target")
    parser.add_argument("-r","--rhost",type=str,default="localhsot",help="Redis Server ip")
    parser.add_argument("-p","--rport",type=int,default=6379,help="Redis Server port")
    parser.add_argument("-d","--rdb",type=int,default=0,help="Redis Server db")
    parser.add_argument("-s","--step",type=float,default=float(1/10**7),help="Sleep Time Between Each RPC between 10**(-7)s and postive infinty")
    args= parser.parse_args()
    master(args.mode,args.target,args.rhost,args.rport,args.rdb,args.step)

if __name__ =="__main__":
    main()



