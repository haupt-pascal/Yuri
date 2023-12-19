import bitcoin
import requests
import threading
def check_address(address):
    with open('rich.txt', 'r') as file:
        for line in file:
            if line.strip() == address:
                return True
    return False

def generate_address():
    private_key = bitcoin.random_key()
    public_key = bitcoin.privkey_to_pubkey(private_key)
    address = bitcoin.pubkey_to_address(public_key)
    print(private_key)
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


