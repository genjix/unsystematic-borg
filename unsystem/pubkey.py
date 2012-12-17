import ecdsa
import hashlib
import lib.bitcoin as bitcoin
from ecdsa.ellipticcurve import Point

##########################
# init master public key
##########################

# from bitcoin.py
# secp256k1, http://www.oid-info.com/get/1.3.132.0.10
_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
_b = 0x0000000000000000000000000000000000000000000000000000000000000007L
_a = 0x0000000000000000000000000000000000000000000000000000000000000000L
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L
curve_secp256k1 = ecdsa.ellipticcurve.CurveFp( _p, _a, _b )
generator_secp256k1 = ecdsa.ellipticcurve.Point( curve_secp256k1, _Gx, _Gy, _r )
oid_secp256k1 = (1,3,132,0,10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1, generator_secp256k1, oid_secp256k1) 

# stretch key
master_public_key = "f455f6d61bb0d4092c1618a43be487d96e23d4c53fad01df10d68fe17af0ddac620a736ca2cf0e7008c6dc5a1f13264e49785c997bb4921d5cd2e63c5bf94437"

Hash = lambda x: hashlib.sha256(hashlib.sha256(x).digest()).digest()
def get_sequence(n, for_change):
    return ecdsa.util.string_to_number( Hash( "%d:%d:"%(n,for_change) + master_public_key.decode('hex') ) )

def generate_address(n):
    # get_new_address
    for_change = False
    z = get_sequence(n, for_change)
    dec_mpk = master_public_key.decode("hex")
    # verifykey from_string
    order = SECP256k1.order
    assert len(dec_mpk) == SECP256k1.verifying_key_length
    xs = dec_mpk[:SECP256k1.baselen]
    ys = dec_mpk[SECP256k1.baselen:]
    assert len(xs) == SECP256k1.baselen
    assert len(ys) == SECP256k1.baselen
    def string_to_number(string):
        import binascii
        return int(binascii.hexlify(string), 16)
    x = string_to_number(xs)
    y = string_to_number(ys)
    mpk = ecdsa.VerifyingKey.from_string( master_public_key.decode('hex'), curve = SECP256k1 )
    mpk_pubkey_point = Point(SECP256k1.curve, x, y, order)
    pubkey_point = mpk_pubkey_point + z*SECP256k1.generator
    public_key2 = ecdsa.VerifyingKey.from_public_point( pubkey_point, curve = SECP256k1 )
    address = bitcoin.public_key_to_bc_address( '04'.decode('hex') + public_key2.to_string() )
    return address

if __name__ == "__main__":
    for i in range(10):
        print generate_address(i)

