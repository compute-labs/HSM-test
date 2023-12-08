#!/bin/bash
# Check for sudo privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as sudo user (use sudo)" 
   exit 1
fi
# Define the paths to the encrypted and decrypted .env files
ENCRYPTED_ENV_DB="/home/amd/App/postgres-docker/.env.db.aes"
DECRYPTED_ENV_DB="/home/amd/App/postgres-docker/.env.db"
KEY_FILE="/home/amd/derivedKey.bin"
# Decrypt the .env.db.aes file
openssl enc -aes-256-cbc -d -in "$ENCRYPTED_ENV_DB" -out "$DECRYPTED_ENV_DB" -pass file:"$KEY_FILE" -pbkdf2
#heck if decryption was successful
if [ -f "$DECRYPTED_ENV_DB" ]; then
    # Navigate to the directory containing the docker-compose.yml file
    cd /home/amd/App/postgres-docker

    # Launch docker-compose
    docker-compose up -d

    # Optionally remove the decrypted file for security
    rm "$DECRYPTED_ENV_DB"
else
    echo "Decryption failed. Unable to start the DATABASE"
    exit 1
fi
ENCRYPTED_ENV_FILE="/home/amd/App/.env.aes"
DECRYPTED_ENV_FILE="/home/amd/App/.env"

# Decrypt the .env.aes file
openssl enc -aes-256-cbc -d -in "$ENCRYPTED_ENV_FILE" -out "$DECRYPTED_ENV_FILE" -pass file:"$KEY_FILE" -pbkdf2

# Check if decryption was successful
if [ -f "$DECRYPTED_ENV_FILE" ]; then
    # Navigate to the directory containing main.py
    cd /home/amd/App
    # Load environment variables from the decrypted .env file
    source "$DECRYPTED_ENV_FILE"	
    source /home/amd/App/Appvenv/bin/activate
    # Start Uvicorn with the loaded environment variables
    uvicorn main:app --host 0.0.0.0 --port 80 --reload

    # Optionally remove the decrypted file for security
    rm "$DECRYPTED_ENV_FILE"
else
    echo "Decryption failed. Unable to start the application."
    exit 1
fi
