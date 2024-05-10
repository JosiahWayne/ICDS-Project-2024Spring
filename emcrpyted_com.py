import random
import math

def is_prime(num):
    if num<=1:
        return False
    if num<=3:
        return True
    if num%2==0 or num%3==0:
        return False
    i=5
    while i*i<=num:
        if num%i==0 or num%(i+2)==0:
            return False
        i+=6
    return True

def generate_random_prime(bit_length):
    """生成指定位数的随机素数"""
    while True:
        num = random.getrandbits(bit_length)
        if num%2==0:
            num+=1
        if is_prime(num):
            return num

def multiplicative_inverse(e,phi):
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
    return int(old_s)
    
def generate_keypair(bit_length):
    p=generate_random_prime(bit_length)
    q=generate_random_prime(bit_length)
    n=p*q
    a=p-1
    b=q-1
    gcd=math.gcd(a,b)
    lcm=(a*b)/gcd
    public_e=random.randint(1,lcm)
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
        keypair=generate_keypair(8)
        print(keypair)
        encrypted=encrypt(words,keypair[0])
        print(encrypted)
        decrpyted=decrypt(encrypted,keypair[1])
        print(decrpyted)
    main()'''