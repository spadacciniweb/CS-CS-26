import json

print("Load external JSON...", end="")
with open("iam.json", encoding="utf-8") as f:
    all_authorizations = json.load(f)
print(" loaded ", type(all_authorizations))
