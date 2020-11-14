import sys
valid_subnet_masks = [255, 252, 224, 248, 240, 224, 192, 128, 0]


def validate_subnet(subnet: str) -> bool:
    x = subnet.split(".")
    if x[0] != "255" or len(subnet) < 4:
        return False
    for y in x:
        z = int(y)
        if z not in valid_subnet_masks:
            return False
    return True


def validate_ipaddress(ipaddress: str) -> bool:
    if ipaddress == "127.0.0.1":
        return False
    x = ipaddress.split(".")
    if x[0] == "225" or len(ipaddress) < 4:
        return False
    y = int(x[0])
    if 254 >= y >= 224:
        return False
    for k in x:
        if int(k) > 255:
            return False
    return True


def bit_array_conversion(address: str) -> [str]:
    x = address.split(".")
    holder = []
    for y in x:
        holder_octet = str(bin(int(y)))[2:]
        if len(holder_octet) < 8:
            holder_octet = pad_out_octet(holder_octet)
        holder.append(holder_octet)
    return holder


def pad_out_octet(octet: str):
    if len(octet) < 8:
        octet = "0" + octet
        octet = pad_out_octet(octet)
    return octet


def pad_out_num(num: str):
    if len(num) < 3:
        num = "0" + num
        num = pad_out_num(num)
    return num


def get_network_address(ip_address: str, subnet: str) -> str:
    network_address = ""
    x = ip_address.split(".")
    y = subnet.split(".")
    for num in range(len(y)):
        h = int(x[num])
        u = int(y[num])
        network_address = network_address + str(bitwise_and(h, u))
        if num != len(y) - 1:
            network_address = network_address + "."
    return network_address


def get_subnet_in_binary(subnet: str) -> str:
    octets = bit_array_conversion(subnet)
    holder = ""
    for x in range(len(octets)):
        holder = holder + octets[x]
        if x < len(octets) - 1:
            holder = holder + "."
    return holder


def get_wildcard_mask(subnet: str) -> str:
    subnet_split = subnet.split(".")
    holder_wildcard_mask = ""
    for x in subnet_split:
        holder = 255 - int(x)
        holder_wildcard_mask = holder_wildcard_mask + pad_out_num(str(holder))
    return ".".join(holder_wildcard_mask[i:i + 3] for i in range(0, len(holder_wildcard_mask), 3))


def get_broadcast_address(ipaddress: str, subnet: str):
    ipaddress_split = ipaddress.split(".")
    subnet_split = subnet.split(".")
    holder = ""
    for x in range(len(subnet_split)):
        if int(subnet_split[x]) == 255:
            holder = holder + (ipaddress_split[x])
            if x < len(subnet_split) -1:
                holder=holder +"."
        elif int(subnet_split[x]) == 0:
            holder = holder + "255"
            if x < len(subnet_split) - 1:
                holder = holder + "."
        else:
            holder = holder + str(calculate_difference(int(subnet_split[x]), int(ipaddress_split[x])))
            if x < len(subnet_split) - 1:
                holder = holder + "."
    return holder


def calculate_difference(x: int, y: int):
    j = 256 - x
    holder_j = j
    while not (j > y):
        j = j + holder_j
    return j - 1


def bitwise_and(a: int, b: int) -> int:
    c = a & b
    return c


def get_usable_hosts(subnet_binary: str) -> str:
    counter = 0
    for x in subnet_binary:
        if x == "0":
            counter = counter + 1
    usable_hosts = (2 ** counter) - 2
    return str(usable_hosts)


def check_input(subnet:str, ipAddress:str):
    holder_s=subnet
    holder_ip=ipAddress
    if not validate_subnet(subnet):
        print("Your subnet is invalid")
        holder_s = input("Pass a new subnet? Or enter N to quit.")
    if not validate_ipaddress(ipAddress):
        print("Your IP address is invalid")
        holder_ip = input("Pass a new IP address? Or enter N to quit.")
    if holder_s == "N" or holder_ip == "N":
        sys.exit()
    if validate_ipaddress(holder_ip) and validate_subnet(holder_s):
        core_program(holder_s,holder_ip)
    else:
        check_input(holder_s,holder_ip)


def core_program(subnet: str, ipAddress: str):
    network_address = get_network_address(ipAddress, subnet)
    print("Network Address :" + network_address)
    print("Subnet in Binary :" + get_subnet_in_binary(subnet))
    print("Broadcast Address :" + get_broadcast_address(ipAddress,subnet))
    print("Wildcard Mask :" + get_wildcard_mask(subnet))
    print("Usable Hosts :" + get_usable_hosts(get_subnet_in_binary(subnet)))


if __name__ == '__main__':
    ipAddress = input("Enter IP Address:")
    subnet = input("Enter Subnet:")
    check_input(subnet,ipAddress)
