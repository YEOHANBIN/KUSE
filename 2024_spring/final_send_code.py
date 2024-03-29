import can
from cryptography.hazmat.primitives import hashes, hmac
import time
import hashlib

def plain2bitstring(plain: str):
    return "".join(format(ord(c), "0>8b") for c in plain)

def plain2bitarray(plain: str):
    bitstring = plain2bitstring(plain)
    encoded = bytearray([int(b) for b in bitstring])
    return encoded

def decimal2bytes(decimal_list):
    byte_string = bytes(decimal_list)
    return byte_string

def KSA(key):
    key_length = len(key)
    S = [n for n in range(MOD)]
    j = 0
    for i in range(0,MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % MOD]
        yield K

def get_keystream(key):
    S = KSA(key)
    return PRGA(S)

def encrypt(key, plaintext):
    # For plaintext key, use this
    if type(key) == type('abc'):
        key = [ord(c) for c in key]
    else:
        # If key is in hex:
        key = key.decode('hex')
        key = [ord(c) for c in key]

    # Get the keystream
    keystream = get_keystream(key)

    res = []
    for c in plaintext:
        if type(c) == type('s'):
            val = ("%02X" % (ord(c) ^ next(keystream)))  # XOR and taking hex
        elif type(c) == bytes:
            val = ("%02X" % (ord(c) ^ next(keystream)))
        else:
            val = ("%02X" % (c ^ next(keystream)))
        res.append(val)
    return res

def diffie_hellman(prime, generator, private_key):
    public_key = pow(generator, private_key, prime)  # Use pow() for exponentiation
    return public_key

# Function to generate key table using SHA-256
def generate_key_table(final_key):
    global key_table  # Declare key_table as global
    sha256 = hashlib.sha256()
    sha256.update(str(final_key).encode())
    key_hash = sha256.hexdigest()
    key_table = [key_hash[i*16:(i+1)*16] for i in range(0,len(key_hash))]

    return key_table

def send_key():
    node1_public_key = diffie_hellman(prime, generator, node1_private_key)
    data_to_send = [node1_public_key, 0, 0, 0, 0, 0, 0, 0]
    msg = can.Message(arbitration_id=node1_CAN_ID, data=data_to_send, is_extended_id = False)
    bus.send(msg)
    print("Send Diffie-Hellman Key")
    print('\n================================\n')

bus = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

MOD = 256
node1_CAN_ID = 0x456
node2_CAN_ID = 0x123
node1_private_key = 15
prime = 23
generator = 5

# Initialize an empty key table
key_table = None
update_count=0

while 1:
    # Receive
    message = bus.recv(3.0)

    if message is None:
        print('No message received')
        print('\n================================\n')
    else:
        if message.arbitration_id == 0x123:             # 0x123 is other node's diffie hellman message id        
            received_key = message.data[0]
            print('Received Diffie Key: ', received_key)
            final_key = diffie_hellman(prime, received_key, node1_private_key)
            print('Final Diffie Key: ', final_key)

            key_table = generate_key_table(final_key)
            print('Key table: ', key_table)
        elif message.arbitration_id == 0x999:           # 0x999 is error message
            key_table = None
        else:
            pass
    
    # Send
    data = [12, 21, 33, 47]
    if key_table == None:
        send_key()
    else:
        if type(key_table[0]) != bytearray:
            key = plain2bitarray(key_table[0])

        # HMAC Algorithm using SHA-256
        print('KEY: ', key)
        h = hmac.HMAC(key, hashes.SHA256())
        mac_data = decimal2bytes(data)
        h.update(mac_data)
        signature = h.finalize()
        print('Initial MAC: ',signature)

        # Generate Send Message
        signature = [byte for byte in signature]
        send_data = signature[:4] + data
        print('Send Data: ', send_data)

        # Encryption using RC4
        hex_key = key.hex()

        ciphertext = encrypt(hex_key, send_data)
        cipher_msg = [int(h,16) for h in ciphertext]
        print('Cipher Data: ', cipher_msg)

        # Send Can Message
        message = can.Message(arbitration_id=0x01, data=cipher_msg, is_extended_id=False)
        bus.send(message)

        time.sleep(3)


        # Key Regeneration
        digest = hashes.Hash(hashes.SHA256())
        digest.update(key)
        key_table[0] = digest.finalize()
        print('Key Regeneration: ', key)
        print('\n==============================\n')