This is the repository for HW1, CSC 8820 - Advanced Computer Network (GSU - CS dept)
The program use TCP to simulate selective repeat protocols with NAK only.
There are three entities in the program. 
 - Server send Y packets consecutively to client
 - Client check missing packets, send NAK for each one upon receiving new packet
 - Router in the middle of Client and Server, forwarding the packet, and drop one with a probability
