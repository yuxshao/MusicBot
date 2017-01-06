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
        it = [iter(v) for v in self.data.values()]
        remaining = True
        while remaining:
            remaining = False
            for i in it:
                try:
                    yield next(i)
                    remaining = True
                except StopIteration:
                    pass

    def __len__(self):
        return sum([len(v) for v in self.data.values()])

    def __getitem__(self, key):
        it = iter(self)
        try:
            for _ in range(int(key)):
                next(it)
            return next(it)
        except StopIteration:
            raise IndexError("list index out of range")

    def append(self, entry):
        user = self.user(entry)
        if not user in self.data:
            self.data[user] = deque()
        self.data[user].append(entry)

    def popleft(self):
        if not self:
            raise IndexError("queue empty")
        while True:
            k, v = self.data.popitem(last=False)
            self.data[k] = v
            if v:
                i = v.popleft()
                return i

    def clear(self):
        self.data.clear()
