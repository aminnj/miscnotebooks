#!/usr/bin/env sh


mkdir -p data/
for i in `seq 12 1000`; do
    x=$(curl -s "https://kubra.io/stormcenter/api/v1/stormcenters/dd9c446f-f6b8-43f9-8f80-83f5245c60a1/views/76446308-a901-4fa3-849c-3dd569933a51/currentState" | jq -r '.data.interval_generation_data') ;
    curl "https://kubra.io/$x/public/summary-1/data.json" | jq > data/data_$i.json
    sleep 300
done
