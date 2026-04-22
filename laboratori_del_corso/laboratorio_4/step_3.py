import json

def load_authorizations():
    print("Load authorizations...", end="")
    with open("iam.json", encoding="utf-8") as f:
        all_authorizations = json.load(f)
    print(" loaded ")
    return all_authorizations

def check_authorization(all_authorizations, user_name, resource_name, required_permission):
    if user_name in all_authorizations:
        if all_authorizations[ user_name ]["authorizations"] and resource_name in all_authorizations[ user_name ]["authorizations"] and required_permission in all_authorizations[ user_name ]["authorizations"][resource_name]["perms"]:
            print("User got the autorization %s -> %s " % (required_permission, resource_name) )
            return True
        else:
            print("The user '%s' does not have permission for the resource '%s'" % (user_name, resource_name) )
    else:
        print("The user '%s' does not exist" % (user_name) )
    return False

def main():
    all_authorizations = load_authorizations()
    print("Got authorizations ", type(all_authorizations))

    user_name = "an@other.com"
    resource_name = ""
    required_permission = ""
    check_authorization(all_authorizations, user_name, resource_name, required_permission)

    user_name = "ms@example.com"
    resource_name = "S3::"
    required_permission = ""
    check_authorization(all_authorizations, user_name, resource_name, required_permission)

    user_name = "ms@example.com"
    resource_name = "S3::C8ABCX"
    required_permission = "read"
    check_authorization(all_authorizations, user_name, resource_name, required_permission)

    user_name = "ms@example.com"
    resource_name = "S3::C8ABCX"
    required_permission = "delete"
    check_authorization(all_authorizations, user_name, resource_name, required_permission)
    
if __name__ == "__main__":
    main()
