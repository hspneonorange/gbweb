#!/bin/bash
rm -rf ./migrations
echo "enter password: Baby1c@t"
mysql -u root -p -e "drop database gbweb; create database gbweb;"
flask db init
flask db migrate -m "Initial deploy (after nuke)"
flask db upgrade
echo "enter password: Baby1c@t"
mysql -u root -p -e "use gbweb; insert into user(first_name, last_name, username, password_hash, last_seen) values('Bryan', 'Owen', 'bryandowen', 'pbkdf2:sha256:50000\$zZJrCiKq\$7709f7ce09826fd088bdc218efc923513a6a6b5cbdbda8d84ef59b22a2cd6b5f', '2018-07-08 07:44:33'); insert into user(first_name, last_name, username, password_hash, last_seen) values('Nicole', 'Owen', 'hspneonorange', 'pbkdf2:sha256:50000\$V2gbbg35\$000cbaf9bf44551232401cd3f85537aef6b65d07651b7b996a8e9b9b0e38bfe8', '2018-07-08 07:20:21')"
