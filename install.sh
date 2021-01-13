#!/bin/bash

#
# Settings
#

nebula_branch=immstudios
site_name=nebula

#
# Common utils
#

base_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

function error_exit {
    printf "\n\033[0;31mInstallation failed\033[0m\n"
    cd ${base_dir}
    exit 1
}

function finished {
    printf "\n\033[0;92mInstallation completed\033[0m\n"
    cd ${base_dir}
    exit 0
}

#
# Download nebula
#

nebula_dir=$base_dir/nebula
nebula_repos=(
    "https://github.com/${nebula_branch}/nebula"
    "https://github.com/${nebula_branch}/nebula-setup"
)

function download_repos {
    for i in ${nebula_repos[@]}; do
        cd $nebula_dir
        repo_dir=`basename $i`
        if [ -d $repo_dir ]; then
            cd $repo_dir
            git checkout master || return 1
            git pull || return 1
            cd ..
        else
            git clone $i || return 1
        fi
        cd $repo_dir
        python3 rex.py --rex-update
    done
    return 0
}

download_repos || error_exit

settings_path=$base_dir/nebula/nebula/settings.json
echo "{" > $settings_path
echo "    \"site_name\" : \"$site_name\"," >> $settings_path
echo "    \"db_host\" : \"postgres\"," >> $settings_path
echo "    \"db_user\" : \"nebula\"," >> $settings_path
echo "    \"db_pass\" : \"nebula\"," >> $settings_path
echo "    \"db_name\" : \"nebula\"" >> $settings_path
echo "}" >> $settings_path
cp $settings_path $base_dir/nebula/nebula-setup/settings.json

#
# Database
#

cp \
    $base_dir/nebula/nebula-setup/support/schema.sql \
    $base_dir/support/postgres-init/schema

#
# Default settings
#

docker-compose build \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) \
    core

docker-compose build \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) \
    worker

docker-compose build \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) \
    playout




finished
