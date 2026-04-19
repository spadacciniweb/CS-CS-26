# To create a new Droplet
curl -X POST -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer '$DIGITALOCEAN_TOKEN'' \
    -d '{"name":"infobasic-test",
        "size":"s-1vcpu-1gb",
        "region":"lon1",
        "image":"ubuntu-22-04-x64",
        "monitoring":true,
        "vpc_uuid":"bebe5ba8-dc82-11e8-83ec-3cfdfea9f3f0"}' \
    "https://api.digitalocean.com/v2/droplets"
