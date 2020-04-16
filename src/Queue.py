# @author: Matheus Kunnen Ledesma


class Queue:
    def __init__(self, max_elements):
        self.max_elements = max_elements
        self.n_elements = 0
        self.elements = []
    
    def put(self, element, dequeue_on_full=True):
        if self.n_elements + 1 > self.max_elements:
            if dequeue_on_full:
                self.dequeue()
            else:
                return 1
        self.elements.append(element)
        self.n_elements += 1
        return 0 
           
    def dequeue(self):
        if not self.is_empty():
            self.elements.pop(0)
            self.n_elements -= 1

    def is_empty(self):
        return self.n_elements == 0
