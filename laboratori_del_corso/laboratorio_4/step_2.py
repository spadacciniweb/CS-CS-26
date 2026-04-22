import json

def load_authorizations():
    print("Load external JSON...", end="")
    with open("iam.json", encoding="utf-8") as f:
        all_authorizations = json.load(f)
    print(" loaded ", type(all_authorizations))
    return all_authorizations

def main():
    all_authorizations = load_authorizations()
    print("Got authorizations ", type(all_authorizations))
    
if __name__ == "__main__":
    main()
