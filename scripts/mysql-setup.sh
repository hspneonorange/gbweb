#!/bin/bash
sudo apt-get update
sudo apt-get install python3.6-dev libmysqlclient-dev mysql-server # install MySQL
systemctl start mysql # start MySQL now
systemctl enable mysql # start after boot
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'gbweb'@'localhost' IDENTIFIED BY 'Baby1c@t'; create database gbweb; insert into user(first_name, last_name, username, password_hash, last_seen) values('Bryan', 'Owen', 'bryandowen', 'pbkdf2:sha256:50000$zZJrCiKq$7709f7ce09826fd088bdc218efc923513a6a6b5cbdbda8d84ef59b22a2cd6b5f', '2018-07-08 07:44:33'); insert into user(first_name, last_name, username, password_hash, last_seen) values('Nicole', 'Owen', 'hspneonorange', 'pbkdf2:sha256:50000$V2gbbg35$000cbaf9bf44551232401cd3f85537aef6b65d07651b7b996a8e9b9b0e38bfe8', '2018-07-08 07:20:21')"
