#!/bin/bash
set -e

echo "Installing PM2 globally..."
npm install -g pm2

echo "Installing PM2 logrotate module..."
pm2 install pm2-logrotate

echo "Configuring PM2 logrotate..."
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 10
pm2 set pm2-logrotate:compress true
pm2 set pm2-logrotate:dateFormat 'YYYY-MM-DD_HH-mm-ss'
pm2 set pm2-logrotate:rotateModule true
pm2 set pm2-logrotate:workerInterval 30
pm2 set pm2-logrotate:rotateInterval '0 0 * * *'

echo "Setting up PM2 startup script..."
pm2 startup

echo "Creating logs directory..."
mkdir -p logs

echo "PM2 setup complete!"
echo ""
echo "To start all applications:"
echo "  pm2 start ecosystem.config.js"
echo ""
echo "To save the process list:"
echo "  pm2 save"
echo ""
echo "To monitor processes:"
echo "  pm2 monit"
