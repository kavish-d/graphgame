class PQ:
    def __init__(self, ip, key_fn=lambda x: x):
        self.get_key = key_fn
        self.heap = []
        self.map = {}
        self.size = 0

        for i in ip:
            self.push(i)

    def not_empty(self):
        return self.size>0 

    def push(self, ip):
        k = self.get_key(ip)
        if k in self.map:
            self.replace(ip)
            return
        self.map[k] = self.size
        self.heap.append(ip)
        self.size += 1

        self.sift_up(self.size - 1)

    def sift_up(self, idx):
        if not idx:
            return
        cur = self.heap[idx]
        k_cur = self.get_key(cur)
        pidx = idx >> 1 if idx & 1 else (idx - 1) >> 1
        par = self.heap[pidx]
        k_par = self.get_key(par)

        if cur < par:
            self.heap[idx], self.heap[pidx] = self.heap[pidx], self.heap[idx]
            self.map[k_par], self.map[k_cur] = idx, pidx
            self.sift_up(pidx)

        return

    def sift_down(self, idx):
        l = idx << 1 | 1
        r = l + 1

        if l >= self.size:
            return
        if r >= self.size:
            r = l

        s = min([[self.heap[idx], idx], [self.heap[l], l], [self.heap[r], r]])[1]

        if s == idx:
            return

        self.map[self.get_key(self.heap[idx])], self.map[self.get_key(self.heap[s])] = s, idx
        self.heap[idx], self.heap[s] = self.heap[s], self.heap[idx]

        self.sift_down(s)

    def pop(self):
        if not self.size:
            return -1
        p = self.heap[0]
        del self.map[self.get_key(p)]
        self.size -= 1
        l = self.heap.pop()

        if self.size:
            self.heap[0] = l
            self.map[self.get_key(l)] = 0
            self.sift_down(0)

        return p

    def replace(self, ip):
        k = self.map[self.get_key(ip)]
        if self.heap[k] > ip:
            self.heap[k] = ip
            self.sift_up(k)
