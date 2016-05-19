def header_get_garbage_flag(heap, pointer):
  mask = 1 << 7
  return heap[pointer + 3] & mask != 0


def header_set_garbage_flag(heap, pointer, value):
  pass

def header_get_used_flag(heap, pointer):
  mask = 1 << 6
  return heap[pointer + 3] & mask != 0

def header_set_used_flag(heap, pointer, value):
  pass

def header_is_pointers_array(heap, pointer):
  pass

def header_mark_as_pointers_array(heap, pointer):
  pass

def header_mark_as_bytes_array(heap, pointer):
  pass

def header_get_size(heap, pointer):
  ba = bytearray()
  for i in range (0, 4):
    ba.append(heap[pointer+i])
  number = int.from_bytes(ba, 'little')
  return number & ~(111 << 29)

def header_set_size(heap, pointer, size):
  pass
