#!/usr/bin/env bash
set -e

# 1. K3s (Traefik désactivé)
curl -sfL https://get.k3s.io \
 | INSTALL_K3S_EXEC="--disable traefik --node-ip 192.168.56.10" sh -

# 2. Dépendances minimales
apt-get update -y
apt-get install -y nfs-common curl

# 3. Helm 3 via script officiel (pas le dépôt APT 403)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 4. Token worker
cat /var/lib/rancher/k3s/server/node-token > /vagrant/node-token
