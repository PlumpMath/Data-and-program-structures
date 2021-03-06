from .header import *
from .pointers_array import *

HEADER_SIZE = 4
INT_SIZE = 4
MIN_FREE_THRESHOLD = HEADER_SIZE + INT_SIZE

class heap(object):

  # size: the size (in bytes) of the heap
  def __init__(self, size):
    self.data = bytearray(size)
    self.free_space = size - HEADER_SIZE
    self.allocated_space = 0
    self.first_free = 0
    self.size = size
    header_set_size(self.data, self.first_free, (size - HEADER_SIZE))


  # return the index to the begining of a block with size (in bytes)
  def allocate(self, size):
    (previous, new) = self.find_free(size, None, self.first_free)
    # Allocate the new space.
    self.beancount_alloc(size)
    leftover_space = header_get_size(self.data, new) - size - HEADER_SIZE
    header_set_size(self.data, new, size)

    # If there is free space left after the area we just allocated.
    if leftover_space > 0:
      next_free = self.make_free(new + size + HEADER_SIZE, leftover_space,
                                 self.next_free_space(new))
    else:
      next_free = self.next_free_space(new)

    # Sort out the free pointer linking chain.
    # If we're in the middle of the chain.
    if previous is not None:
      if next_free is not None:
        self.set_next_free(previous, next_free)
      else:
        pass
    # If we're at the very begining
    else:
      self.first_free = next_free
    header_set_used_flag(self.data, new, True)

    return new


  # unallocate the memory at the given index
  def disallocate(self, pointer):
    size = header_get_size(self.data, pointer)
    self.beancount_free(size)
    self.clear(pointer)
    self.make_free(pointer, size)
    self.insert_into_free_chain(None, self.first_free, pointer)
    self.merge_all_continuous_free_spaces()


  def insert_into_free_chain(self, previous, current, new):
    if current is None:
      return
    next_free = self.next_free_space(current)
    if current == self.first_free and new < current:
      self.first_free = new
      self.set_next_free(new, current)
    elif next_free is not None:
      if next_free > new:
        self.set_next_free(current, new)
        self.set_next_free(new, next_free)
      else:
        self.insert_into_free_chain(current, next_free, new)
    elif previous is not None:
      self.set_next_free(previous, new)
      self.set_next_free(new, current)
    else:
      raise Exception("This shuold never happen.")


  def set_next_free(self, writing_to, next):
    if not header_get_used_flag(self.data, writing_to):
      write_int(self.data, writing_to + HEADER_SIZE, next)
    else:
      raise Exception("Attempt to set next_free pointer on non-free data:", writing_to, ", target:", next)


  def merge_all_continuous_free_spaces(self):
    self.merge_following_free_spaces(self.first_free)


  def merge_following_free_spaces(self, pointer):
    next_free = self.next_free_space(pointer)
    if next_free is None:
      return
    if next_free == pointer + header_get_size(self.data, pointer) + HEADER_SIZE:
      # Merge next_free into pointer.
      own_size = header_get_size(self.data, pointer)
      next_size = header_get_size(self.data, next_free) + HEADER_SIZE
      two_steps_forward = self.next_free_space(next_free)
      self.make_free(pointer, own_size + next_size, two_steps_forward)
      self.clear(next_free)
      self.beancount_freeheader()
      # We might have yet another free space infront of us.
      self.merge_following_free_spaces(pointer)
    else:
      self.merge_following_free_spaces(next_free)


  def next_free_space(self, pointer):
    if not header_get_used_flag(self.data, pointer):
      result = read_int(self.data, pointer + 4)
      return result if result != 0 else None
    else:
      raise Exception("Detected link to non-free space")


  def make_free(self, pointer, size, next_free=None):
    if next_free is not None:
      self.write_next_free(pointer, next_free)
    else:
      self.write_next_free(pointer, 0)
    header_set_used_flag(self.data, pointer, False)
    header_set_size(self.data, pointer, size)
    return pointer


  def write_next_free(self, pointer, next_free):
    write_int(self.data, pointer + 4, next_free)


  def clear(self, pointer):
    """Empties the data space pointed to by the pointer."""
    for i in range(0, header_get_size(self.data, pointer) + HEADER_SIZE):
      self.data[pointer + i] = 0


  def total_free_space(self):
    """Return the current total (allocatable) free space"""
    return self.free_space


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


  def find_free(self, min_size, previous, new):
    if new > self.size:
      raise Exception("Unable to allocate, no large enough spot available.")
    next_free = self.next_free_space(new)
    if header_get_used_flag(self.data, new):
      raise Exception("Free pointer chain broken by used data!")
    elif header_get_size(self.data, new) == min_size or next_free is None \
         or header_get_size(self.data, new) >= min_size + MIN_FREE_THRESHOLD:
      return (previous, new)
    else:
      return self.find_free(min_size, new, next_free)


  def beancount_alloc(self, size):
    self.free_space -= size + HEADER_SIZE
    self.allocated_space += size



  def beancount_free(self, size):
    self.free_space += size
    self.allocated_space -= size


  def beancount_freeheader(self):
    self.free_space += HEADER_SIZE


  def set_free_pointer(self, pointer):
    if not header_get_used_flag(self.data, pointer):
      header_set_size(self.data, pointer, header_get_size(self.data, self.free))
      self.first_free = pointer
    else:
      raise Exception("New free pointer is invalid, space already occupied.")
