from .header import *
from .pointers_array import *

class heap(object):
  # size: the size (in bytes) of the heap
  def __init__(self, size):
    self.data = bytearray(size)
    self.allocated_space = 0
    self.free = 4
    header_set_size(self.data, 0, size - 4)

  # return the index to the begining of a block with size (in bytes)
  def allocate(self, size):
    size += 4
    pointer = self.find_free(size, self.free)
    print(pointer)
    if pointer is not None:
      self.allocated_space += size
      self.free += size
      header_set_size(self.data, pointer, size)
      header_set_used_flag(self.data, pointer, True)
    else:
      raise Exception


  # unallocate the memory at the given index
  def disallocate(self, pointer):
    self.allocated_space -= header_get_size(self.data, pointer)
    pass

  # Return the current total (allocatable) free space
  def total_free_space(self):
    return header_get_size(self.data, 0)

  # Return the current total allocated memory
  def total_allocated_space(self):
    return self.allocated_space

  def allocate_array(self, count):
    pointer = self.allocate(count * 4)
    header_mark_as_pointers_array(self.data, pointer)
    return pointer

  def allocate_bytes(self, count):
    pointer = self.allocate(count)
    header_mark_as_bytes_array(self.data, pointer)
    return pointer

  def find_free(self, min_size, pointer):
    print(header_get_size(self.data, pointer))
    if not header_get_used_flag(self.data, pointer) and \
       header_get_size(self.data, pointer) >= min_size:
      return pointer
    else:
      return self.find_free(min_size, pointer_array_get(self.data, pointer, 0))
