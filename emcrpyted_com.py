import random

def miller_rabin_primality_test(n, k=128):
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Write n as d * 2^r + 1
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    def witness(a, d, n):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True
        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                return True
        return False

    # Perform k rounds of testing
    for _ in range(k):
        a = random.randint(2, n - 2)
        if not witness(a, r, n):
            return False

    return True

def generate_random_prime(bit_length):
    while True:
        num = random.getrandbits(bit_length)
        if num%2==0:
            num+=1
        if miller_rabin_primality_test(num):
            return num

def multiplicative_inverse(e, phi):
    old_r, r = e, phi
    old_s, s = 1, 0
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    if old_r > 1:
        return None
    if old_s < 0:
        old_s += phi
    return old_s

def gcd_(a, b):
    while b != 0:
        a, b = b, a % b
    return a

    
def generate_keypair(bit_length):
    p=generate_random_prime(bit_length)
    q=generate_random_prime(bit_length)
    n=p*q
    a=p-1
    b=q-1
    lcm=a*b
    public_e=random.randrange(1,lcm)
    gcd=gcd_(public_e,lcm)
    while gcd!=1:
        public_e=random.randrange(1,lcm)
        gcd=gcd_(public_e,lcm)
    public_n=n
    private_d=multiplicative_inverse(public_e,lcm)
    return ((public_e,public_n),(private_d,public_n))

def encrypt(origin_msg,keypair):
    e,n=keypair
    encrypted_msg=[pow(ord(c), e, n) for c in origin_msg]
    return encrypted_msg

def decrypt(encrpted_msg,keypair):
    d,n=keypair
    origin_msg_list=[chr(pow(c, d, n)) for c in encrpted_msg]
    origin_msg=''.join(origin_msg_list)
    return origin_msg
    
'''def main():
    words="abcdefg"
    keypair=generate_keypair(256)
    print(keypair)
    encrypted=encrypt(words,keypair[0])
    print(encrypted)
    decrpyted=decrypt(encrypted,keypair[1])
    print(decrpyted)
main()'''