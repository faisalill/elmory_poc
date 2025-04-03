import subprocess


def get_acl(filepath):
    cmd = ["getfacl", f"{filepath}"]
    subprocess.run(cmd, check=True)


file_path = "./test.txt"

get_acl(file_path)
