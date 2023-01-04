import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;

public class pid_parser{
    final static int PACKET_SIZE = 188;
    final static int SYNC_BYTE = 0x47;
    public static void main(String[] args) throws IOException{
        String fileName = "C:/Users/parkm/Desktop/France 20080505_Ch1.ts";
        // String fileName = "C:/Users/parkm/Desktop/dump_690000_25.ts";
        File TSFile = new File(fileName);
        DataInputStream dataInputStream = new DataInputStream(new FileInputStream(TSFile));
        TSPacketReader(dataInputStream);
    }

    public static void TSPacketReader(DataInputStream dataInputStream) throws IOException{
        byte[] onePacket = new byte[PACKET_SIZE];
        int transportErrorIndicator = 0;
        int payloadUnitStartIndicator = 0;
        int transportPriority = 0;
        int pid, pidLeft, pidRight = 0;
        int transportScramblingControl = 0;
        int adaptationFieldControl = 0;
        int continuityCounter = 0;
        int packetNumber = 0;
        int syncByte = 0;

        // Write to file
        File writeFile = new File("C:/Users/parkm/Desktop/ts_parser_java.txt");
        PrintWriter writer = new PrintWriter(writeFile);

        while(dataInputStream.read(onePacket) != -1){
            if(onePacket[0] == SYNC_BYTE){
                // System.out.print(">> 47 found ");
                // for(int i = 0; i < PACKET_SIZE; i ++){
                //     System.out.print(String.format("%02x ", onePacket[i]));     
                // }

                // Header (4 Bytes)
                System.out.print("Header: ");
                writer.print("Header: ");
                for(int i = 0; i < 4; i++){
                    System.out.print(String.format("%02X ", onePacket[i]));
                    writer.print(String.format("%02X ", onePacket[i]));
                }

                syncByte = onePacket[0];    
                transportErrorIndicator = (onePacket[1] >> 7) & 1;               // transport_error_indicator (1)
                payloadUnitStartIndicator = (onePacket[1] >> 6) & 1;             // payload_unit_start_indicator (1)
                transportPriority = (onePacket[1] >> 5) & 1;                     // transport_priority (1)
                pidLeft = onePacket[1] & 0x1F;                                   // pid (13)
                pidRight = onePacket[2] & 0xFF;
                pid = (pidLeft << 8) + pidRight;
                transportScramblingControl = (onePacket[3] & 0xC0) >> 6;         // transport_scrambling_control (2)
                adaptationFieldControl = (onePacket[3] & 0x30) >> 4;             // adaptation_field_control (2)
                continuityCounter = onePacket[3] & 0x0F;                         // continuity_counter (4)
                
                System.out.println();
                System.out.println("    Packet Number:                  " + packetNumber);
                System.out.println("    Sync Byte:                      " + String.format("0x%02X ", syncByte));
                System.out.println("    Transport Error Indicator:      " + "0b" + Integer.toBinaryString(transportErrorIndicator));
                System.out.println("    Payload Unit Start Indicator:   " + "0b" + Integer.toBinaryString(payloadUnitStartIndicator));
                System.out.println("    Transport Priority:             " + "0b" + Integer.toBinaryString(transportPriority));
                System.out.println("    PID:                            " + String.format("0x%04X  ", pid));
                System.out.println("    Transport Scrambling Control:   " + "0b" + Integer.toBinaryString(transportScramblingControl));
                System.out.println("    Adaptation Field Control:       " + "0b" + Integer.toBinaryString(adaptationFieldControl));
                System.out.println("    Continuity Counter:             " + String.format("0x%01X ", continuityCounter));
                System.out.println();
                
                // write to file
                writer.println();
                writer.println("\t Packet Number: \t\t\t" + packetNumber);
                writer.println("\t Sync Byte: \t\t\t" + String.format("0x%02X ", syncByte));
                writer.println("\t Transport Error Indicator: \t\t"+ "0b" + Integer.toBinaryString(transportErrorIndicator));
                writer.println("\t Payload Unit Start Indicator: \t\t"+ "0b" + Integer.toBinaryString(payloadUnitStartIndicator));
                writer.println("\t Transport Priority: \t\t\t"+ "0b" + Integer.toBinaryString(transportPriority));
                writer.println("\t PID: \t\t\t\t" + String.format("0x%04X  ", pid));
                writer.println("\t Transport Scrambling Control: \t" + "0b" + Integer.toBinaryString(transportScramblingControl));
                writer.println("\t Adaptation Field Control: \t\t" + "0b" + Integer.toBinaryString(adaptationFieldControl));
                writer.println("\t Continuity Counter: \t\t" + String.format("0x%01X ", continuityCounter));
                writer.println();

                packetNumber++;                
            }

            else{
                // File does not start with 0x47
                throw new IOException();
            }
            
        }
        writer.close();
    }
}