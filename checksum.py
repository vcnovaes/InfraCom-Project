# implemenar uma função de checksum segundo o algoritmo apresentaedo na disciplina e no kurose

"""

from RFC 1071
   In outline, the Internet checksum algorithm is very simple:

   (1)  Adjacent octets to be checksummed are paired to form 16-bit
        integers, and the 1's complement sum of these 16-bit integers is
        formed.

   (2)  To generate a checksum, the checksum field itself is cleared,
        the 16-bit 1's complement sum is computed over the octets
        concerned, and the 1's complement of this sum is placed in the
        checksum field.

   (3)  To check a checksum, the 1's complement sum is computed over the
        same set of octets, including the checksum field.  If the result
        is all 1 bits (-0 in 1's complement arithmetic), the check
        succeeds.


        4.  Implementation Examples

   In this section we show examples of Internet checksum implementation
   algorithms that have been found to be efficient on a variety of
   CPU's.  In each case, we show the core of the algorithm, without
   including environmental code (e.g., subroutine linkages) or special-
   case code.

4.1  "C"

   The following "C" code algorithm computes the checksum with an inner
   loop that sums 16-bits at a time in a 32-bit accumulator.

   in 6
       {
           /* Compute Internet Checksum for "count" bytes
            *         beginning at location "addr".
            */
       register long sum = 0;

        while( count > 1 )  {
           /*  This is the inner loop */
               sum += * (unsigned short) addr++;
               count -= 2;
       }

           /*  Add left-over byte, if any */
       if( count > 0 )
               sum += * (unsigned char *) addr;

           /*  Fold 32-bit sum to 16 bits */
       while (sum>>16)
           sum = (sum & 0xffff) + (sum >> 16);

       checksum = ~sum;
   }


"""

def Checksum(count, data, flag = True):
    """
    computes the checksum with an inner loop
    that sums 16-bits at a time in a 32-bit accumulator

    count: number of bytes
    addr: location
    """
    addr = 0 
    # Copute Internet Checksum for "count" bytes, begining at location "addr"
    Sum = 0

    while (count > 1):
        # inner loop
        Sum += data[addr] << 8 + data[addr+1]  # index do byte 
        addr += 2
        count -= 2

    # add left-over byte, if any
    if (count > 0):
        Sum += data[addr]

    # fold 32-bit Sum to 16 bits
    while (Sum>>16):
        Sum = (Sum & 0xffff) + (Sum >> 16)
    if flag== False:
        checksum = ~Sum
    return checksum

print(Checksum(4,b"1535"))
print(Checksum(4,b"1525"))
print(b"1535")