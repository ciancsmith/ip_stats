#!usr/bin/env_python
import textwrap as t
from collections import Counter
import os



#note this code is quite modular as I prefer it this way it looks cleaner and allows me to make quick changes that can affect the entire program

#Dict with class name as key and the prefix as value to make the program more dynamic
classes = {'A': '0', 'B': '10', 'C': '110', 'D': '1110', 'E': '1111'}

#Yes I only realised after attempting the question that this resourse was available on the rubric xD
class_info = {'A':{
 'network_bits':7,
 'host_bits':24
 },
 'B':{
 'network_bits':14,
 'host_bits':16
 },
 'C':{
 'network_bits':21,
 'host_bits':8
 },
 'D':{
 'network_bits':'N/A',
 'host_bits':'N/A'
 },
 'E':{
 'network_bits':'N/A',
 'host_bits':'N/A'
 }
}


#this function takes an ip as a parameter and returns stats based on the ip
def get_class_stat(ip_addr):
    #split the ip into a list based on the character "." there is a flaw here for ips with a ":" char
    #convert the ip list into its binary counter-part
    binary = convert_to_binary(ip_addr)

    #check the prefix of the first element in binary to get class
    class_type = check_class(binary)
    networks = check_networks(class_type)
    hosts = check_hosts(class_type)
    addresses = get_range(class_type)
    firstAddress, lastAddress = addresses[0], addresses[1]
    #print('class: {}\nnetworks: {}\nhosts: {}\nfirst address: {}\nlast address: {}'.format(class_type, networks, hosts, firstAddress, lastAddress))
    return(class_type, networks, hosts, firstAddress, lastAddress)


def convert_to_binary(string):
    #split the ip into a list based on the character "." there is a flaw here for ips with a ":" char
    if type(string) == str:
        string_list = string.split(".")
    else:
        string_list = string
    
    binary = [('{0:08b}').format(int(x)) for x in string_list]
    return binary

def convert_decimal_dot(list):
    return ".".join([str(int(x,2)) for x in list])



def check_class(binary_ip):
    global classes
    first_byte = binary_ip[0]
    bits = ''
    for bit in first_byte:
        bits += bit
#The following code seems a little clunky may look for a way to optimise this.        
        if bits == '0':
            #this is to get the dictionary key for the corresponding value
            return(list(classes.keys())[list(classes.values()).index(bits)])
        elif bits == '10':
            return(list(classes.keys())[list(classes.values()).index(bits)])
        elif bits == '110':
            return(list(classes.keys())[list(classes.values()).index(bits)])
        elif bits == '1110':
            return(list(classes.keys())[list(classes.values()).index(bits)])
        elif bits == '11111':
            return(list(classes.keys())[list(classes.values()).index(bits)])
        else:
            continue

def check_networks(class_type):
    #function to get the number of network addresses
    if class_type == 'A':
        networks = 2**(8-1)
    if class_type == 'B':
        networks = 2**(16-2)
    if class_type == 'C':
        networks = 2**(24-3)
    if class_type == 'D' or class_type == 'E':
        networks = 'N/A'
    return networks

def check_hosts(class_type):
    #function to get the number of host addresses
    if class_type == 'A':
        hosts = (2**24) - 2
    if class_type == 'B':
        hosts = (2**16) - 2
    if class_type == 'C':
        hosts = (2**8) - 2
    if class_type == 'D' or class_type == 'E':
        hosts = 'N/A'
    return hosts


def get_range(class_type):
    #function to get tuple of class ranges
    if class_type == 'A':
        range_t = ('0.0.0.0', '127.255.255.255')
    if class_type == 'B':
        range_t = ('128.0.0.0', '191.255.255.255')
    if class_type == 'C':
        range_t = ('192.0.0.0', '223.255.255.255')
    if class_type == 'D':
        range_t = ('224.0.0.0', '239.255.255.255')
    if class_type == 'E':
        range_t = ('240.0.0.0', '255.255.255.255')
    return range_t


