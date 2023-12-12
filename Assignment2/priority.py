# import heapq

# class PriorityQueue:
#     def __init__(self):
#         self.elements: tuple[float, float] = []
    
#     def empty(self) -> bool:
#         return not self.elements
    
#     def put(self, item: float, priority: float):
#         heapq.heappush(self.elements, (priority, item))
    
#     def get(self) -> float:
#         if not self.elements:
#             raise Exception("Queue is empty")
#         return heapq.heappop(self.elements)[1]