# Kubernetes deployment notes

Build and tag the image for your cluster, then apply `deployment.yaml`.
Create a `fraud-db` Secret with key `database-url` and provision Redis/PostgreSQL
inside the target cluster first. Do not commit credentials to Git. The manifest is
a starter and does not include ingress, autoscaling, network policies, resource limits,
or a production secret-management integration.
