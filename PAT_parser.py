import glob
import os

PACKET_NUMBER = 0
TEN_COUNTER = 1


def read_file(file_input):
    # while True:
    #     ts_packets = []
    #     testing_array = []
    #     num = 0
    #     # Ask for file name to user
    #     file_input = input("Enter the filename of .ts: ")
    #     if os.path.exists(file_input + '.ts'):
    #         file_open = open(file_input + '.ts', "rb")
    #     else:
    #         print("ERROR: Invalid filename. Please enter again: ")

    file_open = open(file_input, 'rb')

    while True:
        # if os.path.exists(file_input):
        #     with open(file_input, "rb") as file_object:
        reading_file = file_open.read(188)

        if len(reading_file) < 188:
            break

        decompose_file(reading_file)


def decompose_file(one_packet_bytes):
    # print("========== Packet Information ==========")
    sync_byte = one_packet_bytes[0]                                         # Sync byte (8)
    continuity_counter_list = []
    num = 0
    global PACKET_NUMBER
    global TEN_COUNTER
    # user_pid = enter_pid()

    # Decompose Header
    if sync_byte != SYNC_BYTE:
        print(">> ERROR! First byte is not 0x47")

    transport_error_indicator = (one_packet_bytes[1] >> 7) & 1              # transport_error_indicator (1)
    payload_unit_start_indicator = (one_packet_bytes[1] >> 6) & 1           # payload_unit_start_indicator (1)
    transport_priority = (one_packet_bytes[1] >> 5) & 1                     # transport_priority (1)
    pid_left = one_packet_bytes[1] & 0x1F  # pid (13)
    pid_right = one_packet_bytes[2] & 0xFF
    pid = (pid_left << 8) + pid_right
    transport_scrambling_control = (one_packet_bytes[3] & 0xC0) >> 6        # transport_scrambling_control (2)
    adaptation_field_control = (one_packet_bytes[3] & 0x30) >> 4            # adaptation_field_control (2)
    continuity_counter = one_packet_bytes[3] & 0x0F                         # continuity_counter (4)

    # Check conditions for PAT
    if pid == 0x0000:
        while TEN_COUNTER <= 10:
            print("PAT #", TEN_COUNTER)
            print("PID FOUND", '0x{0:0{1}X}'.format(pid, 4))
            print(" ".join(["{:02x}".format(x) for x in one_packet_bytes]))

            # Header
            print("---------------- Header ----------------")
            print("Header: ", end='')
            for i in range(0, 4):
                print('{0:0{1}X}'.format(one_packet_bytes[i], 2), end=' ')

            print("\n     Packet Number:                  ", PACKET_NUMBER)
            print("     Sync Byte                       ", hex(sync_byte))
            print("     Transport Error Indicator       ", bin(transport_error_indicator))
            print("     Payload Unit Start Indicator    ", bin(payload_unit_start_indicator))
            print("     Transport Priority              ", bin(transport_priority))
            print("     PID                             ", '0x{0:0{1}X}'.format(pid, 4))
            print("     Transport Scrambling Control    ", bin(transport_scrambling_control))
            print("     Adaptation Field Control        ", bin(adaptation_field_control))
            print("     Continuity Counter              ", bin(continuity_counter), "(", hex(continuity_counter), ")")

            calculate_PAT(one_packet_bytes)
            print("\n")
            break
        TEN_COUNTER = TEN_COUNTER + 1
    PACKET_NUMBER = PACKET_NUMBER + 1

    # Checking conditions for PAT
    # if pid_left == 0x0 and pid_right == 0x0 and payload_unit_start_indicator == 0b1:
    #     print(">> CONDITIONS MET FOR PID AND PUSI. PAT = TRUE")
    #     calculate_PAT(one_packet_bytes)

    # if payload_unit_start_indicator == 0b1:
    #     print(">> Second condition met for PAT")

    # if table_id == 0x00:
    #     print(">> Third condition met for PAT")

    # Check if continuity counter increases sequentially
    # if pid == 0x0:
    #     print("pid", hex(pid))
    #     print("Continuity Counter              ", bin(continuity_counter), "(", hex(continuity_counter), ")")

    for b in continuity_counter_list:
        num = 2 * num + int(b)


