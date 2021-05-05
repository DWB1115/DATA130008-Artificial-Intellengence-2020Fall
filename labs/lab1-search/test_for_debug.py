import sys
import os

# utilize heapq
# record nodes and priority

import heapq


class PriorityQueue:

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        # return True if this item is updated (priority changed or newly inserted), False if unchanged
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    return False
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                return True
        else:
            self.push(item, priority)
            return True


pq = PriorityQueue()
pq.push("Start", 0)
pq.push("A", 4)
pq.push("B", 6)
pq.update("Goal", 8)
print('Update an item which not in queue:')
print(pq.heap)

pq.update("Goal", 2)
print('Update an item with higher priority:')
print(pq.heap)

pq.update("Goal", 8)
print('Update an item with lower priority:')
print(pq.heap)