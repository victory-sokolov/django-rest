#!/bin/bash

CERT_FILE="$(pwd)/certs/fullchain.pem"

# Get the expiration date
EXPIRATION_DATE=$(openssl x509 -in "$CERT_FILE" -noout -dates | grep notAfter | cut -d= -f2)

# Convert to a timestamp
EXPIRATION_TIMESTAMP=$(date -j -f "%b %d %T %Y" "$EXPIRATION_DATE" +"%s")
CURRENT_TIMESTAMP=$(date +"%s")

if [ "$CURRENT_TIMESTAMP" -gt "$EXPIRATION_TIMESTAMP" ]; then
    echo "The certificate has expired."
else
    echo "The certificate is valid. Expiration date: $EXPIRATION_DATE"
fi

openssl verify "$CERT_FILE"
