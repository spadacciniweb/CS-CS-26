import json

def load_authorizations():
    print("Load authorizations...", end="")
    with open("iam_6.json", encoding="utf-8") as f:
        data = json.load(f)
    print(" loaded ")
    return data

def match_resource(pattern, resource):
    return resource.startswith(pattern)

def evaluate_policies(authorizations, resource_name, required_permission, source="unknown"):
    """
    Valuta le policy per una risorsa e un'azione richiesta.

    Returns:
        (decision, reason, matched_rule)
        - decision: "allow" | "deny"
        - reason: stringa descrittiva
        - matched_rule: pattern che ha fatto match (None se nessuna regola trovata)
    """
    allowed = False

    for pattern in sorted(authorizations.keys(), key=len, reverse=True):
        if not match_resource(pattern, resource_name):
            continue

        perms = authorizations[pattern].get("perms", [])

        for perm in perms:
            # -------------------------
            # FORMATO SEMPLICE (stringa)
            # -------------------------
            if isinstance(perm, str):
                if perm == required_permission:
                    return (
                        "allow",
                        f"Matched simple allow in {source}",
                        pattern
                    )

            # -------------------------
            # FORMATO OGGETTO (dict)
            # -------------------------
            elif isinstance(perm, dict):
                if perm.get("action") == required_permission:
                    if perm.get("effect") == "deny":
                        return (
                            "deny",
                            f"Explicit deny in {source}",
                            pattern
                        )
                    elif perm.get("effect") == "allow":
                        allowed = True

    if allowed:
        return (
            "allow",
            f"Allowed by rule in {source}",
            None
        )

    # Nessuna regola trovata: deny implicito, matched_rule=None
    return (
        "deny",
        f"No matching rule in {source}",
        None
    )

def check_authorization(data, user_name, resource_name, required_permission):
    user = data.get("users", {}).get(user_name)

    if not user:
        return {
            "decision": "DENY",
            "reason": "User does not exist"
        }

    # -------------------------
    # POLICY UTENTE
    # -------------------------
    if "authorizations" in user:
        decision, reason, rule = evaluate_policies(
            user["authorizations"],
            resource_name,
            required_permission,
            source="user"
        )

        # Blocca SOLO se c'è un deny esplicito (rule valorizzato),
        # non per semplice assenza di regola (rule=None)
        if decision == "deny" and rule is not None:
            return {
                "decision": "DENY",
                "reason": reason,
                "matched_rule": rule,
                "source": "user"
            }

    # -------------------------
    # POLICY DEI RUOLI
    # -------------------------
    final_allow = False

    for role_name in user.get("roles", []):
        role = data.get("roles", {}).get(role_name)

        if not role or "authorizations" not in role:
            continue

        decision, reason, rule = evaluate_policies(
            role["authorizations"],
            resource_name,
            required_permission,
            source=f"role:{role_name}"
        )

        # Deny esplicito da un ruolo blocca tutto
        if decision == "deny" and rule is not None:
            return {
                "decision": "DENY",
                "reason": reason,
                "matched_rule": rule,
                "source": role_name
            }

        elif decision == "allow":
            final_allow = True

    if final_allow:
        return {
            "decision": "ALLOW",
            "reason": "Allowed by role policy",
            "matched_rule": None,
            "source": "role"
        }

    return {
        "decision": "DENY",
        "reason": "No matching permissions",
        "matched_rule": None,
        "source": "none"
    }

def main():
    data = load_authorizations()

    tests = [
        ("ms@example.com", "S3::C8ABCX", "read"),
        ("ms@example.com", "S3::C8ABCX", "delete"),
        ("ms@example.com", "S3::OTHER", "read"),
        ("ms@example.com", "S3::OTHER", "delete"),
    ]

    for user_name, resource_name, action in tests:
        print("\n---")
        print(f"user: '{user_name}' -- resource: '{resource_name}' -- action: '{action}'")
        result = check_authorization(data, user_name, resource_name, action)
        print(result)

if __name__ == "__main__":
    main()
