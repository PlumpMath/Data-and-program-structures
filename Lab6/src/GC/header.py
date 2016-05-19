def header_get_garbage_flag(heap, pointer):
  mask = 1 << 7
  return heap[pointer + 3] & mask != 0


def header_set_garbage_flag(heap, pointer, value):
  pass

def header_get_used_flag(heap, pointer):
  pass

def header_set_used_flag(heap, pointer, value):
  pass

def header_is_pointers_array(heap, pointer):
  pass

def header_mark_as_pointers_array(heap, pointer):
  pass

def header_mark_as_bytes_array(heap, pointer):
  pass

def header_get_size(heap, pointer):
  number = bytearray()
  for i in range (0, 4):
    number.append(heap[pointer+i])
  print("Number:", number)
  return int.from_bytes(number, 'little')

def header_set_size(heap, pointer, size):
  pass
