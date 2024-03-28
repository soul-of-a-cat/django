__all__ = []


class IntConverter:
    regex = r"[1-9]\d*"

    def to_python(self, pk):
        return int(pk)

    def to_url(self, pk):
        return f"{pk}"
