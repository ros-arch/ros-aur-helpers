import subprocess


class Sed:
    def __init__(self, path, arg1):
        self.path = path
        self.arg1 = arg1

    def del_lines(self):
        subprocess.run(["sed", "-i", "!{0}!d".format(self.arg1), self.path])

    def replace_string(self, arg2):
        subprocess.run(["sed", "-i", "s!{0}!{1}!".format(self.arg1, arg2), self.path])

    def replace_string_global(self, arg2):
        subprocess.run(["sed", "-i", '%s!{0}!{1}!g'.format(self.arg1, arg2), self.path])
