import json

print("Load a Python dictionary...", end="")
all_authorizations = {
    "admin@example.com": {
        "firstname": "admin",
        "lastname": "BIG",
        "registration_date": "2020-02-01 11:01:02",
        "authorizations": {
            "s3::": {
                "perms": ["read", "write", "delete"],
                "since": "2020-02-01 12:03:01"
            },
            "ec2::": {
                "perms": ["read", "write", "delete"],
                "since": "2020-02-01 12:01:01"
            }
        }
    },
    "ms@example.com": {
        "firstname": "M",
        "lastname": "S",
        "registration_date": "2020-02-01 12:03:01",
        "authorizations": {
            "S3::C8ABCX": {
                "perms": ["read", "write"],
                "since": "2020-02-01 12:06:01"
            },
            "ec2::": {
                "perms": ["read", "write", "delete"],
                "since": "2020-02-01 12:08:01"
            }
        }
    }
}
print(" loaded a ", type(all_authorizations))

print("Convert from Python to JSON...", end="")
JSON_string = json.dumps(all_authorizations)
print(" converted to ", type(JSON_string))

print("Convert from JSON to Python...", end="")
data_dict = json.loads(JSON_string)
print(" converted to ", type(data_dict))

print("Check that the conversions were correct... ", all_authorizations == data_dict)
