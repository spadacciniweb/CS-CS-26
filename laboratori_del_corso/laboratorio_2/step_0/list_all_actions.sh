# To list all of the actions that have been executed on the current accoun
curl -X GET "https://api.digitalocean.com/v2/actions" \
	-H "Authorization: Bearer $DIGITALOCEAN_TOKEN"
