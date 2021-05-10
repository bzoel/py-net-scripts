## Billy Zoellers, Dean Dorton 2021
##
## usage: guestshell run python3 rolling_pcap.py <tftp|ftp|scp> <transfer-server-ip> <cap-intf>
##  example: guestshell run python3 rolling_pcap.py tftp 192.168.1.112 GigabitEthernet0/0/0

import cli
from datetime import datetime
import sys

if (len(sys.argv) != 4):
  print('ERROR: missing arguments')
  print('  usage "guestshell run python3 rolling_pcap.py <tftp|ftp|scp> <transfer-server-ip> <cap-intf>"')
  exit()

## ----- Parameters
capture_name = 'pythoncap'
server_protocol = sys.argv[1]
server_ip = sys.argv[2]
capture_intf = sys.argv[3]
friendly_intf = capture_intf.replace('/', '-')
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
## ----- End Parameters

## ----- Commands
stop_capture = [
  f'monitor capture {capture_name} stop_export',
]
create_capture = [
  f'monitor capture {capture_name} interface {capture_intf} both buffer size 100 match ipv4 any any',
  f'monitor capture {capture_name} start'
]
export_capture = [
  f'copy bootflash:{capture_name}.pcap {server_protocol}://{server_ip}/{friendly_intf}_{timestamp}.pcap',
  f'delete /force bootflash:{capture_name}.pcap',
]
## ----- End Commands

# Run different command set if a capture is already running
existing_cap = cli.execute(f'show monitor capture {capture_name}')
print(existing_cap)
commands = []
if 'does not exist' in existing_cap:
  commands += create_capture
else:
  commands += stop_capture + create_capture + export_capture

# Execute commands
for command in commands:
  cli.executep(command)