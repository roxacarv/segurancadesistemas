# DVWA - CSRF (High) — Diário de Execução

## Contexto

O objetivo foi explorar a vulnerabilidade de Cross-Site Request Forgery (CSRF) no DVWA em nível HIGH, analisando o mecanismo de proteção baseado em token e suas limitações.

---

## Observação inicial

A funcionalidade permite alterar a senha do usuário através de uma requisição HTTP contendo:

- nova senha
- confirmação
- token CSRF (user_token)

Exemplo de requisição:

/vulnerabilities/csrf/?password_new=admin&password_conf=admin&Change=Change&user_token=XXXX

---

## Análise do comportamento

Durante os testes observei que:

- a requisição utiliza método GET
- o token muda a cada requisição
- o token é incluído como parâmetro na URL
- o token está presente no HTML da página

Exemplo:

<input type="hidden" name="user_token" value="XXXXXXXX">

---

## Tentativa de ataque direto

Tentei executar o ataque diretamente via URL sem token:

/vulnerabilities/csrf/?password_new=hacked&password_conf=hacked&Change=Change

Resultado:

A requisição falhou devido à ausência do token.

---

## Reutilização de token

Em seguida:

1. capturei um token válido na página
2. reutilizei imediatamente na URL

/vulnerabilities/csrf/?password_new=hacked&password_conf=hacked&Change=Change&user_token=TOKEN

Resultado:

A senha foi alterada com sucesso.

---

## Teste com Burp Suite

Utilizei o Burp para:

1. interceptar a requisição
2. enviar para o Repeater
3. modificar os parâmetros
4. reenviar com o mesmo token

Resultado:

A requisição foi aceita enquanto o token permanecia válido.

---

## Tentativa de automação com HTML

Foi criado um arquivo HTML com iframe e JavaScript para:

- carregar a página CSRF
- capturar o token do DOM
- enviar a requisição automaticamente

No entanto, ao executar localmente (file://), ocorreu o erro:

Permission denied to access property "document" on cross-origin object

---

## Análise da limitação

O erro ocorreu devido à Same-Origin Policy:

- file:// e http://localhost são origens diferentes
- o navegador bloqueia acesso ao DOM de outra origem

---

## Ajuste do ambiente

Para contornar isso, servi o arquivo via HTTP ou dentro do próprio DVWA, garantindo mesma origem:

http://localhost:8080/attack.html

Resultado:

Foi possível acessar o DOM do iframe e capturar o token.

---

## Automação via script

Implementei um script em Python que:

1. acessa a página CSRF
2. extrai o token com BeautifulSoup
3. envia a requisição com token válido

Fluxo:

GET /csrf/ > extrai token > envia requisição

Resultado:

A senha foi alterada automaticamente.

---

## Análise da proteção

A aplicação utiliza:

- token anti-CSRF dinâmico

Problemas identificados:

1. token exposto no HTML
2. ausência de validação de origem (Referer/Origin)
3. uso de método GET
4. token reutilizável dentro da sessão

---

## Conclusão

Apesar da implementação de token anti-CSRF, a aplicação permanece vulnerável quando o atacante consegue obter um token válido.

O ataque não consiste em quebrar o token, mas em reproduzir o fluxo legítimo da aplicação utilizando um token válido.

---

## Observação final

Em cenários reais, esse tipo de ataque normalmente depende da combinação com outras vulnerabilidades, como XSS, para permitir a captura do token dentro do contexto da aplicação.
