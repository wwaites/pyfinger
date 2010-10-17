import pwd, os, sys

def finger():
    req = sys.argv[-1].rsplit(".")

    username = req[0]
    if len(req) > 1:
        fname = req[1].lower()
    else:
        fname = "plan"

    if fname not in ("plan", "project", "foaf"):
        return

    n = pwd.getpwnam(username)

    if fname in ("plan", "project"):
        sys.stdout.write("Login: %s\t\t\t\tName: %s\n" % (username, n.pw_gecos))
        sys.stdout.write("%s: " % (fname[0].upper() + fname[1:],))

    fpath = os.path.join(n.pw_dir, ".%s" % fname)
    try:
        os.stat(fpath)
        fp = open(fpath)
        sys.stdout.write(fp.read())
        fp.close()
    except OSError:
        pass
