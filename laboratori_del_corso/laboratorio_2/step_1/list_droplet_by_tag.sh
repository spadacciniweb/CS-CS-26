# To list droplets in your account by tag
curl -X GET "https://api.digitalocean.com/v2/droplets?tag_name=infobasic" \
	-H "Authorization: Bearer $DIGITALOCEAN_TOKEN"

