# 🔓 Vulnerabilidade: Ataques JavaScript (High)

## 📄 Descrição

### Nível Alto

A aplicação utiliza JavaScript fortemente ofuscado para gerar um token de validação no lado do cliente. O objetivo é enviar a palavra **"success"**, porém a requisição exige um token válido.

O mecanismo de proteção assume que o código ofuscado não pode ser facilmente entendido ou reproduzido.

No entanto, como toda a lógica é executada no cliente, ela pode ser revertida e reproduzida externamente.

---

## 🧠 Causa Raiz

- Geração do token ocorre totalmente no **client-side**
- Uso de **ofuscação ao invés de segurança real**
- Não há **segredo no servidor**
- Token é **determinístico e previsível**

---

## 🔍 Engenharia Reversa

### Passo 1: Deofuscação

Substituir:

eval(...)

Por:

console.log(...)

Isso revela o código real.

---

### Passo 2: Funções Relevantes

function do_something(e) {
  for (var t = "", n = e.length - 1; n >= 0; n--) t += e[n];
  return t;
}

function token_part_1(a, b) {
  document.getElementById("token").value =
    do_something(document.getElementById("phrase").value);
}

function token_part_2(e = "XX") {
  document.getElementById("token").value = sha256(
    e + document.getElementById("token").value
  );
}

function token_part_3(t, y = "ZZ") {
  document.getElementById("token").value = sha256(
    document.getElementById("token").value + y
  );
}

---

## 🔄 Lógica de Geração do Token

1. Reverter a frase
2. sha256("XX" + resultado)
3. sha256(resultado + "ZZ")

Fórmula final:

token = sha256( sha256("XX" + reverse(phrase)) + "ZZ" )

---

## 💣 Exploração (Sem JavaScript)

Podemos reproduzir a lógica externamente.

---

### 🐍 Prova de Conceito em Python

import hashlib

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def generate_token(phrase: str) -> str:
    token = phrase[::-1]
    token = sha256("XX" + token)
    token = sha256(token + "ZZ")
    return token

phrase = "success"
token = generate_token(phrase)

print(token)

---

### ✅ Resultado Esperado

ec7ef8687050b6fe803867ea696734c67b541dfafb286a0b1239f42ac5b0aa84

---

## 🌐 Exploração via Burp Suite

### Passo 1: Interceptar

POST /vulnerabilities/javascript/

phrase=success&token=INVALID

---

### Passo 2: Substituir

phrase=success&token=ec7ef8687050b6fe803867ea696734c67b541dfafb286a0b1239f42ac5b0aa84

---

### Passo 3: Enviar

O servidor aceita a requisição sem executar JS.

---

## 🔥 Impacto

- Bypass total
- Token gerado offline
- Automação possível
- Ofuscação inútil

---

## ⚠️ Problema

Confiança em token client-side previsível.

---

## 🛡️ Correção

Gerar token no servidor usando HMAC:

token = HMAC(secret, phrase + session_id)

---

## 🧩 Conclusão

Ofuscação ≠ segurança.
