def rmreplica(string: str):
    """Input your lists, and get them back without duplicates"""
    return list(dict.fromkeys(string))
