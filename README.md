# PyBBS
A simple message board and messaginig service with a "toy" authentication system. Built as a learning project.

Message Structure[size = 1024]:
[OPCODE Size=3][TOKEN size=9][NAME_LEN size=2][NAME size == Name_LEN<=12][DATA]

OPCODES:

Client-
AUT - Request User Auth
WDB - Write to Public DataBase
RDB - Read From Public DataBase
WMU - Write Message to User Inbox
RMB - Read Personal Inbox

Server -

ATF - Authorization Failed
ATS - Authorization Successful
