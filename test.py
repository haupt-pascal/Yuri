import threading
from cryptofuzz import getPrivateKey, PrivateKey_To_Address

def check_address(address):
    with open('rich.txt', 'r') as file:
        for line in file:
            if line.strip() == address:
                return True
    return False

def generate_address():
    private_key = getPrivateKey()
    address = PrivateKey_To_Address(private_key, compress=True)
    print(f"Generated address: {address}")
    return private_key, address

def search_address():
    while not found[0]:
        private_key, address = generate_address()
        if check_address(address):
            found[0] = True
            with open('found.txt', 'w') as file:
                file.write(f"Private Key: {private_key}\n")
                file.write(f"Address: {address}\n")
            print("Address found in rich.txt!")
            break

found = [False]
threads = []
for _ in range(4):
    thread = threading.Thread(target=search_address)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
