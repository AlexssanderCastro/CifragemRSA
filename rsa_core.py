import random
from math import gcd


_rng = random.SystemRandom()


def euclides_estendido(a: int, b: int):
    """Return (g, x, y) such that ax + by = g = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    # Relacao recursiva para obter os coeficientes de Bezout.
    g, x1, y1 = euclides_estendido(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def inverso_modular(a: int, m: int) -> int:
    g, x, _ = euclides_estendido(a, m)
    if g != 1:
        raise ValueError("Nao existe inverso modular para os valores informados.")
    return x % m


def eh_primo_provavel(n: int, rounds: int = 12) -> bool:
    """Miller-Rabin primality test (probabilistic)."""
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False

    # Decompoe n - 1 em d * 2^s, com d impar.
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(rounds):
        a = _rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite_witness = True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite_witness = False
                break
        if composite_witness:
            return False
    return True


def gerar_primo(bits: int) -> int:
    if bits < 8:
        raise ValueError("Use pelo menos 8 bits por primo para demonstracao didatica.")
    while True:
        candidate = _rng.getrandbits(bits)
        # Force odd and force top bit to keep target size.
        candidate |= (1 << (bits - 1)) | 1
        if eh_primo_provavel(candidate):
            return candidate
def escolher_expoente_publico(phi: int) -> int:
    preferred = 65537
    if gcd(preferred, phi) == 1:
        return preferred

    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            return e
        e += 2
    raise ValueError("Nao foi possivel encontrar expoente publico valido.")


def montar_chaves(p: int, q: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = escolher_expoente_publico(phi)
    # d e o inverso modular de e em modulo phi(n).
    d = inverso_modular(e, phi)

    return {
        "p": p,
        "q": q,
        "n": n,
        "phi": phi,
        "e": e,
        "d": d,
        "public_key": {"e": e, "n": n},
        "private_key": {"d": d, "n": n},
    }


def gerar_chaves_automatico(bits_por_primo: int = 16):
    p = gerar_primo(bits_por_primo)
    q = gerar_primo(bits_por_primo)
    while q == p:
        q = gerar_primo(bits_por_primo)
    return montar_chaves(p, q)


def gerar_chaves_com_primos(p: int, q: int):
    if p == q:
        raise ValueError("p e q devem ser primos distintos.")
    if p < 257 or q < 257:
        raise ValueError("Use primos maiores que 256 para suportar bytes UTF-8 no exemplo.")
    if not eh_primo_provavel(p):
        raise ValueError("O valor informado para p nao e primo.")
    if not eh_primo_provavel(q):
        raise ValueError("O valor informado para q nao e primo.")
    return montar_chaves(p, q)


def cifrar_mensagem(message: str, e: int, n: int):
    if n <= 255:
        raise ValueError("n muito pequeno. Gere chaves maiores para suportar bytes de texto.")

    plaintext_bytes = message.encode("utf-8")
    ciphertext = [pow(byte, e, n) for byte in plaintext_bytes]
    return ciphertext


def decifrar_mensagem(ciphertext, d: int, n: int) -> str:
    plain_bytes = bytes([pow(int(block), d, n) for block in ciphertext])
    return plain_bytes.decode("utf-8")


def texto_para_blocos(ciphertext_text: str):
    cleaned = ciphertext_text.replace(";", " ").replace(",", " ").strip()
    if not cleaned:
        return []
    parts = cleaned.split()
    return [int(part) for part in parts]


def blocos_para_texto(ciphertext_blocks):
    return " ".join(str(block) for block in ciphertext_blocks)


# Alias para manter compatibilidade com nomes antigos.
extended_gcd = euclides_estendido
mod_inverse = inverso_modular
is_probable_prime = eh_primo_provavel
choose_public_exponent = escolher_expoente_publico
_build_key_bundle = montar_chaves
generate_prime = gerar_primo
generate_keys = gerar_chaves_automatico
generate_keys_from_primes = gerar_chaves_com_primos
encrypt_message = cifrar_mensagem
decrypt_message = decifrar_mensagem
parse_ciphertext = texto_para_blocos
format_ciphertext = blocos_para_texto
