# DVWA - Brute Force (High) - Diário de Estudo

## Contexto

O objetivo era explorar o módulo de **Brute Force** do DVWA no nível **HIGH**, entendendo como a proteção funciona e como contorná-la.

Inicialmente, a ideia era usar o Burp Suite para interceptar requisições e tentar automatizar o ataque com Intruder, mas o comportamento do sistema exigiu uma abordagem mais cuidadosa.

---

## Configuração inicial

- DVWA rodando em Docker (`localhost:8080`)
- Burp Suite configurado como proxy (`127.0.0.1:8081`)
- Firefox usando FoxyProxy

Um dos primeiros problemas foi que o Firefox não enviava requisições locais (`localhost`) para o Burp. Isso foi resolvido alterando a configuração:

about:config > network.proxy.allow_hijacking_localhost = true

Depois disso, o Burp começou a interceptar corretamente.

---

## Primeiras tentativas com Burp

Interceptando a requisição de login, identificamos:

/vulnerabilities/brute/?username=...&password=...&Login=Login&user_token=...

Ou seja:
- Método GET
- Token CSRF (`user_token`)
- Parâmetros claros

Inicialmente, parecia possível fazer brute force direto, mas o token começou a causar problemas.

---

## Análise do token

Durante os testes, observei comportamentos diferentes:

- Em alguns momentos o token parecia fixo
- Depois percebi que **ele muda a cada requisição**
- Cada tentativa exige um token novo válido

Conclusão:
O sistema implementa proteção contra automação via token dinâmico.

---

## Problema com Intruder

Ao usar o Intruder:

- O mesmo token era reutilizado
- O sistema rejeitava as requisições
- O ataque não funcionava

Isso mostrou que:
Não basta repetir requisições — é necessário reproduzir o fluxo completo da aplicação.

---

## Mudança de abordagem:

Criei um script em Python:

- requests
- BeautifulSoup (bs4)

Fluxo implementado:

1. GET /brute/ > extrai user_token
2. GET login com username + senha + token
3. analisar resposta
4. repetir

---

## Problemas encontrados no script

### 1. Detecção baseada em texto

Inicialmente:
if "Username and/or password incorrect" not in r.text:

Funcionava, mas era frágil pois dependia exclusivamente do body retornar algo no DOM.

---

### 2. Tentativa de usar status e length

Foi implementado:

- comparação de status_code
- comparação de len(r.text)

Mas no nível HIGH:

- status quase sempre 200
- tamanho da resposta muito similar

Resultado:
Não era confiável usar apenas esses critérios.

---

### 3. Confusão com redirects

Tentei usar allow_redirects=False

Isso gerou:

- respostas 302
- length = 0

No entanto o sistema só redireciona quando o token é inválido.

---

## Solução final

O critério mais confiável:

"Welcome to the password protected area" in r.text

---

## Melhorias implementadas

- baseline de resposta inválida
- comparação de tamanho
- comparação de status: nesse caso, se compara status com intuito de evitar bad requests, pois os status de senha válida e inválida são sempre 200

---

## Resultado final

O script consegue:

- Obter token dinâmico
- Manter sessão válida
- Automatizar o brute force
- Detectar corretamente o sucesso

---

## Conclusão

O nível HIGH não impede brute force completamente, mas:

- adiciona complexidade com tokens
- exige entender o fluxo da aplicação
- exige análise de resposta mais cuidadosa

O ponto principal:
O sistema não muda status ou estrutura, apenas o conteúdo.

---

## Observação final

- Ferramentas ajudam, mas não resolvem tudo
- Entender o comportamento da aplicação é essencial
- Pequenos detalhes mudam completamente a estratégia
