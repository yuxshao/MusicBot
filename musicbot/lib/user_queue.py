from collections import deque, OrderedDict


class UserQueue:
    """
        A queue supporting round-robin ordering.
    """

    def __init__(self, get_user):
        """
            :param get_user: A function for getting the user "owning" the task.
        """
        self.user = get_user
        self.data = OrderedDict()

    def __iter__(self):
        for v in self.data.values():
            for s in v:
                yield s

    def __len__(self):
        return sum([len(v) for v in self.data.values()])

    def __getitem__(self, key):
        key = int(key)
        for v in self.data.values():
            if key < len(v):
                return v[key]
            key -= len(v)
        raise IndexError("list index out of range")

    def __delitem__(self, key):
        key = int(key)
        for v in self.data.values():
            if key < len(v):
                del v[key]
                return
            key -= len(v)
        raise IndexError("list index out of range")

    def append(self, entry):
        user = self.user(entry)
        if not user in self.data:
            self.data[user] = deque()
        self.data[user].append(entry)

    def popleft(self):
        i = self[0]
        del self[0]
        return i

    def clear(self):
        self.data.clear()
