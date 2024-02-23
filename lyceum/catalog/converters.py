class IntConverter:
    regex = r"[0-9]|[1-9]+[0-9]*"

    def to_python(self, num):
        return int(num)

    def to_url(self, num):
        return f"{num}"
