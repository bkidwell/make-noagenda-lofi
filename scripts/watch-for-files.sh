#!/bin/bash

app_dir="$(readlink -f "$(dirname $0)/..")"
run="$app_dir/scripts/process.py"

echo $$>"$app_dir/state/watch-for-files.pid"

sleep 5
"$run"

while true; do
  inotifywait --quiet --event create --event move "$app_dir/input" && (
    sleep 5
    "$run"
  )
done
