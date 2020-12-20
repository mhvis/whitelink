#!/usr/bin/env bash
# This creates a symlink inside the CrewLink container for privkey.pem and
# fullchain.pem, pointing to the location where letsencrypt-nginx-proxy stores
# them.
set -e
ln -s -f /certs/$ADDRESS/fullchain.pem /app/fullchain.pem
ln -s -f /certs/$ADDRESS/key.pem /app/privkey.pem
exec "$@"
