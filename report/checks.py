# alert also if not found - also check first 3 check first 3 chars for 'no '
ALERT_COMS = ['spanning-tree mode rapid-pvst', ' transport input ssh', 'service password-encryption', 'service timestamps log datetime localtime show-timezone']

ALERT_COMS_OR = [['logging 192.168.1.150','logging host 192.168.1.150'], ['logging 192.168.1.151','logging host 192.168.1.151']]

#'permit tcp any any eq 22', 'transport input telnet ssh' alert if found !
ALERT_FOUND_COMS = [' permit tcp any any eq 22', ' transport input telnet ssh']

ALERT_COMS_NO = ['no ip http server', 'no ip http secure-server']
# Commands display output:
DISPLAY_COMS = ['ntp server', 'clock timezone', 'clock summer-time',]
DIS_BLOCK_COMS = ['line vty']

# Commands that dont show in runnin Config
# logging trap informational
# crypto key generate rsa general-keys modulus 2048 - just as a side note ssh wont work without rsa keys generated