def get_subnet_stats(ip_addr, subnet_mask):
    b_ip = convert_to_binary(ip_addr)
    sub_bin = convert_to_binary(subnet_mask)
    cidr = count_ones(sub_bin)
    address = ip_addr + "/" + str(cidr)
    f_addr, l_addr, valid_subs, v_host, nets, b_addrs = calculate_subnets(b_ip, cidr, sub_bin)
    #print("Address: {}\nSubnets: {}\nAddressable Hosts per subnet: {}\nValid Subnets: {}\n Broadcast Addresses: {}\nFirst Addresses: {}\nLast Addresses: {}".format(address, nets,
    #v_host, valid_subs, b_addrs, f_addr, l_addr))

    return(address, nets,v_host, valid_subs, b_addrs, f_addr, l_addr)


def get_supernet_stats(ip_list):
    first_ip = ip_list[0]
    last_ip = ip_list[len(ip_list) - 1]
    last_ip = convert_to_binary(last_ip)
    first_ip = convert_to_binary(first_ip)
    string1="".join(first_ip) 
    string2="".join(last_ip)
    common = os.path.commonprefix([string1, string2])
    cidr = len(common)
    while len(common)  < 32:
        common += "0"
    supernet = "".join(common)
    supernet = t.wrap("".join(supernet), 8)
    supernet = convert_decimal_dot(supernet) + "/" + str(cidr)
    mask = ""
    while len(mask) < 32:
        if len(mask) <= cidr:
            mask += "1"
        else:
            mask += "0"

    netmask = t.wrap(mask, 8)
    netmask = convert_decimal_dot(netmask)
    #print("Address: {}\nNetwork Mask: {}".format(supernet, netmask))
    return(supernet, netmask)
    


    

def count_ones(binary_list):
    binary_string = "".join(binary_list)
    ones = len([x for x in binary_string if x == "1"])
    return ones


def calculate_subnets(binary_ip, cidr, sub_bin):
    ip_class = check_class(binary_ip)
    if ip_class == "A":
        return("Not done yet")
    if ip_class == "B":
        host_bits_used = class_info['B']['host_bits'] - (32 - int(cidr))
        networks = 2**(host_bits_used)
        valid_hosts = (2**(16-host_bits_used)) - 2
        net_addr = get_net_id(binary_ip, sub_bin)
        first_addrs = get_first_addrs(net_addr, valid_hosts + 2, networks, ip_class, cidr)
        valid_subnets = get_valid_subnets(net_addr, valid_hosts + 2, networks, ip_class, cidr)
        last_addrs = get_last_addrs(net_addr, valid_hosts + 2, networks, ip_class, cidr)
        broadcast_addrs = get_broadcast_addrs(net_addr, valid_hosts + 2, networks, ip_class, cidr)
        return(first_addrs, last_addrs, valid_subnets, valid_hosts, networks, broadcast_addrs)
        
    if ip_class == "C":
        host_bits_used = class_info['C']['host_bits'] - (32 - int(cidr))
        networks = 2**(host_bits_used)
        valid_hosts = (2**(8-host_bits_used)) - 2
        net_addr = get_net_id(binary_ip, sub_bin)
        first_addrs = get_first_addrs(net_addr, valid_hosts + 2, networks, ip_class, cidr)
        valid_subnets = get_valid_subnets(net_addr, valid_hosts + 2, (valid_hosts + 2), ip_class, cidr)
        last_addrs = get_last_addrs(net_addr, valid_hosts + 2, networks, ip_class, cidr)
        broadcast_addrs = get_broadcast_addrs(net_addr, valid_hosts + 2, networks, ip_class, cidr)
        return(first_addrs, last_addrs, valid_subnets, valid_hosts, networks, broadcast_addrs)


def get_first_addrs(net, inc, networks, ip_class, cidr):
    i = 0
    net = net.split(".")
    addrs = []

    if ip_class == "A":
        net_chunk = None
        print(net)
        #while i <= networks:
    
    
    if ip_class == "B" and int(cidr) <= 23:
        inc = inc // 256
        for chunks in net:
            if chunks == '0':
                net_chunk = int(chunks)
        addrs = []
        while i <= networks and int(net_chunk) < 256:
            net.pop()
            net.pop()
            net.append(str(net_chunk))
            net.append(str(1))
            addr = ".".join(net)
            addrs.append(addr)
            net_chunk += (inc)
            i += 1
    if ip_class == "C" or int(cidr) >= 24:
        net_chunk = int(net[3]) + 1
        addrs = []
        while i <= networks and int(net_chunk) < 255:
            net.pop()
            net.append(str(net_chunk))
            addr = ".".join(net)
            addrs.append(addr)
            net_chunk += inc
            i += 1
        
    return(addrs)


