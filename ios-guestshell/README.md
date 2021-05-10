# Guestshell Tools

This repository contains a collection of scripts created to run in guestshell on Cisco devices.

### Rolling PCAP (rolling-pcap.py)
**Purpose**: Create a constant packet capture using `monitor capture` functionality on a Cisco router. At the user-defined interval, the .pcap file will be timestamped and uploaded to a TFTP server
**Setup**:
  This tool is intended to be triggered by EEM on a Cisco device. You should already have guestshell setup, with appropriate network access to the TFTP server.

  1. Copy rolling-pcap.py to the router's `flash:guest-share` directory
  2. Create an EEM applet to trigger the script at your defined interval

    ```
    event manager applet rolling-pcap

      event timer watchdog name "every 10 mins" time 600 maxrun 120

        action 0.0 cli command "enable"

        action 1.0 cli command "guestshell run python3 /bootflash/guest-share/rolling-pcap.py <tftp|ftp|scp> <transfer-server-ip> <cap-intf>"
    ```
    
    *Note:* The `event timer watchdog` command controls the interval and maximum run time
      - `time 600` is the default interval of "every 10 mins" in seconds. You may need to adjust this.
      - `maxrun 120` is the maximum time the script is allowed to run. You may need to adjust this if the file transfer is taking longer than 120 seconds.

  To confirm the tool is running:

    ```
    R1#show event manager history events

    No.  Job Id Proc Status   Time of Event            Event Type        Name

    1    72991  Actv success  Wed Mar10 13:22:46 2021  timer watchdog    applet: rolling-pcap

    ```
