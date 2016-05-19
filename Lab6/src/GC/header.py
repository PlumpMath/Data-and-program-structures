def header_get_garbage_flag(heap, pointer):
  mask = 1 << 7
  return heap[pointer + 3] & mask != 0


def header_set_garbage_flag(heap, pointer, value):
  mask = 1 << 7
  if value:
    heap[pointer + 3] = heap[pointer + 3] | mask
  else:
    heap[pointer + 3] = heap[pointer + 3] & ~mask


def header_get_used_flag(heap, pointer):
  mask = 1 << 6
  return heap[pointer + 3] & mask != 0


def header_set_used_flag(heap, pointer, value):
  mask = 1 << 6
  if value:
    heap[pointer + 3] = heap[pointer + 3] | mask
  else:
    heap[pointer + 3] = heap[pointer + 3] & ~mask


def header_is_pointers_array(heap, pointer):
  mask = 1 << 5
  return heap[pointer + 3] & mask != 0


def header_mark_as_pointers_array(heap, pointer):
  mask = 1 << 5
  heap[pointer + 3] = heap[pointer + 3] | mask


def header_mark_as_bytes_array(heap, pointer):
  mask = ~(1 << 5)
  heap[pointer + 3] = heap[pointer + 3] & mask



def header_get_size(heap, pointer):
  number = get_header(heap, pointer)
  return number & ~(111 << 29)


def header_set_size(heap, pointer, size):
  number = get_header(heap, pointer)
  flags = number & (111 << 29)
  ba = (size | flags).to_bytes(4, 'little')
  for i in range(0, 4):
    heap[pointer + i] = ba[i]


def get_header(heap, pointer):
  ba = bytearray()
  for i in range (0, 4):
    ba.append(heap[pointer+i])
  return int.from_bytes(ba, 'little')
