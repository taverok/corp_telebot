def get_subcommand(message: str, default: str = None):
    arr = message.split()
    return arr[1] if len(arr)>1 else default
