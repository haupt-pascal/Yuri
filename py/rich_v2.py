from cryptofuzz import Convertor, Generator

def check_address_in_file(address, filename):
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == address:
                return True
    return False

def generate_and_check_addresses():
    conv = Convertor()
    gen = Generator()

    while True:
        privatekey = gen.generate_private_key()
        compress_address = conv.hex_to_addr(privatekey, True)
        uncompress_address = conv.hex_to_addr(privatekey, False)

        if check_address_in_file(compress_address, 'rich.txt'):
            print(f"Compressed Address found in rich.txt: {compress_address}")
            break
        
        if check_address_in_file(uncompress_address, 'rich.txt'):
            print(f"Uncompressed Address found in rich.txt: {uncompress_address}")
            break

if __name__ == "__main__":
    generate_and_check_addresses()
