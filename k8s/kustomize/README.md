# Kustomize Example

This directory contains a Kustomize configuration example with a base layer and two environment overlays (dev and prod).

## Directory Structure

```
kustomize/
├── base/                    # Base configuration
│   ├── namespace.yaml       # Base namespace
│   ├── deployment.yaml      # Base deployment
│   ├── service.yaml         # Base service
│   └── kustomization.yaml   # Base kustomization
└── overlays/
    ├── dev/                 # Development overlay
    │   ├── kustomization.yaml
    │   └── deployment-patch.yaml
    └── prod/                # Production overlay
        ├── kustomization.yaml
        ├── deployment-patch.yaml
        └── service-patch.yaml
```

## Usage

### View the rendered manifests

```bash
# Development environment
kubectl kustomize k8s/kustomize/overlays/dev

# Production environment
kubectl kustomize k8s/kustomize/overlays/prod
```

### Apply to cluster

```bash
# Apply development configuration
kubectl apply -k k8s/kustomize/overlays/dev

# Apply production configuration
kubectl apply -k k8s/kustomize/overlays/prod
```

### Build and save manifests

```bash
# Build dev manifests
kustomize build k8s/kustomize/overlays/dev > dev-manifests.yaml

# Build prod manifests
kustomize build k8s/kustomize/overlays/prod > prod-manifests.yaml
```

## Environment Differences

### Development (dev)
- **Namespace**: `podinfo-dev`
- **Name prefix**: `dev-`
- **Replicas**: 1
- **Resources**: Lower (32Mi-64Mi memory, 50m-100m CPU)
- **Image**: `stefanprodan/podinfo:6.5.0`
- **UI Color**: Blue (#34577c)
- **Log Level**: debug
- **Feature Flags**: experimental

### Production (prod)
- **Namespace**: `podinfo-prod`
- **Name prefix**: `prod-`
- **Replicas**: 3
- **Resources**: Higher (128Mi-256Mi memory, 200m-500m CPU)
- **Image**: `stefanprodan/podinfo:6.5.4`
- **UI Color**: Green (#008000)
- **Log Level**: info
- **Feature Flags**: stable
- **Service Type**: LoadBalancer (vs ClusterIP in dev)
- **Security**: ReadOnly filesystem, non-root user
- **Monitoring**: Prometheus annotations

## Key Features Demonstrated

1. **Resource Patching**: Modifying base resources for each environment
2. **ConfigMap Generation**: Environment-specific configurations
3. **Namespace Management**: Different namespaces per environment
4. **Label Management**: Common and environment-specific labels
5. **Name Prefixing**: Resource naming conventions
6. **Replica Management**: Different scaling per environment
7. **Security Contexts**: Production hardening
8. **Service Type Override**: LoadBalancer for production 