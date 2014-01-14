#!/bin/bash

app_dir="$(readlink -f "$(dirname $0)/..")"

echo $$>"$app_dir/state/watch-for-files.pid"

while true; do
  inotifywait --quiet --event create --event move "$app_dir/input" && (
    "$app_dir/scripts/process.py"
  )
done
