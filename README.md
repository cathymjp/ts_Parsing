# tsTesting

PID parser for MPEG ts streams based on ETSI EN 300 468 Digital Video Broadcasting (DVB); Specification for Service Information (SI) in DVB systems
Parse data for Electronic Program Guide (EPG) and additional information inteded for display to the user

It specifies the Service Information (SI) data which forms a part of DVB bitstreams, in order that the user can be provided with information to assist in selection of services and/or events within the bitstream. SI data for automatic configuration is mostly specified as Program Specific Information (PSI).
https://www.etsi.org/deliver/etsi_en/300400_300499/300468/01.16.01_60/en_300468v011601p.pdf


The PSI data provides information to enable automatic configuration of the receiver to demultiplex and decode the various streams of programs within the multiplex.

The PSI data is structured as four types of table
1. Program Association Table (PAT) - indicates the location (the Packet Identifier (PID) values of the Transport Stream (TS) packets) of the corresponding Program Map Table (PMT). It also gives the location of the Network Information Table (NIT).
2. Conditional Access Table (CAT)- provides information on the CA systems used in the multiplex
3. **Program Map Table (PMT)**: identifies and indicates the locations of the streams that make up each service and the location of the Program Clock Reference fields for a service
4. **Network Information Table (NIT)**: provide information about the physical network

***

Data is needed to provide identification of services and events for the user 
additional information defined within the present document can also provide information on services and events carried by different multiplexes, and even on
other networks

Data is structured as nine tables:
1. Bouquet Association Table (BAT): provides information regarding bouquets
2. **Service Description Table (SDT)**: contains data describing the services in the system e.g. names of services, the service provider, etc.
3) **Event Information Table (EIT)**: contains data concerning events or programmes such as event name, start time, duration, etc.
4) Running Status Table (RST): gives the status of an event (running/not running)<br />
5) **Time and Date Table (TDT)**: gives information relating to the present time and date
6) **Time Offset Table (TOT)**: gives information relating to the present time and date and local time offset
7) Stuffing Table (ST): used to invalidate existing sections
8) Selection Information Table (SIT): carries a summary of the SI information required to describe the streams in the partial bitstream
9) Discontinuity Information Table (DIT): inserted where the SI information in the partial bitstream may be discontinuous. 
