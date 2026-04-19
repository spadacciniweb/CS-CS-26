curl -X POST -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITALOCEAN_TOKEN'' \
    -d '{"name":"infobasic-base",
        "size":"s-1vcpu-1gb",
        "region":"fra1",
        "image":"ubuntu-22-04-x64",
        "monitoring":true,
        "tags": [
            "infobasic",
            "base"
        ],
        "ssh_keys": [
            "3a:5d:3a:d7:e0:a5:62:db:33:11:8f:e4:e1:d9:d2:78"
        ],
        "vpc_uuid":"fc9420a4-dc84-11e8-8b13-3cfdfea9f160"}' \
    "https://api.digitalocean.com/v2/droplets"
