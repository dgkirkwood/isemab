# MAB device-replacement program using Cisco ISE + Spark

This project uses a Spark chat interface to give non-IT personnel the ability to replace network-connected devices that require MAC Authentication Bypass (MAB).

See ISEAPI.py for generic API calls to ISE and Spark
See mabReplace.py for the main program logic

Note currently this script requires a settings file containing the following: 
* Server IP
* ISE ERS username
* ISE ERS password
* The Spark Room ID
* The Spark Bot token
* The Spark Bot ID

In future revisions the process of retrieving this data and creating the settings file will be automated. 