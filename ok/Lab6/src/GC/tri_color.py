from .header import *
from .pointers_array import *
from .heap import *

class tri_color(object):

  def __init__(self, heap):
    self.heap = heap
    self.black = set()
    self.white = set()
    self.grey = set()


  def collect(self):
    """This function should collect the memory in the heap."""
    self.initialize_white()
    self.black = set()
    self.grey = set()
    self.grey.add(0)
    self.sort()
    self.clean()


  def initialize_white(self):
    self.white = set()
    pointer = header_get_size(self.heap.data, 0) \
                 + HEADER_SIZE
    while pointer < self.heap.size:
      self.white.add(pointer)
      pointer += header_get_size(self.heap.data, pointer) \
                 + HEADER_SIZE


  def sort(self):
    if len(self.grey) == 0:
      return
    else:
      element = self.grey.pop()
      self.mark(element)
      self.black.add(element)
      if header_is_pointers_array(self.heap.data, element):
        length = pointer_array_count(self.heap.data, element)
        for i in range(0, length):
          ptr = pointer_array_get(self.heap.data, element, i)
          if ptr == 0:
            continue
          else:
            if ptr in self.white:
              self.white.remove(ptr)
            self.grey.add(ptr)

      self.sort()


  def mark(self, pointer):
    """Mark the pointer as in use."""
    header_set_used_flag(self.heap.data, pointer, True)


  def clean(self):
    for ptr in self.white:
      header_set_used_flag(self.heap.data, ptr, False)
