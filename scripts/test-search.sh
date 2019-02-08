#!/bin/bash

gb_un=bryandowen
gb_pw=[stbil
authz="Authorization:Bearer `http --auth $gb_un:$gb_pw POST http://localhost:5000/api/tokens | jq -r .token `"

echo http GET http://localhost:5000/api/products?search=dragonball "$authz"
http GET http://localhost:5000/api/products?search=dragonball "$authz"

echo http GET http://localhost:5000/api/products?search=pokemon "$authz"
http GET http://localhost:5000/api/products?search=pokemon "$authz"

echo http GET http://localhost:5000/api/products?search=dragonball%20z "$authz"
http GET http://localhost:5000/api/products?search=dragonball%20z "$authz"

echo http GET http://localhost:5000/api/products?search=sailor "$authz"
http GET http://localhost:5000/api/products?search=sailor "$authz"
