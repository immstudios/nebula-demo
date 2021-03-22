from defaults import data

# This file is used to override default nebula settings,
# which you can see in `nebula/nebula-setup/defaults/`

data["settings"]["cache_host"] = "memcached"
data["settings"]["hub_sessions_dir"] = "/data/sessions"

# We use watchfolders to create assets, so there is no need
# to have a "New asset" function in Firefly and the web interface

data["settings"]["ui_asset_create"] = False

# Uncomment the following lines to use RabbitMQ as a messaging broker
# instead of the default UDP method.
# This should allow simpler connection from nodes outside this stack.
# Note that RabbitMQ support is experimental and may cause problems.

data["settings"]["messaging"] = "rabbitmq"
data["settings"]["rabbitmq_host"] = "rabbitmq"


############
# STORAGES #
############


# The primary storage is ./data/storage on host.
# You may define other storages (samba, nfs as well)

data["storages"][1] = {
        "protocol" : "local",
        "path" : "/data/storage"
}

# Remote storage example:
#
# data["storages"][1] = {
#     "title"    : "production",
#     "protocol" : "samba",
#     "path"     : "//storage_server_ip_address/share",
#     "login"    : "nebula",
#     "password" : "nebula",
#     "samba_version" : "2.0"
#
# }


############
# SERVICES #
############


services = [
    # type      host             name       settings
    ["mesg",   "worker",         "mesg",    "template/services/mesg.xml"],
    ["watch",  "worker",         "watch",   "template/services/watch.xml"],
    ["broker", "worker",         "broker",  None],
    ["meta",   "worker",         "meta",    None],
    ["conv",   "worker",         "conv",    None],
    ["play",   "playout",        "play",    "template/services/play.xml"],
]

# All services have auto_restart enabled (True)
# and the loop_delay parameter set to 5 seconds
for i, row in enumerate(services):
    data["services"][i+1] = row + [True, 5]


###########
# ACTIONS #
###########


data["actions"] = {
    1 : ["proxy",   "conv", "template/actions/proxy.xml"]
}


############
# CHANNELS #
############


#
# Linear playout channel uses Conti engine with HLS output
# Feel free to modify the quality settings in the `conti_output` section;
# Default values are chosen to be CPU inexpensive in order to run on a laptop.
#

data["channels"] = {
    1 : [0, {
        'title': 'Nebula TV',
        'engine' : 'conti',
        'allow_remote' : True, # Allow playback from the production storage

        'conti_settings' : {
                "width" : 1920,
                "height" : 1080,
                "frame_rate" : 25,
                "pre_filters" : ["movie=/data/logo.png[logo]", "[video][logo]overlay[video]"],
            },

        'conti_outputs' : [{
            "target" : "/data/hls/nebula.m3u8",
            "audio_filters" : ["pan=stereo|c0=c0|c1=c1", "loudnorm=I=-23"],
            "video_filters" : "scale=960x540",
            "params" : {
                "pix_fmt" : "yuv420p",
                "c:v" : "libx264",
                "b:v" : "1200k",
                "g" : 80,
                "x264opts" :  "keyint=80:min-keyint=80:no-scenecut",
                "c:a" : "aac",
                "b:a" : "128k",
                "f" : "hls",
                "hls_time" : 3.2,
                "hls_segment_filename" : "/data/hls/nebula%04d.ts",
                "hls_flags" : "+delete_segments"
            }
        }],

        'controller_host' : "playout",
        'controller_port' : 42101,
        'day_start' : [7, 0],
        'rundown_accepts': "asset['content_type'] == VIDEO",
        'scheduler_accepts': "asset['id_folder'] in [1, 2]",
        'fps': 25,
        'meta_set' : [
            ("start", {}),
            ("title", {}),
            ("subtitle", {}),
            ("description", {}),
            ("promoted", {}),
            ("color", {})
        ]
    }]
}




# We'll keep the configuration simple, so we'll get rid of a few folders
del (data["folders"][2])  # Episodes
del (data["folders"][9])  # Commercials
del (data["folders"][10]) # Teleshopping
del (data["folders"][11]) # Datasets
del (data["folders"][12]) # Incoming
del (data["folders"][13]) # Series

# And views...
del (data["views"][5])  # Commercial
del (data["views"][30]) # Series
del (data["views"][52]) # Incoming

