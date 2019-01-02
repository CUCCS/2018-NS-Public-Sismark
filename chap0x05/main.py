import logging
from scapy.layers.inet import *
import argparse

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

src_port = RandShort()


def tcp_scan(packet, dst_ip, dst_port, flags):
    if ('NoneType' in str(type(packet))):
        if flags == "FPU":
            print("Open|Filtered")
        else:
            print("Unreachable|Filtered")
    elif (packet.haslayer(TCP)):
        ret_flags = packet.getlayer(TCP).flags
        if ret_flags == 0x12:
            send_rst = sr(IP(dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags=flags), timeout=10)
            print("Open")
        elif ret_flags == 0x14:
            print("Closed")
    return 0


def udp_scan(packet):
    if 'NoneType' in str(type(packet)):
        print("Open|Filtered")
    elif packet.haslayer(UDP):
        print("Open")
    return 0


def send_packet(type, dst_ip, dst_port, flags):
    if "tcp" in type:
        packet = sr1(IP(dst=dst_ip) / TCP(sport=src_port,
                                          dport=dst_port, flags=flags), timeout=10)
        if type == 'tcp1' and flags == "S":
            tcp_connect_scan = tcp_scan(packet, dst_ip, dst_port, "AR")
        elif type == 'tcp2' and flags == "S":
            tcp_stealth_scan = tcp_scan(packet, dst_ip, dst_port, "R")
        elif type == 'tcp3' and flags == "FPU":
            tcp_xmas_tree_scan = tcp_scan(packet, dst_ip, dst_port, "FPU")
        else:
            print('ERROR')
    if "udp" == type:
        packet = sr1(IP(dst=dst_ip) / UDP(dport=dst_port), timeout=10)
        udp__scan = udp_scan(packet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='main')
    parser.add_argument('type', type=str)
    parser.add_argument('dst_ip', type=str)
    parser.add_argument('dst_port', type=int)
    parser.add_argument('-f', '--flags', type=str)
    args = parser.parse_args()
    send_packet(args.type, args.dst_ip, args.dst_port, args.flags)

