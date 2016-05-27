from .header import *
from .pointers_array import *
from .heap import *

class mark_sweep(object):
  def __init__(self, heap):
    self.heap = heap


  # This function should collect the memory in the heap
  def collect(self):
    self.unmark_all()
    self.mark_reachable(0)


  def unmark_all(self):
    """Linearily unmark all objects in heap."""
    pointer = 0
    while pointer < self.heap.size:
      self.unmark(pointer)
      pointer += header_get_size(self.heap.data, pointer) \
                 + HEADER_SIZE


  def unmark(self, pointer):
    header_set_used_flag(self.heap.data, pointer, False)


  def mark(self, pointer):
    """Mark the pointer as in use."""
    header_set_used_flag(self.heap.data, pointer, True)


  def mark_reachable(self, pointer):
    """Tree traversal marking all reachable parts of the heap."""
    self.mark(pointer)
    if header_is_pointers_array(self.heap.data, pointer):
      length = pointer_array_count(self.heap.data, pointer)
      for i in range(0, length):
        ptr = pointer_array_get(self.heap.data, pointer, i)
        if ptr == 0:
          continue
        else:
          self.mark_reachable(ptr)
