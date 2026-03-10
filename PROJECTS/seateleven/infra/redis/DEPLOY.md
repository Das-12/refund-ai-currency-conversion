# Redis Deployment Instructions

## Files Overview

### Required Files (Apply these):
1. **redis-secret.yaml** - Contains the Redis password
2. **redis-configmap.yaml** - Contains redis.conf configuration
3. **redis-sts.yaml** - StatefulSet with password authentication
4. **redis-svc.yaml** - Services (already applied)

### NOT Required:
- **pvs.yaml** - This is an old PVC export from a different namespace, don't apply it

## Apply Commands (Run in order)

```bash
# 1. Apply Secret
kubectl apply -f redis-secret.yaml

# 2. Apply ConfigMap
kubectl apply -f redis-configmap.yaml

# 3. Apply StatefulSet (this will recreate the pod)
kubectl apply -f redis-sts.yaml

# 4. Delete the old pod to force recreation with new config
kubectl delete pod redis-master-0 -n infra

# 5. Wait for pod to be ready
kubectl wait --for=condition=ready pod/redis-master-0 -n infra --timeout=120s

# 6. Test authentication
kubectl exec -n infra redis-master-0 -- redis-cli -a RedisPassword123! ping
```

## Expected Result
- Redis will restart with password authentication enabled
- All services using `RedisPassword123!` will connect successfully
- Logging service error will be resolved
