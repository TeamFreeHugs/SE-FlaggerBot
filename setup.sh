#!/bin/bash
echo "Make sure you source this file instead of simply running it!"
read -p "Username: " u
export ChatExchangeU=$u
export CEU="h"
stty -echo
read -p "Password: " p
export ChatExchangeP=$p
stty echo
echo
read -p "Client ID: " cID
export SEAPICID=$cID
read -p "Client Secret: " cS
export SEAPICS=$cS
read -p "API Key: " key
export SEAPIKey=$key