#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "Esperando o MySQL em $host ficar pronto..."
until mysqladmin ping -h "$host" --silent; do
  echo "MySQL ainda não está pronto - esperando..."
  sleep 2
done

echo "MySQL está pronto! Executando comando..."
exec $cmd
