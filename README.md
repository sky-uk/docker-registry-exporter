# docker-registry-exporter

Prometheus exporter for the opensource [Docker registry](https://github.com/docker/distribution)'s file storage system.

It is intended to run as a sidecar in Kubernetes mounting the same persistent volume as the Docker registry.

## Running the exporter

If running in Kubernetes, you can run the exporter as a sidecar container to your regular registry image:

```yaml
containers:
- image: registry:2
  name: registry
  ports:
  - containerPort: 5000
    name: http
    protocol: TCP
  readinessProbe:
    httpGet:
      path: /
      port: 5000
    initialDelaySeconds: 1
    timeoutSeconds: 1
  livenessProbe:
    httpGet:
      path: /
      port: 5000
    initialDelaySeconds: 1
    timeoutSeconds: 1
  volumeMounts:
  - name: storage
    mountPath: /var/lib/registry

- image: skyuk/docker-registry-exporter:v1.0.0
  name: registry-exporter
  args:
    - /var/lib/registry/docker/registry/v2
  ports:
  - containerPort: 8080
    name: http
    protocol: TCP
  volumeMounts:
  - name: storage
    mountPath: /var/lib/registry

volumes:
- name: storage
  persistentVolumeClaim:
    claimName: registry
```

## Metrics produced

The exporter produces four metrics:

 * `repository_tags_total` - a Gauge representing the number of tags for each repository in the registry
   * Labels: `repository`
 * `repository_revisions_total` - a Gauge representing the number of revisions for each repository in the registry
   * Labels: `repository`
 * `repository_tag_layers_total` - a Gauge representing the number of layers for each tag for each repository in the registry
   * Labels: `repository`, `tag`
 * `repository_tag_size_bytes` - a Gauge representing the sum of the size of each layer for each tag for each repository in the resitry
   * Labels: `repository`, `tag`

## Development

Please see our [Contributing guidelines](/CONTRIBUTING.md) for more information.

## Releasing

See instructions in eponymous section in `CONTRIBUTING.md`
