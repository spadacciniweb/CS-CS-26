# To list droplets in your account by tag
curl -X GET "https://api.digitalocean.com/v2/droplets?tag_name=infobasic&tag_name=base" \
	-H "Authorization: Bearer $DIGITALOCEAN_TOKEN"

