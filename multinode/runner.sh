#! /usr/bin/env bash
# coding: utf-8
# author: baochenx.yang@intel.com
# copyrights 2019 intel.com all rights reserved.


help(){
    echo -e "======================================================================="
    echo -e "                       Worker Runner "
    echo -e "-----------------------------------------------------------------------" 
    echo -e "ARGS\tTYPE\t DEFAULT         \tDESC"
    echo -e "  -h\t    \t                 \tPrint This Help Info"
    echo -e "  -j\t int\t 8               \tThreads Wanna Use"
    echo -e "  -s\t str\t localhost:8500  \tTensorflow gRPC Server ip:port"
    echo -e "  -f\t str\t ./inputs        \tTensorflow Input Records"
    echo -e "  -r\t str\t localhost       \tRedis Server ip"
    echo -e "  -p\t int\t 6379            \tRedis Server prot"
    echo -e "  -d\t int\t 0               \tRedis Sercer db "
    echo -e "eg."
    echo -e "$0 -h"
    echo -e "$0 -j 8 -s localhost:8500 -f ./inputs -r localhost -p 6379 -d 0"
    echo -e "========================================================================"

}

task(){
    for i in $(seq 1 $1)
        do
            python3 ./worker.py -s $2 -f $3 -r $4 -p $5 -d $6&
        done
    echo -e "Please Use `CTRL + C` to Close the Programe"
    wait
    
}


if [ $# -gt 0 ];then
    while getopts "hj:s:f:r:p:d:" args;
        do
                case $args in
                    h)
                    help
                    exit 0
                    ;;
                    j)
                    jobs=$OPTARG
                    ;;
                    s)
                    hostport=$OPTARG
                    ;;
                    f)
                    filePath=$OPTARG
                    ;;
                    r)
                    rserver=$OPTARG
                    ;;
                    p)
                    rport=$OPTARG
                    ;;
                    d)
                    rdb=$OPTARG
                    ;;
                    ?)
                    echo -e "[ ERROR ] Umm, Unknown arguments!"
                    exit 1
                    ;;
                esac
        done
        task $jobs $hostport $filePath $rserver $rport $rdb
else
    help
    exit 0
fi




