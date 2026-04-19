# To list all Droplets in your account
curl -X GET "https://api.digitalocean.com/v2/account/keys" \
	-H "Authorization: Bearer $DIGITALOCEAN_TOKEN"

