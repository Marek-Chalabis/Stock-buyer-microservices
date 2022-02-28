#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python app.py run -h 0.0.0.0
