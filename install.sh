#!/bin/bash


nebula_branch=immstudios
site_name=nebula
base_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

function stage (){
    printf "\n\033[0;34m${1}\033[0m\n\n"
}

function error_exit {
    printf "\n\033[0;31mInstallation failed: $1\033[0m\n"
    cd ${base_dir}
    exit 1
}

function finished {
    printf "\n\033[0;92mInstallation completed\033[0m\n"
    cd ${base_dir}
    exit 0
}

if ! [ -x "$(command -v git)" ]; then
    error_exit "git is not installed"
fi

if ! [ -x "$(command -v docker-compose)" ]; then
    error_exit "docker-compose is not installed"
fi

if ! [ -x "$(command -v pip3)" ]; then
    error_exit "pip3 is not installed"
fi

#
# Download nebula
#


nebula_dir=$base_dir/nebula
nebula_repos=(
    "https://github.com/${nebula_branch}/nebula"
    "https://github.com/${nebula_branch}/nebula-setup"
)

stage "Downloading Nebula to $nebula_dir"

function download_repos {
    for i in ${nebula_repos[@]}; do
        repo_dir=$nebula_dir/$(basename $i)
        if [ -d $repo_dir ]; then
            echo "PWD: $nebula_dir"
            cd $repo_dir
            git checkout master || return 1
            git pull || return 1
        else
            echo "PWD: $nebula_dir"
            cd $nebula_dir
            git clone $i || return 1
        fi
        cd $repo_dir
        python3 rex.py --rex-update
    done
    return 0
}

download_repos || error_exit "Download failed"

settings_path=$base_dir/nebula/nebula/settings.json
echo "{" > $settings_path
echo "    \"site_name\" : \"$site_name\"," >> $settings_path
echo "    \"db_host\" : \"postgres\"," >> $settings_path
echo "    \"db_user\" : \"nebula\"," >> $settings_path
echo "    \"db_pass\" : \"nebula\"," >> $settings_path
echo "    \"db_name\" : \"nebula\"" >> $settings_path
echo "}" >> $settings_path
cp $settings_path $base_dir/nebula/nebula-setup/settings.json



stage "Pulling the latest nebula-base image"

docker pull nebulabroadcast/nebula-base:latest


#
# Database
#

stage "Starting database server"

docker-compose up -d postgres

# Wait for postgres
while true; do
    docker-compose exec postgres sh -c "PGPASSWORD=nebulapass psql -U postgres -c '\d'" > /dev/null
    if [ $? -eq 0 ]; then
        break
    fi
    echo "Waiting for PostgreSQL"

done

stage "Creating the database and user"

docker-compose exec -T postgres sh -c "PGPASSWORD=nebulapass psql -U postgres" <<-EOSQL
    CREATE USER nebula WITH PASSWORD 'nebula';
    CREATE DATABASE nebula OWNER nebula;
EOSQL

stage "Creating database schema"

docker-compose exec -T postgres sh -c "PGPASSWORD=nebulapass psql -U nebula nebula" < ${base_dir}/nebula/nebula-setup/support/schema.sql

stage "Applying site settings"

docker-compose run -w /opt/nebula-setup --entrypoint ./setup.py core

stage "Installation finished. Now run 'docker-compose up' or 'docker-compose up -d' to bring your stack to life"
finished
