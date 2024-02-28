__all__ = [
    "IntConverter",
]


class IntConverter:
    regex = r"[1-9]\d*"

    def to_python(self, num):
        return int(num)

    def to_url(self, num):
        return f"{num}"