def get_last_addrs(net, inc, networks, ip_class, cidr):
    i = 0
    net = net.split(".")
    addrs = []

    if ip_class == "A":
        net_chunk = None
        print(net)
        #while i <= networks:
    
    if ip_class == "B" and int(cidr) <= 23:
        inc = inc // 256
        for chunks in net:
            if chunks == '0':
                net_chunk = int(chunks) - 1
        addrs = []
        while i <= networks and int(net_chunk) < 256:
            last_val = net.pop()
            net.pop()
            net.append(str(net_chunk))
            net.append('254')
            addr = ".".join(net)
            if net_chunk > 0:
                addrs.append(addr)
            net_chunk += (inc)
            i += 1
    if ip_class == "C" or int(cidr) >= 24:

        net_chunk = int(net[3]) + (inc - 2)
        addrs = []
        while i <= networks and int(net_chunk) < 256:
            net.pop()
            net.append(str(net_chunk))
            addr = ".".join(net)
            addrs.append(addr)
            net_chunk += inc
            i += 1
        
    return(addrs)

def get_valid_subnets(net, inc, networks, ip_class, cidr):
    i = 0
    net = net.split(".")
    addrs = []


    if ip_class == "A":
        net_chunk = None
        print(net)
        #while i <= networks:
    if ip_class == "B" and int(cidr) <= 23:
        inc = inc // 256
        for chunks in net:
            if chunks == '0':
                net_chunk = int(chunks)
        addrs = []
        while i <= networks and int(net_chunk) < 256:
            last_val = net.pop()
            net.pop()
            net.append(str(net_chunk))
            net.append(str(last_val))
            addr = ".".join(net)
            addrs.append(addr)
            net_chunk += (inc)
            i += 1
    if ip_class == "C" or int(cidr) >= 24:
        net_chunk = int(net[3])
        addrs = []

        while i <= networks and int(net_chunk) < 256:
            net.pop()
            net.append(str(net_chunk))
            addr = ".".join(net)
            addrs.append(addr)
            net_chunk += inc
            i += 1
    
    return(addrs)


def get_broadcast_addrs(net, inc, networks, ip_class, cidr):
    i = 0
    net = net.split(".")
    addrs = []

    if ip_class == "A":
        net_chunk = None
        print(net)
        #while i <= networks:
    if ip_class == "B" and int(cidr) <= 23:
        inc = inc // 256
        for chunks in net:
            if chunks == '0':
                net_chunk = int(chunks) - 1
        addrs = []
        while i <= networks and int(net_chunk) < 256:
            net.pop()
            net.pop()
            net.append(str(net_chunk))
            net.append('255')
            addr = ".".join(net)
            if net_chunk > 0:
                addrs.append(addr)
            net_chunk += (inc)
            i += 1
    if ip_class == "C" or int(cidr) >= 24:
        net_chunk = int(net[3])
        addrs = []
        while i <= networks and int(net_chunk) < 256:
            net.pop()
            if net_chunk == 0:
                net_chunk += inc - 1
                net.append(str(net_chunk))
                addr = ".".join(net)
                addrs.append(addr)
            else:
                net.append(str(net_chunk))
                addr = ".".join(net)
                addrs.append(addr)
            
            net_chunk += (inc)
            i += 1
       
    return(addrs)
        


    






def get_net_id(b_ip, s_ip):
    b_ip = int("".join(b_ip), 2)
    s_ip = int("".join(s_ip), 2)
    net_id = b_ip & s_ip
    net_id = "".join([('{0:08b}').format(int(x)) for x in str(net_id).split()])
    net_id = t.wrap(net_id, 8)
    net_id = ".".join([str(int(x,2)) for x in net_id])
    return(net_id)



def get_increment(valid_host, ip_class):
    inc = 256 // valid_host
    return inc

        

def main():
    ip = input("Please enter the Ip address in DOT notation: ")
    subnet_mask = input("testing purposes")
    get_class_stat(ip)
    get_subnet_stats(ip, subnet_mask)
    get_supernet_stats(["192.168.10.0","192.168.10.1","192.168.10.2","192.168.10.3"])
if __name__ == '__main__':
    main()
    