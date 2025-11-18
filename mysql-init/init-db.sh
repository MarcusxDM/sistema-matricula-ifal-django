#!/bin/sh
set -e

DB_NAME=${MYSQL_DATABASE:-sistemadb}
DB_USER=${MYSQL_USER:-sistemadbuser}
DB_PASS=${MYSQL_PASSWORD:-sistemadbpass}
ROOT_PASS=${MYSQL_ROOT_PASSWORD:-}

echo "[mysql-init] Using DB_NAME=$DB_NAME DB_USER=$DB_USER"

# Helper to run mysql command
run_mysql() {
  if [ -S "/var/run/mysqld/mysqld.sock" ]; then
    if [ -n "$ROOT_PASS" ]; then
      mysql --protocol=SOCKET -S /var/run/mysqld/mysqld.sock -uroot -p"$ROOT_PASS" "$@"
    else
      mysql --protocol=SOCKET -S /var/run/mysqld/mysqld.sock -uroot "$@"
    fi
  else
    # fallback to TCP on localhost
    if [ -n "$ROOT_PASS" ]; then
      mysql -uroot -p"$ROOT_PASS" -h 127.0.0.1 --protocol=TCP "$@"
    else
      mysql -uroot -h 127.0.0.1 --protocol=TCP "$@"
    fi
  fi
}

echo "[mysql-init] Waiting for MySQL to accept connections..."
n=0
until run_mysql -e "SELECT 1" >/dev/null 2>&1; do
  n=$((n+1))
  if [ $n -gt 60 ]; then
    echo "[mysql-init] Timeout waiting for MySQL to become available" >&2
    exit 1
  fi
  sleep 1
done

echo "[mysql-init] Creating database '$DB_NAME' if not exists and user '$DB_USER'..."
run_mysql <<-EOSQL
  CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  CREATE USER IF NOT EXISTS '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASS}';
  GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'%';
  FLUSH PRIVILEGES;
EOSQL

echo "[mysql-init] Done."

exit 0
