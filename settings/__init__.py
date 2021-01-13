from defaults import data

data["settings"]["cache_host"] = "memcached"
data["settings"]["hub_sessions_dir"] = "/data/sessions"

# We use watchfolders for assets creation, so there is no need
# to have a "New asset" functionality in Firefly and Webadmin
data["settings"]["ui_asset_create"] = False


# The primary storage is ./data/storage on host.
# You may define other storages (samba, nfs as well)
data["storages"][1] = {
        "protocol" : "local",
        "path" : "/data/storage"
}


services = [
    # type      host             name       settings
    ["mesg",   "worker",         "mesg",    "template/services/mesg.xml"],
    ["watch",  "worker",         "watch",   "template/services/watch.xml"],
    ["broker", "worker",         "broker",  None],
    ["meta",   "worker",         "meta",    None],
    ["conv",   "worker",         "conv",    None],
    ["play",   "playout",        "play",    "template/services/play.xml"],
]

for i, row in enumerate(services):
    # All services have auto_restart enabled (True)
    # and the loop_delay parameter set to 5 seconds
    data["services"][i] = row + [True, 5]


data["channels"] = {
    1 : [0, {
        'title': 'Nebula TV',
        'engine' : 'conti',
        'allow_remote' : True,

        'conti_settings' : {},
        'conti_outputs' : [{
            "target" : "/data/output/nebula.m3u8",
            "audio_filters" : "pan=stereo|c0=c0|c1=c1, loudnorm=I=-23",
            "video_filters" : "scale=640x360",
            "params" : {
                "pix_fmt" : "yuv420p",
                "c:v" : "libx264",
                "g" : 80,
                "x264opts" :  "keyint=80:min-keyint=80:no-scenecut",
                "c:a" : "aac",
                "b:a" : "128k",
                "f" : "hls",
                "hls_time" : 3.2,
                "hls_segment_filename" : "/data/output/nebula%04d.ts",
                "hls_flags" : "+delete_segments"
            }
        }],

        'controller_host' : "nebula-playout",
        'controller_port' : 42100,
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




# We'll keep the configuration easy, so we'll get rid of a few folders
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


