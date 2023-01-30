# ts (transport stream) Parser

## Introduction
- PID parser for MPEG ts streams based on ETSI EN 300 468 Digital Video Broadcasting (DVB); 
- Specification for Service Information (SI) in DVB systems
- Parse data for Electronic Program Guide (EPG) and additional information inteded for display to the user
- SI data for automatic configuration is mostly specified as Program Specific Information (PSI).


## Description
:small_orange_diamond: This parser parses data from ts streams described in bold. 
<br />
<br />
A) PSI: information to enable automatic configuration of the receiver to demultiplex and decode the various streams of programs
1. Program Association Table (PAT) - location of the Program Map Table(PMT), Network Information Table(NIT)
2. Conditional Access Table (CAT)- CA systems used in the multiplex
3. **Program Map Table (PMT)**: locations of the streams that make up each service and the Program Clock Reference for a service
4. **Network Information Table (NIT)**: information about the physical network


B) Data: identification of services and events for the user
1. Bouquet Association Table (BAT): information of bouquets
2. **Service Description Table (SDT)**: services in the system e.g. names of services, the service provider, etc.
3) **Event Information Table (EIT)**: events or programs such as event name, start time, duration, etc.
4) Running Status Table (RST): status of an event (running/not running)<br />
5) **Time and Date Table (TDT)**: present time and date
6) **Time Offset Table (TOT)**: ipresent time and date and local time offset
7) Stuffing Table (ST): invalidate existing sections
8) Selection Information Table (SIT): SI required to describe the streams in the partial bitstream
9) Discontinuity Information Table (DIT): inserted where the SI in the partial bitstream may be discontinuous


Reference: https://www.etsi.org/deliver/etsi_en/300400_300499/300468/01.16.01_60/en_300468v011601p.pdf
