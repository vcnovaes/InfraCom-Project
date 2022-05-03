from test import assert_eq

"""
See RFC 1071

"""

def calculate_checksum(data):
    """
    computes the checksum with an inner loop
    that sums 16-bits at a time in a 32-bit accumulator
    """
    idx = 0 
    acc = 0
    count = len(data)

    # We add some padding to ensure that we have 8 bit pairs
    if (len(data) % 2) != 0:
        data = data + bytearray([0])

    while (count > 1):
        int16 = ((data[idx] << 8) & 0xFF00) + (data[idx + 1] & 0x00FF)
        acc += int16  
        idx += 2
        count -= 2

    # fold 32-bit acc to 16 bits
    while (acc >> 16) > 0:
        acc = (acc & 0xFFFF) + (acc >> 16)

    acc = ~acc
    acc = acc & 0xFFFF

    return acc

def verify_checksum(data, checksum):
    (a, b) = split_int16(checksum)

    # We want the sum of all 16 bit pairs with the checksum
    # the checksum sums them all and flips the bits, so we just
    # unflip them
    data = data + bytearray([a, b])
    sum = ~calculate_checksum(data)

    return sum ==  (~0)

def append_checksum(data):
    chksum = calculate_checksum(data)
    (chksum_top, chksum_bottom) = split_int16(chksum)

    ndata = data + bytearray([chksum_top, chksum_bottom])

    return ndata

def extract_checksum(data):
    chksum = int.from_bytes(data[-2:], 'big')
    n_data = data[:-2]

    print('cksum {}'.format(chksum))

    return (n_data, chksum)

def split_int16(x):
    top = ((x & 0xFF00) >> 8)
    bottom = x & 0x00FF

    return (top, bottom)

textbook_example_payload = bytearray([0b01100110, 0b01100000, 0b01010101, 0b01010101, 0b10001111, 0b00001100])
textbook_example_checksum = 0b1011010100111101

checksum = calculate_checksum(textbook_example_payload)
assert_eq(bin(checksum), bin(textbook_example_checksum))

checksum_passed = verify_checksum(textbook_example_payload, checksum)
assert_eq(checksum_passed, True)

data = textbook_example_payload
(n_data, n_chksum) = extract_checksum(append_checksum(data))
assert_eq(data, n_data)
assert_eq(checksum, n_chksum)
