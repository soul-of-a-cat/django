class IntConverter:
    regex = r"[0-9]+"

    def to_python(self, num: int):
        return num

    def to_url(self, num: int):
        return num
