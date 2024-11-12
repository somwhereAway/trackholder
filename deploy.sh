#!/bin/bash

cd app
docker build -t akromerd/trackholder_app .
docker push akromerd/trackholder_app

ssh vds_rf << 'EOF'
    echo @parol@ | sudo -S true
    cd trackholder
    sudo docker compose -f docker-compose.production.yml pull
    sudo docker compose -f docker-compose.production.yml down
    sudo docker compose -f docker-compose.production.yml up -d
EOF
