
def parse(cmd):
    """
    Returns a parsed command with this structure:
        command_name[, arg1, arg2]
    """
    if not cmd: return
    if cmd[0] == "rep":
        return (cmd[0], cmd[2], cmd[4])
    if cmd[0] == "-":
        return (cmd[0], cmd[3], None)
