#!/bin/bash
script_dir=$(dirname $0)
until $script_dir/honeypot.py --file $1; do
    output="$(/bin/date '+%x %X') - Yalih crashed with exit code $?, restarting honeypot.py."
    echo -e "$output" >&2 >> crash.log
    python $script_dir/SendStatusEmail.py "$output"
    sleep 1
done
