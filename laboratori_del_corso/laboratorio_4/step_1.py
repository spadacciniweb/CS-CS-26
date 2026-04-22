import json

print("Load external JSON...", end="")
with open("iam.json", encoding="utf-8") as f:
    all_authorizations = json.load(f)
print(" loaded ", type(all_authorizations))


#print("Convert from Python to JSON...", end="")
#JSON_string = json.dumps(data)
#print(" converted to ", type(JSON_string))
#
#print("Convert from JSON to Python...", end="")
#data_dict = json.loads(JSON_string)
#print(" converted to ", type(data_dict))
##print(data == data_dict)
#
#print("Check that the conversions were correct... ", data == data_dict)
#
#user = "ms@example.com"
#check_permission = "S3::C8ABCX"
#check_authorization( data_dict[user]["authorizations"], check_permission )
#
#if __name__ == "__main__":
#    main()
#
