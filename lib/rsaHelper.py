# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/7/15
@Software: PyCharm
@disc:
======================================="""
import rsa
def generate_public_key(private_key_byte: bytes):
    """
    从私钥反推公钥
    """
    priv_key = rsa.PrivateKey.load_pkcs1(private_key_byte)
    # 构造公钥
    public_key = rsa.PublicKey(priv_key.n, priv_key.e)
    # 验证公钥是否匹配
    msg = b'hello'
    priv_sig = rsa.sign(msg, priv_key, 'SHA-1')
    pub_verify = rsa.verify(msg, priv_sig, public_key)
    print(pub_verify)
    return public_key
