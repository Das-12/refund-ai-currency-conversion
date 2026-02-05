root@ecogo:/home/ecogo/k8s-backup/nginx-ingress# kubectl get po -n kafka
NAME                            READY   STATUS    RESTARTS   AGE
kafka-broker-55bb59788d-6gzvd   1/1     Running   0          21h
zookeeper-6f7cf7f747-9bvpc      1/1     Running   0          21h
root@ecogo:/home/ecogo/k8s-backup/nginx-ingress# kubectl get svc -n kafka
NAME                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
kafka-service       ClusterIP   10.96.2.72     <none>        9092/TCP         21h
zookeeper-service   NodePort    10.99.10.154   <none>        2181:30181/TCP   21h
root@ecogo:/home/ecogo/k8s-backup/nginx-ingress#