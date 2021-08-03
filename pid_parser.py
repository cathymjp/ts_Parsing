import glob
import os

PACKET_NUMBER = 0


def start_parse(file_input):
    # while True:
        # ts_packets = []
        # testing_array = []
        # num = 0
        # # Ask for file name to user
        # file_input = input("Enter the filename of .ts: ")
        # if os.path.exists(file_input + '.ts'):
        #     file_open = open(file_input + '.ts', "rb")
        # else:
        #     print("ERROR: Invalid filename. Please enter again: ")

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
    # user_pid = enter_pid()

    if sync_byte != SYNC_BYTE:
        print(">> ERROR! First byte is not 0x47")

    # print("---------------- Header ----------------")
    transport_error_indicator = (one_packet_bytes[1] >> 7) & 1              # transport_error_indicator (1)
    payload_unit_start_indicator = (one_packet_bytes[1] >> 6) & 1           # payload_unit_start_indicator (1)
    transport_priority = (one_packet_bytes[1] >> 5) & 1                     # transport_priority (1)
    pid_left = one_packet_bytes[1] & 0x1F                                   # pid (13)
    pid_right = one_packet_bytes[2] & 0xFF
    pid = (pid_left << 8) + pid_right
    transport_scrambling_control = (one_packet_bytes[3] & 0xC0) >> 6        # transport_scrambling_control (2)
    adaptation_field_control = (one_packet_bytes[3] & 0x30) >> 4            # adaptation_field_control (2)
    continuity_counter = one_packet_bytes[3] & 0x0F                         # continuity_counter (4)

    # Header
    print("Header: ", end='')
    file_output.write("Header: ")
    for i in range(0, 4):
        print('{0:0{1}X}'.format(one_packet_bytes[i], 2), end=' ')
        file_output.write("%s " % '{0:0{1}X}'.format(one_packet_bytes[i], 2))

    print("\n     Packet Number:                  ", PACKET_NUMBER)
    file_output.write("\n\t Packet Number: \t\t\t %d" % PACKET_NUMBER)

    print("     Sync Byte                       ", hex(sync_byte))
    file_output.write("\n\t Sync Byte \t\t\t %s" % hex(sync_byte))

    print("     Transport Error Indicator       ", bin(transport_error_indicator))
    file_output.write("\n\t Transport Error Indicator \t\t %s" % bin(transport_error_indicator))

    print("     Payload Unit Start Indicator    ", bin(payload_unit_start_indicator))
    file_output.write("\n\t Payload Unit Start Indicator \t\t %s" % bin(payload_unit_start_indicator))

    print("     Transport Priority              ", bin(transport_priority))
    file_output.write("\n\t Transport Priority \t\t\t %s" % bin(transport_priority))

    print("     PID                             ", '0x{0:0{1}X}'.format(pid, 4))
    file_output.write("\n\t PID    \t\t\t\t %s" % '0x{0:0{1}X}'.format(pid, 4))

    print("     Transport Scrambling Control    ", bin(transport_scrambling_control))
    file_output.write("\n\t Transport Scrambling Control \t %s" % bin(transport_scrambling_control))

    print("     Adaptation Field Control        ", bin(adaptation_field_control))
    file_output.write("\n\t Adaptation Field Control \t\t %s" % bin(adaptation_field_control))

    print("     Continuity Counter              ", bin(continuity_counter), "(", hex(continuity_counter), ")")
    file_output.write("\n\t Continuity Counter \t\t %s (%s)" % (bin(continuity_counter),  hex(continuity_counter)))

    print("\n")
    file_output.write("\n\n")

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
        # print("pid", hex(pid))
        # print("Continuity Counter              ", bin(continuity_counter), "(", hex(continuity_counter), ")")

    for b in continuity_counter_list:
        num = 2 * num + int(b)

    # <<< PAT INFORMATION >>>
    # if one_packet_bytes[5] == 0x0:
    #     calculate_PAT(one_packet_bytes)


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
    section_syntax_indicator = (one_packet_bytes[6] >> 7) & 1
    reserved_future_use = (one_packet_bytes[6] >> 6) & 1
    reserved = (one_packet_bytes[3] & 0x30) >> 4
    section_length_left = one_packet_bytes[6] & 0x0F  # <simplify if possible> section length (12)
    section_length_right = one_packet_bytes[7] & 0xFF3
    section_length = (section_length_left << 8) + section_length_right
    transport_stream_id = (one_packet_bytes[8] << 8) | one_packet_bytes[9]
    reserved_two = (one_packet_bytes[10] & 0xC0) >> 6

    current_next_indicator = one_packet_bytes[10] & 1
    section_number = one_packet_bytes[11]  # section number (8)
    last_section_number = one_packet_bytes[12]  # last section number (8)
    program_number = (one_packet_bytes[13] << 8) + one_packet_bytes[14]
    version_number = (one_packet_bytes[10] & 0x3E) >> 5

    print("Table ID:                    ", hex(table_id))
    print("Section Syntax Indicator:    ", bin(section_syntax_indicator))
    print("Reserved Future Use:         ", bin(reserved_future_use))
    print("Reserved:                    ", bin(reserved))
    print("Section Length Test:         ", f'0x{section_length_left:x}{section_length_right:x}')
    # print("section_length             ", hex(section_length))
    print("Transport Stream ID:         ", hex(transport_stream_id))
    print("Reserved #2:                 ", bin(reserved_two))
    print("one_packet[10]", bin(one_packet_bytes[10]))
    print("version number", bin(version_number))
    print("Current Next Indicator:      ", bin(current_next_indicator))
    print("Section Number:              ", hex(section_number))
    print("Last Section Number:         ", hex(last_section_number))
    print("Program Number:              ", hex(program_number))


def calculate_PMT():

    return


def main():
    start_parse(file_input)       # In future, delete file_input to choosing file by asking the user or from file explorer

    file_output.close()


if __name__ == "__main__":
    PACKET_SIZE = 188
    SYNC_BYTE = 0x47

    # file_input = "C:\\Users\\parkm\\Desktop\\dump_690000_25.ts"
    file_input = "C:\\Users\\parkm\\Desktop\\France 20080505_Ch1.ts"
    file_output = open("C:\\Users\\parkm\\Desktop\\ts_parser_python.txt", "w")

    main()

