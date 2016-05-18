def header_get_garbage_flag(heap, pointer):
  mask = 0b01000000
  return heap[pointer] & mask == 0


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
  mask_size = 0b00001111
  print("Get size:", bin(mask_size))
  number = bytearray()
  number.append(heap[pointer] & mask_size)
  print("Heap:", heap[pointer])
  print("Masked heap:", heap[pointer] & mask_size)
  for i in range (1, 4):
    number.append(heap[pointer+i])
  print(number)
  return int.from_bytes(number, 'big')

def header_set_size(heap, pointer, size):
  pass
