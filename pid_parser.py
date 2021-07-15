import glob
import os


def open_file(file_input):
    # while True:
    #   ts_packets = []
    # testing_array = []
    #     num = 0
    #     # file_input = input("Enter the filename of .ts: ")
    #     # if os.path.exists(file_input + '.ts'):
    # file_open = open(file_input + '.ts', "rb")

    file_open = open(file_input, 'rb')
    while True:
        # if os.path.exists(file_input):
        #     with open(file_input, "rb") as file_object:
        reading_file = file_open.read(188)
        # print("reading_file", reading_file.hex(), end=' ')
        decompose_file(reading_file)


def decompose_file(one_packet_bytes):
    sync_byte = one_packet_bytes[0]            # Sync byte (8)
    continuity_counter_list = []
    num = 0
    user_pid = enter_pid()

    # print("sync byte", sync_byte)
    if one_packet_bytes[0] != 0x47:
        print(">> ERROR! First byte is not 0x47")

    if hex(one_packet_bytes[0]) == SYNC_BYTE:
        print("YES")

    transport_error_indicator = ('{0:08b}'.format(one_packet_bytes[1]))[0]         # transport_error_indicator (1)
    # print("transport_Error_indicator", transport_error_indicator)

    # <DONE> payload_unit_start_indicator (1)
    payload_unit_start_indicator = (one_packet_bytes[1] >> 6) & 1
    print("payload_unit_start_indicator: ", bin(payload_unit_start_indicator))

    if payload_unit_start_indicator == 0b1:
        print(">> Second condition met for PAT")

    # <DONE> table_id (8)
    table_id = one_packet_bytes[5]
    print("table_id: ", hex(table_id))

    if table_id == 0x00:
        print(">> Third condition met for PAT")

    transport_priority = ('{0:08b}'.format(one_packet_bytes[1]))[2]         # transport_priority (1)
    # print("transport_priority", transport_priority)



    # <simplify if possible> pid (13)
    pid_left = one_packet_bytes[1] & 0x1F
    pid_right = one_packet_bytes[2] & 0xFF

    # if user_pid == (f'0x{pid_left:x}{pid_right:x}'):
    #     print("You have entered", user_pid, ".")

    # Checking conditions for PAT
    if pid_left == 0x0 and pid_right == 0x0 and payload_unit_start_indicator == 0b1:
        print(">> CONDITIONS MET FOR PID AND PUSI. PAT = YES")
        calculate_PAT(one_packet_bytes)

    transport_scrambling_control = one_packet_bytes[3]         # transport_scrambling_control (2)
    # print("transport_scrambling_control", '{0:08b}'.format(transport_scrambling_control)[0],
    #       '{0:08b}'.format(transport_scrambling_control)[1])

    adaptation_field_control = one_packet_bytes[3]             # adaptation_field_control (2)
    # print("adaptation_field_control", '{0:08b}'.format(adaptation_field_control)[2],
    #       '{0:08b}'.format(transport_scrambling_control)[3])

    continuity_counter = one_packet_bytes[3]                   # continuity_counter (4)
    for i in range(4, 8):
        continuity_counter_list.append('{0:08b}'.format(continuity_counter)[i])
        # print("continuity_counter", '{0:08b}'.format(continuity_counter)[i])

    for b in continuity_counter_list:
        num = 2 * num + int(b)
    # print("continuity counter: ", num)

    # Four bytes after 0x47
    # print("---------- Four Bytes ----------")
    # for i in range(0, 5):
        # print("ByteArray", bytearray(one_packet_bytes))
        # print("one_packet_bytes {}".format(i), ": ",  one_packet_bytes[i], ". In binary: ", '{0:08b}'.format(one_packet_bytes[i]),
        #       "(", bin(one_packet_bytes[i]), ")")

    # print("one_packet_bytes[5]", one_packet_bytes[5])

    # <<< PAT INFORMATION >>>
    # if one_packet_bytes[5] == 0x0:
    #     print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    #     calculate_PAT(one_packet_bytes)

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


def enter_pid():
    pid_value = input("Enter the PID value: ")

    return pid_value


def check_start(value):
    # var cc = packet[3] & 0xf
    # byte = file_object.read(1)
    if value == chr(0x47):
        print("Found first sync byte")
        print(value)
    else:
        print("Not a valid Transport Stream")
        print(value)


def calculate_PAT(one_packet_bytes):
    print("---------- PAT Information ----------")
    # payload_unit_start_indicator = ('{0:08b}'.format(one_packet_bytes[1]))[1]
    # section_syntax_indicator = ('{0:08b}'.format(one_packet_bytes[6]))[0]
    # print("section_syntax_indicator", section_syntax_indicator)
    #
    # reserved_future_use = ('{0:08b}'.format(one_packet_bytes[6]))[1]
    # print("reserved_future_use", reserved_future_use)
    #
    # reserved = ('{0:08b}'.format(one_packet_bytes[6]))[2], ('{0:08b}'.format(one_packet_bytes[6]))[3]
    # print("reserved", reserved)

    # section length (12)

    # section number (8)
    section_number = one_packet_bytes[11]
    print("Section number: ", hex(section_number))

    # last section number (8)
    last_section_number = one_packet_bytes[12]
    print("Last section number: ", hex(last_section_number))

    # program number (16)
    program_number1 = one_packet_bytes[13]
    program_number2 = one_packet_bytes[14]
    # print("program_number1", program_number1, ", ", hex(program_number1))
    # print("program_number2", program_number2, ", ", hex(program_number2))
    print("Program number: ", f'0x{program_number1:x}{program_number2:x}')


def calculate_PMT():

    return


def main():
    open_file(file_input)       # In future, delete file_input to choosing file by asking the user or from file explorer


if __name__ == "__main__":
    PACKET_SIZE = 188
    SYNC_BYTE = 0x74

    file_input = "C:\\Users\\parkm\\Desktop\\dump_690000_25.ts"
    main()
