#!/bin/bash

gb_un=bryandowen
gb_pw=[stbil
authz="Authorization:Bearer `http --auth $gb_un:$gb_pw POST http://localhost:5000/api/tokens | jq -r .token `"
http --auth $gb_un:$gb_pw POST http://localhost:5000/api/tokens

# POST
# PUT w/ id
# GET w/ id
# GET
# DELETE w/ id

# Events
# if 'name' not in data or 'city' not in data or 'state_abbr' not in data:
http POST http://localhost:5000/api/events name=test start_date=1970-07-19 end_date=2070-07-19 city=Napa state_abbr=CA "$authz"
http PUT http://localhost:5000/api/events/1 name=test2 start_date=1970-07-20 end_date=2070-07-20 city=Napa2 state_abbr=C2 "$authz"
http GET http://localhost:5000/api/events/1 "$authz"
http GET http://localhost:5000/api/events "$authz"

# Users
# if 'first_name' not in data or 'last_name' not in data or 'username' not in data or 'password' not in data:
http POST http://localhost:5000/api/users first_name=testy last_name=mctesterton username=testes password=hiya "$authz"
http PUT http://localhost:5000/api/users/3 first_name=testy2 last_name=mctesterton2 username=testes2 password=hiya2 "$authz"
http GET http://localhost:5000/api/users/3 "$authz"
http GET http://localhost:5000/api/users "$authz"

# Product Types
# if 'name' not in data:
http POST http://localhost:5000/api/product_types name=typetest "$authz"
http PUT http://localhost:5000/api/product_types/1 name=typetest2 "$authz"
http GET http://localhost:5000/api/product_types/1 "$authz"
http GET http://localhost:5000/api/product_types "$authz"

# Product Series
# if 'name' not in data:
http POST http://localhost:5000/api/product_series name=seriestest "$authz"
http PUT http://localhost:5000/api/product_series/1 name=seriestest2 "$authz"
http GET http://localhost:5000/api/product_series/1 "$authz"
http GET http://localhost:5000/api/product_series "$authz"

# Products
http POST http://localhost:5000/api/product_types name=typetest3 "$authz"
http POST http://localhost:5000/api/product_series name=seriestest3 "$authz"
# if 'product_type_id' not in data or 'product_series_id' not in data or 'name' not in data or 'stock' not in data or 'price' not in data:
http POST http://localhost:5000/api/products product_type_id=1 product_series_id=1 name=producttypetest stock=3 price=2.00 "$authz"
http PUT http://localhost:5000/api/products/1 product_type_id=2 product_series_id=2 name=producttypetest2 stock=4 price=2.02 "$authz"
http GET http://localhost:5000/api/products/1 "$authz"
http GET http://localhost:5000/api/products "$authz"

# Sales
http POST http://localhost:5000/api/events name=test3 start_date=1970-07-21 end_date=2070-07-21 city=Napa3 state_abbr=C3 "$authz"
# if 'event_id' not in data or 'user_id' not in data or 'date' not in data:
http POST http://localhost:5000/api/sales event_id=1 user_id=1 date=2018-07-19 "$authz"
http PUT http://localhost:5000/api/sales/1 event_id=2 user_id=2 date=2018-07-20 "$authz"
http GET http://localhost:5000/api/sales/1 "$authz"
http GET http://localhost:5000/api/sales "$authz"

# Sale Line Items
http POST http://localhost:5000/api/products product_type_id=1 product_series_id=1 name=producttypetest2 stock=4 price=2.04 "$authz"
# if 'product_id' not in data or 'sale_id' not in data or 'sale_price' not in data:
http POST http://localhost:5000/api/sales_line_items product_id=1 sale_id=1 sale_price=1.00 "$authz"
http PUT http://localhost:5000/api/sales_line_items/1 product_id=2 sale_id=2 sale_price=1.02 "$authz"
http GET http://localhost:5000/api/sales_line_items/1 "$authz"
http GET http://localhost:5000/api/sales_line_items "$authz"

# Deletes
http DELETE http://localhost:5000/api/sales_line_items/1 "$authz"
http DELETE http://localhost:5000/api/sales/1 "$authz"
http DELETE http://localhost:5000/api/products/1 "$authz"
http DELETE http://localhost:5000/api/products/2 "$authz"
http DELETE http://localhost:5000/api/product_types/1 "$authz"
http DELETE http://localhost:5000/api/product_types/2 "$authz"
http DELETE http://localhost:5000/api/product_series/1 "$authz"
http DELETE http://localhost:5000/api/product_series/2 "$authz"
http DELETE http://localhost:5000/api/events/1 "$authz"
http DELETE http://localhost:5000/api/events/2 "$authz"
http DELETE http://localhost:5000/api/users/3 "$authz"
