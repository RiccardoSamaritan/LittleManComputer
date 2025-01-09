# RICCARDO SAMARITAN SM3201396

from lmc_exceptions import *

class LMC_Queue:
  def __init__(self):
    self.items = list()

  def enqueue(self, item):
    self.items.append(item)

  def dequeue(self):
    if self.empty():
      raise EmptyInputQueueException("La coda di input è vuota")
    return self.items.pop(0)
  
  def empty(self):
    return self.items == []


