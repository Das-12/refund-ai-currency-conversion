root@ecogo:/home/ecogo/k8s-backup/redis# kubectl get po -n redis
NAME             READY   STATUS    RESTARTS   AGE
redis-master-0   1/1     Running   0          6d22h
root@ecogo:/home/ecogo/k8s-backup/redis# kubectl get pvc -n redis
NAME                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-master-0   Bound    pvc-eeeb4fc2-9cd0-4120-aeef-f2a82ae4af26   5Gi        RWO            local-path     <unset>                 6d23h
root@ecogo:/home/ecogo/k8s-backup/redis# kubectl get svc -n redis
NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
redis            ClusterIP   10.104.107.174   <none>        6379/TCP         6d23h
redis-external   NodePort    10.110.44.9      <none>        6379:32379/TCP   6d23h
redis-master     ClusterIP   None             <none>        6379/TCP         6d23h
root@ecogo:/home/ecogo/k8s-backup/redis#

