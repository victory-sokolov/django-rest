#!/bin/bash

# Generate local Redis TLS certificates used by the Docker development image.
#
#   tls/ca.{crt,key}          Self signed CA certificate.
#   tls/redis.{crt,key}       A certificate with no key usage/policy restrictions.
#   tls/client.{crt,key}      A certificate restricted for SSL client usage.
#   tls/server.{crt,key}      A certificate restricted for SSL server usage.
#   tls/redis.dh              DH Params file.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
TLS_DIR="$SCRIPT_DIR/tls"

generate_cert() {
    local name=$1
    local cn="$2"
    local opts="$3"

    local keyfile="$TLS_DIR/${name}.key"
    local certfile="$TLS_DIR/${name}.crt"

    [ -f $keyfile ] || openssl genrsa -out $keyfile 2048
    openssl req \
        -new -sha256 \
        -subj "/O=Redis Test/CN=$cn" \
        -key $keyfile | \
        openssl x509 \
            -req -sha256 \
        -CA "$TLS_DIR/ca.crt" \
            -CAkey "$TLS_DIR/ca.key" \
            -CAserial "$TLS_DIR/ca.txt" \
            -CAcreateserial \
            -days 365 \
            $opts \
        -out "$certfile"
}

mkdir -p "$TLS_DIR"
[ -f "$TLS_DIR/ca.key" ] || openssl genrsa -out "$TLS_DIR/ca.key" 4096
openssl req \
    -x509 -new -nodes -sha256 \
    -key "$TLS_DIR/ca.key" \
    -days 3650 \
    -subj '/O=Redis Test/CN=Certificate Authority' \
    -out "$TLS_DIR/ca.crt"

cat > "$TLS_DIR/openssl.cnf" <<_END_
[ server_cert ]
keyUsage = digitalSignature, keyEncipherment
nsCertType = server

[ client_cert ]
keyUsage = digitalSignature, keyEncipherment
nsCertType = client
_END_

generate_cert server "Server-only" "-extfile $TLS_DIR/openssl.cnf -extensions server_cert"
generate_cert client "Client-only" "-extfile $TLS_DIR/openssl.cnf -extensions client_cert"
generate_cert redis "Generic-cert"

[ -f "$TLS_DIR/redis.dh" ] || openssl dhparam -out "$TLS_DIR/redis.dh" 2048
