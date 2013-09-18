import config

def lookup_user_id(fuzzy_username):
    if isinstance(fuzzy_username, unicode):
        if fuzzy_username in config.username_to_id:
            return config.username_to_id[fuzzy_username]
        elif fuzzy_username.lower() in config.username_to_id:
            return config.username_to_id[fuzzy_username.lower()]
        else:
            try:
                as_int =  int(fuzzy_username)
                if as_int in config.username_to_id.values():
                    return as_int
            except:
                pass

    elif isinstance(fuzzy_username, int):
        if fuzzy_username in config.username_to_id.values():
            return fuzzy_username

    print type(fuzzy_username)
    raise Exception('No user found matching the input {}'.format(fuzzy_username))


def lookup_user_tags(user_id):
    return config.user_id_to_tags[user_id]
