Dockerized Nebula
=================

Install
-------

 - Run `install.sh` to download the most recent version of Nebula server and to run docker images
 - Run `docker-compose up postgres` to create the database schema, when finished, stop the container
 - Run `docker-compose up core` and then, from a different terminal run "setup.sh" to apply the configuration.
   You may tweak the configuration scripts in the `settings` directory first.
 - Run `adduser.sh` to add the first user.
 - Stop the running `core` container and start the whole stack using `docker-compose up`

Uninstall
---------

Just run `uninstall.sh`


TODO
----

 - install should deploy the db schema and apply the configuration without turning containers on and off
 - Resolve the user madness
 - Sane default settings
 - Bundle a stream player
