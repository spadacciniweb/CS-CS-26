import json

def load_authorizations():
    print("Load authorizations...", end="")
    with open("iam.json", encoding="utf-8") as f:
        all_authorizations = json.load(f)
    print(" loaded ")
    return all_authorizations

def match_resource(pattern, resource):
    """
    Prefix-based matching:
    - "S3::" matches "S3::C8ABCX"
    - exact match also works
    """
    return resource.startswith(pattern)

def check_authorization(all_authorizations, user_name, resource_name, required_permission):
    user = all_authorizations.get(user_name)

    if not user:
        print(f"The user '{user_name}' does not exist")
        return False

    authorizations = user.get("authorizations", {})

    # Sort patterns by length (most specific first)
    sorted_patterns = sorted(authorizations.keys(), key=len, reverse=True)

    allowed = False

    for pattern in sorted_patterns:
        if not match_resource(pattern, resource_name):
            continue

        perms = authorizations[pattern].get("perms", [])

        if required_permission in perms:
            print(f"Matched pattern '{pattern}' -> permission '{required_permission}' found")
            allowed = True

    if allowed:
        print(f"ALLOW: {user_name} -> {required_permission} on {resource_name}")
        return True

    print(f"DENY: {user_name} -> {required_permission} on {resource_name}")
    return False

def main():
    all_authorizations = load_authorizations()
    print("Got authorizations ", type(all_authorizations))

    tests = [
        ("an@other.com", "", ""),
        ("ms@example.com", "S3::", ""),
        ("ms@example.com", "S3::C8ABCX", "read"),
        ("ms@example.com", "S3::C8ABCX", "delete"),
        ("ms@example.com", "S3::OTHER", "read"),
    ]

    for user_name, resource_name, action in tests:
        print("\n---")
        check_authorization(all_authorizations, user_name, resource_name, action)

if __name__ == "__main__":
    main()
