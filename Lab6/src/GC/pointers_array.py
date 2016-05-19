from .header import *

def pointer_array_count(heap, pointer):
  return header_get_size(heap, pointer) / 4


def pointer_array_get(heap, pointer, index):
  number = read_int(heap, pointer + 4 + 4 * index)
  return number


def pointer_array_set(heap, pointer, index, value):
  write_int(heap, pointer + 4 + 4 * index, value)
