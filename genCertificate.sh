#!/bin/bash

openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
