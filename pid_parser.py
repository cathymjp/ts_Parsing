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

        if len(reading_file) < 188:
            break

        decompose_file(reading_file)


def decompose_file(one_packet_bytes):
    # print("========== Packet Information ==========")
    sync_byte = one_packet_bytes[0]                                         # Sync byte (8)
    continuity_counter_list = []
    num = 0
    # user_pid = enter_pid()

    if sync_byte != SYNC_BYTE:
        print(">> ERROR! First byte is not 0x47")
        # wrap it with try-error

    # print("---------------- Header ----------------")
    transport_error_indicator = (one_packet_bytes[1] >> 7) & 1              # transport_error_indicator (1)
    payload_unit_start_indicator = (one_packet_bytes[1] >> 6) & 1           # payload_unit_start_indicator (1)
    transport_priority = (one_packet_bytes[1] >> 5) & 1                     # transport_priority (1)
    pid_left = one_packet_bytes[1] & 0x1F                                   # pid (13)
    pid_right = one_packet_bytes[2] & 0xFF
    pid = pid_left << 8 + pid_right
    transport_scrambling_control = (one_packet_bytes[3] & 0xC0) >> 6        # transport_scrambling_control (2)
    adaptation_field_control = (one_packet_bytes[3] & 0x30) >> 4            # adaptation_field_control (2)
    continuity_counter = one_packet_bytes[3] & 0x0F                         # continuity_counter (4)

    # print("Sync Byte                       ", hex(sync_byte))
    # print("Transport Error Indicator       ", bin(transport_error_indicator))
    # print("Transport Priority              ", bin(transport_priority))
    # print("Payload Unit Start Indicator    ", bin(payload_unit_start_indicator))
    # print("Transport Priority              ", transport_priority)
    # print("PID                             ", f'0x{pid_left:x}{pid_right:x}')
    # print("Transport Scrambling Control    ", bin(transport_scrambling_control))
    # print("Adaptation Field Control        ", bin(adaptation_field_control))
    # print("Continuity Counter              ", bin(continuity_counter), "(", hex(continuity_counter), ")")
    # print("\n")

    # if user_pid == (f'0x{pid_left:x}{pid_right:x}'):
    #     print("You have entered", user_pid, ".")

    # Checking conditions for PAT
    if pid_left == 0x0 and pid_right == 0x0 and payload_unit_start_indicator == 0b1:
        print(">> CONDITIONS MET FOR PID AND PUSI. PAT = TRUE")
        calculate_PAT(one_packet_bytes)

    # if pid_left == 0x0 and pid_right == 0x0:
    # if pid == 0x0:
        # print("pid", hex(pid))
        # print("pid_left", pid_left)
        # print("pid_right", pid_right)
        # print("Continuity Counter              ", bin(continuity_counter), "(", hex(continuity_counter), ")")

    for b in continuity_counter_list:
        num = 2 * num + int(b)

    # if payload_unit_start_indicator == 0b1:
    #     print(">> Second condition met for PAT")

    # if table_id == 0x00:
    #     print(">> Third condition met for PAT")

    # Four bytes after 0x47
    # print("---------- Four Bytes ----------")
    # for i in range(0, 5):
        # print("ByteArray", bytearray(one_packet_bytes))
        # print("one_packet_bytes {}".format(i), ": ",  one_packet_bytes[i], ". In binary: ", '{0:08b}'.format(one_packet_bytes[i]),
        #       "(", bin(one_packet_bytes[i]), ")")

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

    table_id = one_packet_bytes[5]                  # table_id (8)

    print("table_id: ", hex(table_id))

    section_syntax_indicator = (one_packet_bytes[6] >> 7) & 1
    reserved_future_use = (one_packet_bytes[6] >> 6) & 1
    reserved = (one_packet_bytes[3] & 0x30) >> 4
    section_length_left = one_packet_bytes[6] & 0x0F  # <simplify if possible> section length (12)
    section_length_right = one_packet_bytes[7] & 0xFF
    section_length = section_length_left << 8 + section_length_right

    print("section_syntax_indicator2", bin(section_syntax_indicator))
    print("reserved_future_use", bin(reserved_future_use))
    print("reserved", bin(reserved))
    print("section length test", (f'0x{section_length_left:x}{section_length_right:x}'))
    # print("section_length", hex(section_length))

    transport_stream_id = one_packet_bytes[8] + one_packet_bytes[9]
    print("transport_stream_id", hex(transport_stream_id))
    print("transprot_stream_id8", hex(one_packet_bytes[8]))
    print("transprot_stream_id9", hex(one_packet_bytes[9]))

    reserved_two = (one_packet_bytes[10] & 0xC0) >> 6
    print("reserved_#2", bin(reserved_two))

    version_number = (one_packet_bytes[10] & 0x3F) >> 4
    print("version number", bin(version_number))

    current_next_indicator = (one_packet_bytes[10] >> 1) & 1
    print("current_next_indicator", bin(current_next_indicator))

    section_number = one_packet_bytes[11] & 0xFF             # section number (8)
    print("section_number", hex(section_number))

    last_section_number = one_packet_bytes[12] & 0xFF          # last section number (8)
    print("last_section_number", hex(last_section_number))

    program_number1 = one_packet_bytes[13]              # program number (16)
    program_number2 = one_packet_bytes[14]
    program_number = program_number1 << 8 + program_number2

    print("program_number", f'0x{program_number1:x}{program_number2:x}')
    print("Program number2", program_number)


def calculate_PMT():

    return


def main():
    open_file(file_input)       # In future, delete file_input to choosing file by asking the user or from file explorer


if __name__ == "__main__":
    PACKET_SIZE = 188
    SYNC_BYTE = 0x47

    file_input = "C:\\Users\\parkm\\Desktop\\dump_690000_25.ts"
    main()