def enter_pid():
    pid_value = input("Enter the PID value: ")

    return pid_value


def check_start(value):
    if value == chr(0x47):
        print("Found first sync byte")
        print(value)
    else:
        print("Not a valid Transport Stream")
        print(value)


def calculate_PAT(one_packet_bytes):
    print("\n---------- PAT Information ----------")

    table_id = one_packet_bytes[5]                  # table_id (8)
    section_syntax_indicator = (one_packet_bytes[6] >> 7) & 1
    reserved_future_use = (one_packet_bytes[6] >> 6) & 1
    reserved = (one_packet_bytes[6] & 0x30) >> 4  # 다름
    section_length_left = one_packet_bytes[6] & 0x0F  # <simplify if possible> section length (12)
    section_length_right = one_packet_bytes[7] & 0xFF3
    section_length = (section_length_left << 8) + section_length_right
    transport_stream_id = (one_packet_bytes[8] << 8) | one_packet_bytes[9]  # 16 bits
    reserved_two = (one_packet_bytes[10] & 0xC0) >> 6
    version_number = (one_packet_bytes[10] & 0x3E) >> 1
    current_next_indicator = one_packet_bytes[10] & 1
    section_number = one_packet_bytes[11]       # section number (8)
    last_section_number = one_packet_bytes[12]  # last section number (8)

    num_programs_data = int((section_length - 9) / 4)
    for i in range(5, 5 + num_programs_data*4 + 4):   # print till the CRC
        print('{0:0{1}X}'.format(one_packet_bytes[i], 2), end=' ')

    print("\n")
    print("Table ID:                    ", '0x{0:0{1}X}'.format(table_id, 2))
    print("Section Syntax Indicator:    ", bin(section_syntax_indicator))
    print("Reserved Future Use:         ", bin(reserved_future_use))
    print("Reserved:                    ", bin(reserved))
    print("Section Length Test:         ", f'0x{section_length_left:x}{section_length_right:x}')
    # print("section_length             ", hex(section_length))
    print("Transport Stream ID:         ", '0x{0:0{1}X}'.format(table_id, 4))
    print("Reserved #2:                 ", bin(reserved_two))
    print("version number:              ", version_number)      # display in decimal
    print("Current Next Indicator:      ", bin(current_next_indicator))
    print("Section Number:              ", '0x{0:0{1}X}'.format(section_number, 2))
    print("Last Section Number:         ", '0x{0:0{1}X}'.format(last_section_number, 2))
    # print("Program Number:              ", hex(program_number))

    print("Number of programs : ", num_programs_data)
    for i in range(0, num_programs_data):
        program_map_PID_left = one_packet_bytes[15 + 4*i] & 0x1F
        program_map_PID_right = one_packet_bytes[16 + 4*i] & 0xFF

        program_number = (one_packet_bytes[13 + 4*i] << 8) + one_packet_bytes[14 + 4*i]
        print("\tProgram Number: ", '0x{0:0{1}X}'.format(program_number, 4))
        reserved_three = (one_packet_bytes[15 + 4*i] & 0xE0) >> 5
        print("\tReserved #3: ", bin(reserved_three))
        if program_number == 0:
            network_PID = (program_map_PID_left << 8) + program_map_PID_right
            print("\tNetwork PID: ", network_PID)
        else:
            program_map_PID = (program_map_PID_left << 8) + program_map_PID_right
            print("\tprogram map PID: ", program_map_PID)
            print("\tprogram map PID (hex): ", hex(program_map_PID))

    # CRC
    print("CRC: ", end='')
    for i in range(4):
        # Starting position one_packet_bytes[13] + (no. programs * 4 bytes) + four CRC bytes (= i)
        CRC = one_packet_bytes[(13+(4 * num_programs_data)) + i]
        print('{0:0{1}X}'.format(CRC, 2), end=' ')
    print("\n")


def calculate_PMT():

    return


def main():
    read_file(file_input)       # In future, delete file_input to choosing file by asking the user or from file explorer


if __name__ == "__main__":
    PACKET_SIZE = 188
    SYNC_BYTE = 0x47

    # file_input = "C:\\Users\\parkm\\Desktop\\dump_690000_25.ts"
    file_input = "C:\\Users\\parkm\\Desktop\\France 20080505_Ch1.ts"

    main()
