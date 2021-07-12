# class TsParser:
#     PACKET_SIZE = 188
#
#     def __init__(self, ts_filename):
#         self.ts_filename = ts_filename
#         self.handle = open(self.ts_filename, 'rb')
#
#     # def __del__(self):
#     # 	if self.handle:
#     # 		self.handle.close()
#
#     def read_one_packet(self):
#         packet = self.handle.read(TsParser.PACKET_SIZE)
#
#         if len(packet) < TsParser.PACKET_SIZE:
#             raise EOFError
#
#         return packet


if __name__ == '__main__':
    PACKET_SIZE = 188
    HEADER_SIZE = 4


    # def printHeader(packet):
    #     for i in range(HEADER_SIZE):
    #         print(format(packet[i], '#04x'), end=' ')
    #
    #     print('')


    # def getBits(oneByte, bitPos, numOfBit):
    #     convToBin = bin(oneByte)[2:].zfill(8)
    #     bits = convToBin[bitPos:bitPos + numOfBit]
    #     return int(bits, 2)


    def parseHeader(packet):
        sync_byte = packet[0]
        tei = (packet[1] & 0x80) >> 7 == 1
        pusi = (packet[1] & 0x40) >> 6 == 1
        tp_priority = (packet[1] & 0x20) >> 5
        pid = ((packet[1] & 0x1f) << 8) | packet[2]
        tsc = (packet[3] & 0xC0) >> 6
        afc = (packet[3] & 0x30) >> 4
        continuity_counter = packet[3] & 0x0f

        if pid == 0:
            print('sync_byte : ', format(sync_byte, '#04x'))
            print('tei : ', tei)
            print('pusi : ', pusi)
            print('tp_priority : ', tp_priority)
            print('pid : ', format(pid, '#04x'))
            print('tsc : ', tsc)
            print('afc : ', bin(afc))
            print('continuity_counter : ', continuity_counter)
            print('')


    try:
        f = open('C:\\Users\\parkm\\Desktop\\dump_690000_25.ts', 'rb')

        while True:
            readOnePacket = f.read(PACKET_SIZE)

            if len(readOnePacket) != PACKET_SIZE:
                raise IndexError

            parseHeader(readOnePacket)

        f.close()
    except IOError:
        print("File isn't exist!")
    except IndexError:
        print("End of file")