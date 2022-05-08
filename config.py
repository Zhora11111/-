# PostgreSQL StatefulSet ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
    name: postgres-db-config
    labels:
        app: postgresql-db
data:
    POSTGRES_PASSWORD: test123
    PGDATA: /data/pgdata
---
# PostgreSQL StatefulSet Service
apiVersion: v1
kind: Service
metadata:
    name: postgres-db-lb
spec:
    selector:
        app: postgresql-db
    type: LoadBalancer
    ports:
    - port: 5432
    targetPort: 5432
---
# PostgreSQL StatefulSet
apiVersion: apps/v1
kind: StatefulSet
metadata:
    name: postgresql-db
spec:
    serviceName: postgresql-db-service
    selector:
        matchLabels:
            app: postgresql-db
    replicas: 2
    template:
        metadata:
            labels:
                app: postgresql-db
        spec:
            # Official Postgres Container
            containers:
            - name: postgresql-db
            image: postgres:10.4
            imagePullPolicy: IfNotPresent
            ports:
            - containerPort: 5432
            # Resource Limits
            resources:
                requests:
                    memory: "265Mi"
                    cpu: "250m"
                limits:
                    memory: "512Mi"
                    cpu: "500m"
            # Data Volume
            volumeMounts:
            - name: postgresql-db-disk
            mountPath: /data
            # Point to ConfigMap
            env:
            - configMapRef:
            name: postgres-db-config
# Volume Claim
volumeClaimTemplates:
    - metadata:
        name: postgresql-db-disk
    spec:
        accessModes: ["ReadWriteOnce"]
        resources:
            requests:
                storage: 25Gi