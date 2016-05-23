from .header import *
from .pointers_array import *

class heap(object):
  # size: the size (in bytes) of the heap
  def __init__(self, size):
    self.data = bytearray(size)
    self.allocated_space = 0 #No headers shall be counted.
    self.free = 0
    self.set_total_free_size(size-4,False)
    
  # return the index to the begining of a block with size (in bytes)
  def allocate(self, size):  
    pointer = self.find_free((size+4), self.free)
    #print("Allocating pointer:",pointer)
    if pointer is not None:
      self.allocated_space += size
      self.set_free_pointer(self.free +(size+4))
      self.set_total_free_size((size+4),True)
      header_set_size(self.data, pointer, size)
      header_set_used_flag(self.data, pointer, True)
      return pointer
    else:
      raise Exception


  # unallocate the memory at the given index
  def disallocate(self, pointer):
    #TODO testen går åt skogen då denna inte är fixad.
    self.allocated_space -= header_get_size(self.data, pointer)
    pass

  # Return the current total (allocatable) free space
  def total_free_space(self):
    return header_get_size(self.data, self.free)

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
    #print("Find free",header_get_size(self.data, pointer))
    if not header_get_used_flag(self.data, pointer) and \
       header_get_size(self.data, pointer) >= min_size:
      #print("free:",pointer)
      return pointer
    else:
      if not header_get_used_flag(self.data, pointer): 
        #print("header correct but get size is not matched.",pointer)
        return pointer
      #print ("new pointer:", (pointer + header_get_size(self.data, pointer)))
      return self.find_free(min_size, (pointer + header_get_size(self.data, pointer)))

  #increase or decrease the total free size, default is to allocate size.
  def set_total_free_size(self,size, decrease=True):
    if decrease:
      header_set_size(self.data, self.free, header_get_size(self.data, self.free) - size)
    else:
      header_set_size(self.data, self.free, header_get_size(self.data, self.free) + size)

  def set_free_pointer(self, pointer):
    
    if not header_get_used_flag(self.data,pointer):
      header_set_size(self.data,pointer, header_get_size(self.data, self.free))
      self.free = pointer
    else:
      print("New free pointer is invalid, space already occupied.") #raise?



