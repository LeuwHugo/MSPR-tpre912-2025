#!/usr/bin/env bash
set -e
apt-get update -y && apt-get install -y nfs-common  # éventuellement facultatif

K3S_URL="https://192.168.56.10:6443"
curl -sfL https://get.k3s.io \
 | K3S_URL=$K3S_URL \
   K3S_TOKEN=$(cat /vagrant/node-token) sh -
