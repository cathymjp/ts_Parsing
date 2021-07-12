import glob
import os


# class transport_stream:
#     continuity_counter = packet[3] & 0xf


def open_file(file_input):

    # while True:
    #   ts_packets = []
    # testing_array = []
    #     num = 0
    #     # file_input = input("Enter the filename of .ts: ")
    #     # if os.path.exists(file_input + '.ts'):
    # with open(file_input + '.ts', "rb") as file_object:

    file_open = open(file_input, 'rb')
    while True:
        # if os.path.exists(file_input):
        #     with open(file_input, "rb") as file_object:
        reading_file = file_open.read(188)
        # print("reading_file", reading_file.hex(), end=' ')
        decompose_file(reading_file)


def decompose_file(file_name):
    sync_byte = file_name[0]            # Sync byte (8)
    continuity_counter_list = []
    num = 0

    # print("sync byte", sync_byte)
    if file_name[0] != 0x47:
        print(">> ERROR! First byte is not 0x47")

    if hex(file_name[0]) == SYNC_BYTE:
        print("YES")

    transport_error_indicator = ('{0:08b}'.format(file_name[1]))[0]         # transport_error_indicator (1)
    # print("transport_Error_indicator", transport_error_indicator)

    payload_unit_start_indicator = ('{0:08b}'.format(file_name[1]))[1]         # payload_unit_start_indicator (1)
    # print("payload_unit_start_indicator", payload_unit_start_indicator)

    transport_priority = ('{0:08b}'.format(file_name[1]))[2]         # transport_priority (1)
    # print("transport_priority", transport_priority)

    pid = file_name[1]

    transport_scrambling_control = file_name[3]         # transport_scrambling_control (2)
    # print("transport_scrambling_control", '{0:08b}'.format(transport_scrambling_control)[0],
    #       '{0:08b}'.format(transport_scrambling_control)[1])

    adaptation_field_control = file_name[3]             # adaptation_field_control (2)
    # print("adaptation_field_control", '{0:08b}'.format(adaptation_field_control)[2],
    #       '{0:08b}'.format(transport_scrambling_control)[3])

    continuity_counter = file_name[3]                   # continuity_counter (4)
    for i in range(4, 8):
        continuity_counter_list.append('{0:08b}'.format(continuity_counter)[i])
        # print("continuity_counter", '{0:08b}'.format(continuity_counter)[i])
    for b in continuity_counter_list:
        num = 2 * num + int(b)
    # print("continuity counter: ", num)
    # Four bytes after 0x47
    print("---------- Four Bytes ----------")
    for i in range(0, 5):
        print("file_name {}".format(i), ": ",  file_name[i], ". In binary: ", '{0:08b}'.format(file_name[i]))
        # print(('{0:08b}'.format(file_name[i]))[0])

    # print("file_name[5]", file_name[5])


    # <<< PAT INFORMATION >>>
    # if file_name[5] == 0x0:
    #     print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    #     calculate_PAT(file_name)

    # # if os.path.exists(file_input):
    #     # scale = 16
    #     counter = 0
    #     binary_string = ''
    #     num_of_bits = 8
    #     testing = []

        # with open(file_input, "rb") as file_object:
        #         testing.append(four_byte)
        #         four_hex = file_object.read(1).hex()
        #
        #         print(four_byte, end=' ')
        #         print(four_hex, end=' ')
        #
        #     print("\n")
        #
        #     for byte in testing:
        #         int_value = ord(byte)
        #         print("int_value", int_value)      # 71 == 0x47
        #         binary_string = '{0:08b}'.format(int_value)
        #         print(binary_string, end='\\')
        #
        #     print("\n")
        #     for i in range(188):
        #         first = file_object.read(1).hex()
        #         testing_array.append(first)
        #
        #         print(first, end=' ')
        #
        #     print("\n")
        #
        #     # for i in range(1024):
        #     #     packetHeader = file_object.read(1).hex()
        #     #     moved = packetHeader >> 24
        #     #     print("moved", moved)
        #
        #     print("\ntesting_array", testing_array)
        #
        #     # while True:
        #     testing_two = file_object.read(188)
        #     print("\n")
        #     print("testing_two[0]", testing_two[0])


        # print("ERROR: Invalid filename. Please enter again: ")






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


def calculate_PAT(file_name):
    print("---------- PAT Information ----------")
    payload_unit_start_indicator = ('{0:08b}'.format(file_name[1]))[1]
    section_syntax_indicator = ('{0:08b}'.format(file_name[6]))[0]
    print("section_syntax_indicator", section_syntax_indicator)

    reserved_future_use = ('{0:08b}'.format(file_name[6]))[1]
    print("reserved_future_use", reserved_future_use)

    reserved = ('{0:08b}'.format(file_name[6]))[2], ('{0:08b}'.format(file_name[6]))[3]
    print("reserved", reserved)

    # section length (12)

def calculate_PMT():

    return


def main():
    file_input = "C:\\Users\\parkm\\Desktop\\dump_690000_25.ts"
    open_file(file_input)
    # print("Hex value: ", filename)

    # ts_stream_from_file("C:\\Users\\parkm\\Desktop\\dump_690000_25.ts", 1024)
    # ts_bytes = bytearray(open("C:\\Users\\parkm\\Desktop\\dump_690000_25.ts", 'rb').read(2 * 1024))
    # new_str = ""
    # print("ts+bytes", ts_bytes)
    # with open("C:\\Users\\parkm\\Desktop\\dump_690000_25.ts", 'rb') as file_object:
    #     print("bytearray(file_object.read(1024))", bytearray(file_object.read(1024)))
    #     # hexdata = binascii.hexlify(file_object.read(188))
    #     # print("hexdata", hexdata)
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
    SYNC_BYTE = 0x74

    main()
