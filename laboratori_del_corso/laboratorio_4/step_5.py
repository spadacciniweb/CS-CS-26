import json

def load_authorizations():
    print("Load authorizations...", end="")
    with open("iam_5.json", encoding="utf-8") as f:
        all_authorizations = json.load(f)
    print(" loaded ")
    return all_authorizations

def match_resource(pattern, resource):
    """Prefix-based matching"""
    return resource.startswith(pattern)

def check_authorization(all_authorizations, user_name, resource_name, required_permission):
    user = all_authorizations.get(user_name)

    if not user:
        print(f"The user '{user_name}' does not exist")
        return False

    authorizations = user.get("authorizations", {})
    allowed = False

    # Most specific first
    for pattern in sorted(authorizations.keys(), key=len, reverse=True):
        if not match_resource(pattern, resource_name):
            continue

        perms = authorizations[pattern].get("perms", [])

        for perm in perms:
            # old format: "read"
            if isinstance(perm, str):
                if perm == required_permission:
                    print(f"Matched '{pattern}' -> ALLOW (simple)")
                    allowed = True

            # new format: {"action": "...", "effect": "..."}
            elif isinstance(perm, dict):
                if perm.get("action") == required_permission:
                    if perm.get("effect") == "deny":
                        print(f"DENY: matched '{pattern}' (explicit deny)")
                        return False
                    elif perm.get("effect") == "allow":
                        print(f"Matched '{pattern}' -> ALLOW (explicit)")
                        allowed = True

    if allowed:
        print(f"FINAL: ALLOW {user_name} -> {required_permission} on {resource_name}")
        return True

    print(f"FINAL: DENY {user_name} -> {required_permission} on {resource_name}")
    return False

def main():
    all_authorizations = load_authorizations()

    tests = [
        ("ms@example.com", "S3::C8ABCX", "read"),
        ("ms@example.com", "S3::C8ABCX", "delete"),
        ("ms@example.com", "S3::OTHER", "read"),
        ("ms@example.com", "S3::OTHER", "delete"),
    ]

    for user_name, resource_name, action in tests:
        print("\n---")
        check_authorization(all_authorizations, user_name, resource_name, action)

if __name__ == "__main__":
    main()
