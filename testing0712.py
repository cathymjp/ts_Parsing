import glob
import os
from bitstring import BitArray

PACKET_SIZE = 188
SYNC_BYTE = 0x74

# class transport_stream:
#     continuity_counter = packet[3] & 0xf
#
# def read_file(path):
#     """Read from a ts file at path"""
#     def wrapper(n):
#         return f_read(n)
#     f = open(path, "rb")
#     f_read = f.read
#     return wrapper


def open_file():
    # while True:
    #   ts_packets = []
    testing_array = []
    #     num = 0
    #     # file_input = input("Enter the filename of .ts: ")
    file_input = "C:\\Users\\parkm\\Desktop\\dump_690000_25.ts"
    #     # if os.path.exists(file_input + '.ts'):
    if os.path.exists(file_input):
        scale = 16
        num_of_bits = 8
        # with open(file_input + '.ts', "rb") as file_object:
        with open(file_input, "rb") as file_object:
            for i in range(188):
                first = file_object.read(1).hex()
                testing_array.append(first)
                print(first, end=' ')
                # f'{first:0>42b}'

            print("\ntesting_array", testing_array)






            hexdata = file_object.read(188).hex()
            testing_array.append(hexdata)

            print("testing_array", testing_array)
            print("hexdata!!!!!!!", hexdata)
            # print("hex[0]", ord(hexdata))
            current_byte = file_object.read(188)
            what = file_object.read(188)
            print("what", what)
            print("Current byte", current_byte)
            byte = hex(ord(file_object.read(1)))
            print("file_object", current_byte << 8)
            # while True:
            #     byte = hex(ord(file_object.read(1)))
            #     # print("bytttttt", byte)
            # print("BYTE: ", byte)
            # print("chr(0x47)", chr(0x47))
            if byte == '0x47':
                print("Found first sync byte")
                pid = byte.bits.read(13).uint
                print(byte)
            else:
                print("Not a valid Transport Stream")
                print(byte)

            print("askdl", file_object.read(0).hex())
                # for i in file_object:
                #     print(file_object.read(i).hex())

                # WHWHWH = bytearray(file_object.read(1024))
                # ts_bytes = bytearray(file_object.read(2 * 1024))
                # # index_of_1st_packet = ts_bytes.find(chr(0x47))
                # huh = ''.join('{:02x}'.format(x) for x in ts_bytes)
                # print(''.join('{:02x}'.format(x) for x in ts_bytes))
                # print("ts_bytes", ts_bytes)
                # # index_of_1st_packet = ts_bytes.find(chr(0x47))
                # print("WHWHWH", WHWHWH.hex())
                #
                # # for i in range(len(WHWHWH) / 188):
                # #     ts_packets.append(WHWHWH[i * 188:(i + 1) * 188])
                # print("W!!!!!!!", ts_packets)
                # hexdata = file_object.read(188).hex()
                # print("hexdata!!!!!!!", hexdata)
                # # index_of_1st_packet = hexdata.find((0x47))
                # hexdata = hexdata.replace('47', '\n 47')
                # # for i in range(0, len(hexdata), 2):
                # #     # print("i", hexdata[i:i+2])
                # #     if hexdata[i:i+2] == '47':
                # #         print('\n')
                # #     else:
                # #         print((hexdata[i: i+2]))
                # print(' '.join(hexdata[i: i+2] for i in range(0, len(hexdata), 2)))
                #
                # # if 47, return a new line
                # return hexdata

        print("ERROR: Invalid filename. Please enter again: ")


def enter_pid(file):
    pid_value = input("Enter the PID value: ")


def check_start(value):
    # var cc = packet[3] & 0xf
    # byte = file_object.read(1)
    if value == chr(0x47):
        print("Found first sync byte")
        print(value)
    else:
        print("Not a valid Transport Stream")
        print(value)


def check_PAT():

    return


def check_PMT():

    return


def main():
    filename = open_file()
    print("Hex value: ", filename)

    # ts_stream_from_file("C:\\Users\\parkm\\Desktop\\dump_690000_25.ts", 1024)
    # ts_bytes = bytearray(open("C:\\Users\\parkm\\Desktop\\dump_690000_25.ts", 'rb').read(2 * 1024))
    # new_str = ""
    # print("ts+bytes", ts_bytes)
    # with open("C:\\Users\\parkm\\Desktop\\dump_690000_25.ts", 'rb') as file_object:
    #     print("bytearray(file_object.read(1024))", bytearray(file_object.read(1024)))
    #     # hexdata = binascii.hexlify(file_object.read(188))
    #     # print("hexdata", hexdata)
    #     print("=======", filename)
    #     hexdata = file_object.read(188).hex()  # Read 188 bytes in hex
    #     print("hexdata", hexdata)
    #
    #     "0x{:02x}".format(13)
    #
    #     print("new_str", new_str)
    #     byte = hex(ord(file_object.read(1)))
    #     # byte2 = ord(file_object.read(1024))
    #     print("file_object.read(1) byte", byte)
    #     print("\n188", byte)
    #     data = file_object.read(188)
    #     print(data)


def ts_stream_from_file(filename, length=1024):
    with open(filename, 'rb') as f:
        print(bytearray(f.read(length)))
        return bytearray(f.read(length))


if __name__ == "__main__":
    PACKET_SIZE = 188
    main()