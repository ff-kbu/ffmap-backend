#!/bin/bash
PATH=${PATH}:/usr/local/sbin

set -e

DEST=$1


[ "$DEST" ] || exit 1

cd "$(dirname "$0")"/

./kbu.py registerNodes.json > aliases_kbu.json

./bat2nodes.py -a aliases.json -a aliases_kbu.json -d $DEST
