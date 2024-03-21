from cryptography.hazmat.primitives import hashes, hmac

def plain2bitstring(plain: str):
    return "".join(format(ord(c), "0>8b") for c in plain)

def plain2bitarray(plain: str):
    bitstring = plain2bitstring(plain)
    encoded = bytearray([int(b) for b in bitstring])
    return encoded

key_origin = 'test key'
key = plain2bitarray(key_origin)
h = hmac.HMAC(key, hashes.SHA256())
h.update(b"message to hash")
signature = h.finalize()
#print(signature)

def byte2bitstring(plain: bytes):
    return "".join(format(c, "0>8b") for c in plain)

s_signature = [ord(k) for k in list(byte2bitstring(signature))]
#print(s_signature)
mac_id = s_signature[:4]+[0,0,0,0]
print(mac_id)

MOD = 256

def KSA(key):
    ''' Key Scheduling Algorithm (from wikipedia):
        for i from 0 to 255
            S[i] := i
        endfor
        j := 0
        for i from 0 to 255
            j := (j + S[i] + key[i mod keylength]) mod 256
            swap values of S[i] and S[j]
        endfor
    '''
    key_length = len(key)
    # create the array "S"
    S = [n for n in range(MOD)]  # [0,1,2, ... , 255]
    j = 0
    for i in range(0,MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values

    return S


def PRGA(S):
    ''' Psudo Random Generation Algorithm (from wikipedia):
        i := 0
        j := 0
        while GeneratingOutput:
            i := (i + 1) mod 256
            j := (j + S[i]) mod 256
            swap values of S[i] and S[j]
            K := S[(S[i] + S[j]) mod 256]
            output K
        endwhile
    '''
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % MOD]
        yield K

def get_keystream(key):
    ''' Takes the encryption key to get the keystream using PRGA
        return object is a generator
    '''
    S = KSA(key)
    return PRGA(S)

def encrypt(key, plaintext):
    ''' :key -> encryption key used for encrypting, as hex string
        :plaintext -> string to encrpyt/decrypt
    '''
    # For plaintext key, use this
    key = [ord(c) for c in key]

    # If key is in hex:
    # key = key.decode('hex')
    # key = [ord(c) for c in key]

    # Get the keystream
    keystream = get_keystream(key)

    res = []
    for c in plaintext:
        if type(c) == type('s'):
            val = ("%02X" % (ord(c) ^ next(keystream)))  # XOR and taking hex
        else:
            val = ("%02X" % (c ^ next(keystream)))
        res.append(val)
    return ''.join(res)

key_rc = 'I want go home'
plaintext = 'Today is a thursday'
ciphertext = encrypt(key_rc, plaintext)
print(ciphertext)

ciphertext = encrypt(key_origin, mac_id)
print(ciphertext)

def decrypt(key, ciphertext):
    ''' :key -> encryption key used for encrypting, as hex string
        :ciphertext -> hex encoded ciphered text using RC4
    '''
    ciphertext = bytes.fromhex(ciphertext)

    print('ciphertext to func:', ciphertext)  # optional, to see
    res = encrypt(key, ciphertext)
    return bytes.fromhex(res)

decrypted = decrypt(key_origin, ciphertext)
print(decrypted)