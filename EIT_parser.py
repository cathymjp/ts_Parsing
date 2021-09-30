import glob
import os


def open_file(file_input):
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
    sync_byte = one_packet_bytes[0]                                         # Sync byte (8)
    continuity_counter_list = []
    num = 0

    if sync_byte != SYNC_BYTE:
        print(">> ERROR! First byte is not 0x47")

    transport_error_indicator = (one_packet_bytes[1] >> 7) & 1              # transport_error_indicator (1)
    payload_unit_start_indicator = (one_packet_bytes[1] >> 6) & 1           # payload_unit_start_indicator (1)
    transport_priority = (one_packet_bytes[1] >> 5) & 1                     # transport_priority (1)
    pid_left = one_packet_bytes[1] & 0x1F                                   # pid (13)
    pid_right = one_packet_bytes[2] & 0xFF
    pid = (pid_left << 8) + pid_right
    transport_scrambling_control = (one_packet_bytes[3] & 0xC0) >> 6        # transport_scrambling_control (2)
    adaptation_field_control = (one_packet_bytes[3] & 0x30) >> 4            # adaptation_field_control (2)
    continuity_counter = one_packet_bytes[3] & 0x0F                         # continuity_counter (4)
    section_length_left = one_packet_bytes[6] & 0x0F  # <simplify if possible> section length (12)
    section_length_right = one_packet_bytes[7] & 0xFF
    section_length = (section_length_left << 8) + section_length_right
    table_id = one_packet_bytes[5]
    section_syntax_indicator = (one_packet_bytes[6] >> 7) & 1
    reserved_future_use = (one_packet_bytes[6] >> 6) & 1
    reserved = (one_packet_bytes[6] & 0x30) >> 4
    service_id_one = one_packet_bytes[8]
    service_id_two = one_packet_bytes[9]
    section_number = one_packet_bytes[11]
    last_section_number = one_packet_bytes[12]
    transport_stream_one = one_packet_bytes[13]
    transport_stream_two = one_packet_bytes[14]
    original_network_one = one_packet_bytes[15]
    original_network_two = one_packet_bytes[16]

    if pid == 0x0012:
        # Header
        # print("Header: ", end='')
        # file_output.write("Byte \t %s \n" % one_packet_bytes.hex())
        for i in range(0, 4):
            print('{0:0{1}X}'.format(one_packet_bytes[i], 2), end=' ')

        print("bytes: ", one_packet_bytes.hex())

        print("     Sync Byte                       ", hex(sync_byte))
        # file_output.write("\n\t Sync Byte \t\t\t %s" % hex(sync_byte))

        print("     Transport Error Indicator       ", bin(transport_error_indicator))
        # file_output.write("\n\t Transport Error Indicator \t\t %s" % bin(transport_error_indicator))

        print("     Payload Unit Start Indicator    ", bin(payload_unit_start_indicator))
        # file_output.write("\n\t Payload Unit Start Indicator \t\t %s" % bin(payload_unit_start_indicator))

        print("     Transport Priority              ", bin(transport_priority))
        # file_output.write("\n\t Transport Priority \t\t\t %s" % bin(transport_priority))

        print("     PID                             ", '0x{0:0{1}X}'.format(pid, 4))
        # file_output.write("\n\t PID    \t\t\t\t %s" % '0x{0:0{1}X}'.format(pid, 4))

        print("     Transport Scrambling Control    ", bin(transport_scrambling_control))
        # file_output.write("\n\t Transport Scrambling Control \t %s" % bin(transport_scrambling_control))

        print("     Adaptation Field Control        ", bin(adaptation_field_control))
        # file_output.write("\n\t Adaptation Field Control \t\t %s" % bin(adaptation_field_control))

        print("     Continuity Counter              ", bin(continuity_counter), "(", hex(continuity_counter), ")")

        # file_output.write("\n\t Continuity Counter \t\t %s (%s)" % (bin(continuity_counter), hex(continuity_counter)))
        print("Section Length Test:         ", f'0x{section_length_left:x}{section_length_right:x}')

        if table_id == 0x4F:
            if service_id_one == 0x02:
                if service_id_two == 0x66:
                    if transport_stream_one == 0x02:
                        if transport_stream_two == 0x00:
                            if original_network_one == 0x00:
                                if original_network_two == 0x1D:
                                    print("table_id", hex(table_id))
                                    print("Section Syntax Indicator:    ", bin(section_syntax_indicator))
                                    print("Reserved Future Use:         ", bin(reserved_future_use))
                                    print("Reserved:                    ", bin(reserved))
                                    print("Section Length Test:         ", f'0x{section_length_left:x}{section_length_right:x}')
                                    print("service_id: ", hex(service_id_one))
                                    print("service_id: ", hex(service_id_two))
                                    # if section_number == 0x18:
                                    #     file_output.write("YES")
                                    file_output.write("Byte \t %s \n" % one_packet_bytes.hex())
                                    print("section_number: ",  hex(section_number))
                                    print("\n")

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


def EIT_check(one_packet_bytes):
    table_id = one_packet_bytes[5]
    section_syntax_indicator = (one_packet_bytes[6] >> 7) & 1
    reserved_future_use = (one_packet_bytes[6] >> 6) & 1
    reserved = (one_packet_bytes[6] & 0x30) >> 4
    section_length_left = one_packet_bytes[6] & 0x0F  # <simplify if possible> section length (12)
    section_length_right = one_packet_bytes[7] & 0xFF
    section_length = (section_length_left << 8) + section_length_right
    UTC_time = one_packet_bytes[8]
    UTC_time1 = one_packet_bytes[9]
    UTC_time2 = one_packet_bytes[10]
    UTC_time3 = one_packet_bytes[11]
    UTC_time4 = one_packet_bytes[12]

    if 0x60 <= table_id <= 0x6F:
        print("BYTES:", one_packet_bytes.hex())
        print("table_id", hex(table_id))
        print("Section Syntax Indicator:    ", bin(section_syntax_indicator))
        print("Reserved Future Use:         ", bin(reserved_future_use))
        print("Reserved:                    ", bin(reserved))
        print("Section Length Test:         ", f'0x{section_length_left:x}{section_length_right:x}')
        print("UTC time: ", hex(UTC_time))
        print("UTC time1: ", hex(UTC_time1))
        print("UTC time2: ", hex(UTC_time2))
        print("UTC time3: ", hex(UTC_time3))
        print("UTC time4: ", hex(UTC_time4))
        print("\n")


def check_start(value):
    # var cc = packet[3] & 0xf
    # byte = file_object.read(1)
    if value == chr(0x47):
        print("Found first sync byte")
        print(value)
    else:
        print("Not a valid Transport Stream")
        print(value)


def main():
    open_file(file_input)       # In future, delete file_input to choosing file by asking the user or from file explorer

    file_output.close()


if __name__ == "__main__":
    PACKET_SIZE = 188
    SYNC_BYTE = 0x47

    # file_input = "C:\\Users\\parkm\\Desktop\\dump_690000_25.ts"
    file_input = "C:\\Users\\parkm\\Desktop\\France 20080505_Ch1.ts"
    file_output = open("C:\\Users\\parkm\\Desktop\\dump_eit_parsing50.txt", "w")
    main()

