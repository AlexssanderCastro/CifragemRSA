# RSA Manual em Python (com HTML/CSS)

Este projeto implementa manualmente o ciclo completo do RSA sem usar bibliotecas prontas de criptografia.

## Objetivo

Demonstrar, de forma didatica, os fundamentos matematicos da criptografia assimetrica:

- escolha de numeros primos `p` e `q`
- calculo de `n = p * q`
- calculo de `phi(n) = (p - 1)(q - 1)`
- escolha do expoente publico `e`
- calculo do expoente privado `d` com Euclides estendido
- cifragem com chave publica
- decifragem com chave privada

## Fundamentacao Matematica

### 1) Numeros primos

Um numero primo e um inteiro maior que 1 que possui exatamente dois divisores positivos: `1` e ele mesmo.

Exemplos: `2, 3, 5, 7, 11, 13...`

No RSA, escolhemos dois primos distintos `p` e `q`.

Por que primos?

- A estrutura de `n = p * q` permite construir uma funcao facil de calcular em um sentido (cifrar) e dificil de inverter sem a chave (decifrar sem conhecer os fatores de `n`).
- Conhecendo `p` e `q`, conseguimos calcular `phi(n)`, que e essencial para montar a chave privada.

No projeto, os primos podem ser:

- informados manualmente pelo usuario
- gerados automaticamente com teste de primalidade de Miller-Rabin

### 2) Aritmetica modular

Aritmetica modular trabalha com restos de divisao.

Notacao:

`a ≡ b (mod n)` significa que `a` e `b` deixam o mesmo resto quando divididos por `n`.

Exemplo:

`17 ≡ 5 (mod 12)` porque ambos deixam resto `5` na divisao por `12`.

No RSA, usamos principalmente exponenciacao modular:

- cifragem: `c = m^e mod n`
- decifragem: `m = c^d mod n`

Isso permite operar com numeros grandes de forma eficiente e segura.

### 3) Totiente de Euler

A funcao totiente `phi(n)` conta quantos inteiros entre `1` e `n` sao coprimos com `n`.

Quando `n = p * q` com `p` e `q` primos distintos:

`phi(n) = (p - 1)(q - 1)`

Esse valor e usado para relacionar `e` e `d`.

### 4) Escolha de `e` (chave publica)

Escolhemos `e` tal que:

- `1 < e < phi(n)`
- `gcd(e, phi(n)) = 1`

Ou seja, `e` precisa ser coprimo com `phi(n)`.

No codigo, tenta-se usar `65537` (padrao comum) e, se nao for valido, busca-se outro impar coprimo.

### 5) Calculo de `d` (chave privada)

`d` e o inverso modular de `e` em relacao a `phi(n)`:

`d * e ≡ 1 (mod phi(n))`

Para encontrar `d`, o projeto usa o algoritmo de Euclides estendido.

## Como o RSA funciona no projeto

### Geracao de chaves

1. Escolher `p` e `q` (manual ou automatico).
2. Calcular `n = p * q`.
3. Calcular `phi(n) = (p - 1)(q - 1)`.
4. Escolher `e` coprimo com `phi(n)`.
5. Calcular `d` como inverso modular de `e` modulo `phi(n)`.

Resultado:

- chave publica: `(e, n)`
- chave privada: `(d, n)`

### Cifragem

Para cada byte da mensagem (`m`):

`c = m^e mod n`

O texto cifrado e armazenado como blocos inteiros separados por espaco.

### Decifragem

Para cada bloco cifrado (`c`):

`m = c^d mod n`

Os bytes recuperados sao convertidos novamente para UTF-8, reconstruindo o texto original.

## Estrutura do projeto

- `rsa_core.py`: logica matematica do RSA
- `app.py`: servidor HTTP e API (`/api/generate`, `/api/encrypt`, `/api/decrypt`)
- `static/index.html`: interface web
- `static/style.css`: estilo da interface
- `static/app.js`: integracao frontend com backend

## Como executar

1. Abra o terminal na pasta do projeto.
2. Execute:

```bash
python app.py
```

3. Abra no navegador:

```text
http://127.0.0.1:8000
```