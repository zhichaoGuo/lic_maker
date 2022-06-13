import re


def is_mac(mac: str):
    # 00:1f:c1:00:00:0f 或 001fc100000f
    if mac.find(':') != -1:
        pattern = re.compile(r"^\s*([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\s*$")
    elif len(mac) == 12:
        pattern = re.compile(r"^\s*[0-9a-fA-F]{12}\s*$")
    else:
        return False
    if pattern.match(mac):
        return True
    else:
        return False


def mac_12_2_17(mac: str):
    # 001fc100000f -> 00:1f:c1:00:00:0f
    if len(mac) != 12:
        return False
    if is_mac(mac):
        return mac[0:2] + ':' + mac[2:4] + ':' + mac[4:6] + ':' + mac[6:8] + ':' + mac[8:10] + ':' + mac[10:12]
    return False


def mac_17_2_12(mac: str):
    # 00:1f:c1:00:00:0f -> 001fc100000f
    if len(mac) != 17:
        return False
    if is_mac(mac):
        return mac.replace(':', '')
    return False


def gen_mac_list(start_mac, stop_mac):
    # 处理001fc100000f 返回[00:1f:c1:00:00:0f]
    if len(start_mac) == 17:
        start_mac = mac_17_2_12(start_mac)
    if len(stop_mac) == 17:
        stop_mac = mac_17_2_12(stop_mac)
    if start_mac == stop_mac :
        return [start_mac]
    if int(stop_mac, 16) < int(start_mac, 16):
        start_mac, stop_mac = stop_mac, start_mac
    mac_list = list()
    for i in range(int(stop_mac, 16) - int(start_mac, 16) + 1):
        mac_address = "{:012X}".format(int(start_mac, 16) + i)
        mac_list.append(mac_12_2_17(mac_address))
    return mac_list


if __name__ == '__main__':
    print(gen_mac_list('00:1f:c1:00:00:10', '00:1f:c1:00:00:11'))
