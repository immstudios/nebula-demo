Dockerized Nebula
=================

This project is experimental and is intended for development and trials. Never use it in production.


Requirements
------------

 - Docker, docker-compose

Install
-------
 - Edit configuraton scripts in the `settings` directory first.
 - Run `./install.sh` to download the most recent version of Nebula server and to run docker images
 - Run `./adduser.sh` to add the first user.
 - Everytime you do a change to the configuration scripts, run `./setup.py` to apply the new configuration and restart the affected services
   (or just run `docker-compose restart core` or `docker-compose restart worker` etc.)

Usage
-----

 - Connect via [Firefly](https://github.com/nebulabroadcast/firefly) application or the web interface to `http://localhost:8080`
 - View the stack logs in real time using `./logs.sh` or connect to `http://localhost:8080/grafana` to view just Nebula logs along with system metrics.


Uninstall
---------

Just run `uninstall.sh`. Warning: The database will be lost.


TODO
----

 - Sane default settings
 - Bundle a stream player


The main issue at the moment is Nebula should run as root. And it uses the `data` directory on host as a storage by default.
All files created by Nebula here are therefore writable only by root. This is quite inconvenient. In the perfect world, you
should use a samba share as a storage
