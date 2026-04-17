# DVWA - XSS Stored (High) — Diário de Execução

## Contexto

O objetivo foi explorar a vulnerabilidade de Cross-Site Scripting Stored (XSS Stored) no nível HIGH do DVWA.

Diferente do Reflected, aqui o payload é armazenado no servidor (banco de dados) e executado sempre que a página é carregada.

---

## Funcionamento da aplicação

A aplicação permite inserir dados em um formulário (ex: nome e mensagem).

Esses dados são:

1. Enviados ao servidor
2. Armazenados no banco
3. Renderizados posteriormente na página

---

## Proteções no nível HIGH

O sistema tenta:

- filtrar caracteres perigosos
- limitar tamanho de input (apenas no client-side)
- aplicar sanitização parcial

---

### Campo name (vulnerável)

Problemas:

- tenta bloquear apenas a palavra "script"
- não remove outras tags HTML
- não impede uso de eventos (onerror, onload)

---

## Exploração

### Payload funcional

```html
<img src=x onerror=alert(1)>
```

---

## Limitação client-side

O campo "name" possui:

```html
maxlength="10"
```

Isso impediria inserir payloads maiores diretamente pelo navegador.

---

## Bypass da limitação

### Método 1: Alteração no HTML

1. Inspecionar elemento
2. Alterar:

```html
maxlength="10"
```

para:

```html
maxlength="60"
```

3. Inserir payload completo

---

### Método 2: Interceptação com Burp Suite

Fluxo:

1. Ativar intercept no Burp
2. Submeter formulário no DVWA
3. Interceptar requisição POST:

```http
POST /vulnerabilities/xss_s/ HTTP/1.1

txtName=test&mtxMessage=hello&btnSign=Sign+Guestbook
```

4. Alterar parâmetro:

```http
txtName=<img src=x onerror=alert(1)>
```

5. Forward da requisição

---

## Resultado

- payload aceito pelo servidor
- armazenado no banco
- executado ao carregar a página

---

## Prova de persistência

- não é necessário reenviar o payload
- qualquer usuário que acessar executa o script

---

## Prova de impacto

```html
<img src=x onerror="document.body.innerHTML='OWNED'">
```

Resultado:

```
OWNED
```

---

## Conclusão técnica

A vulnerabilidade ocorre porque:

- o campo "name" possui sanitização incompleta
- a validação de tamanho é apenas client-side
- o servidor confia no input do usuário

---

## Impacto

- execução persistente de JavaScript
- afeta todos os usuários
- possibilidade de roubo de sessão
- manipulação completa da página

---

## Conclusão final

Mesmo no nível HIGH, a aplicação permanece vulnerável devido a:

- filtragem inadequada baseada em blacklist
- ausência de validação no servidor
- confiança em restrições do lado do cliente

Isso permite a exploração completa de XSS Stored com persistência.
