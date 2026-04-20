# Comunicação entre Frames e Same-Origin Policy (SOP)

## 1. Objetivo do experimento

Neste experimento, eu implementei uma comunicação bidirecional entre dois frames HTML, seguindo as seguintes restrições:

- O Frame 1 contém todo o código JavaScript da aplicação
- O Frame 2 não contém lógica JavaScript
- Cada frame possui um textarea e um botão
- A comunicação entre os frames ocorre via acesso direto ao DOM

O objetivo também foi observar na prática o comportamento do Same-Origin Policy (SOP) durante essa interação.

---

## 2. Estrutura da aplicação

Eu organizei a aplicação da seguinte forma:

- index.html: responsável por carregar dois frames lado a lado
- frame1.html: centraliza toda a lógica JavaScript
- frame2.html: contém apenas interface HTML

Cada frame possui:

- um elemento textarea
- um botão para disparar ações

---

## 3. Comportamento inicial (execução via file://)

Ao executar os arquivos diretamente pelo sistema de arquivos (protocolo file://), eu observei que o navegador bloqueia a comunicação entre os frames.

### Erro observado

```
Uncaught DOMException: Permission denied to access property
```

Esse comportamento ocorre porque o navegador trata cada arquivo como uma origem distinta, mesmo estando no mesmo diretório local.

---

## 4. Ambiente de teste controlado

Para conseguir executar o experimento corretamente, eu utilizei um ambiente local controlado, ajustando a configuração de segurança para permitir acesso a arquivos locais.

Com isso, foi possível:

- Compartilhar o contexto entre os frames
- Acessar o DOM de um frame a partir do outro usando parent.frames
- Executar funções definidas no Frame 1 a partir do Frame 2

---

## 5. Implementação da comunicação

### Frame 1 (controle central)

Eu centralizei toda a lógica JavaScript neste frame:

```javascript
function enviarParaFrame2() {
    const texto = document.getElementById("t1").value;
    parent.frames["frame2"].document.getElementById("t2").value = texto;
}

function receberDoFrame2() {
    const texto = parent.frames["frame2"].document.getElementById("t2").value;
    document.getElementById("t1").value = texto;
}
```

---

### Frame 2 (interface sem lógica)

No Frame 2, eu apenas utilizei chamadas para funções definidas no Frame 1:

```html
<button onclick="parent.frames['frame1'].receberDoFrame2()">
Enviar para Frame 1
</button>
```

---

## 6. Resultado do experimento

Com o ambiente configurado, eu observei que:

- A comunicação entre frames funcionou corretamente
- O Frame 2 conseguiu acionar funções definidas no Frame 1
- O Frame 1 manteve controle total da lógica da aplicação

---

## 7. Same-Origin Policy (SOP)

O Same-Origin Policy é um mecanismo de segurança dos navegadores que impede que diferentes origens interajam livremente.

Ele bloqueia:

- acesso ao DOM entre frames de origens diferentes
- execução de funções entre contextos não confiáveis
- manipulação de dados entre páginas distintas

---

## 8. Comportamento em navegadores modernos

Eu observei que, em navegadores modernos:

- Frames só podem interagir diretamente se compartilharem o mesmo origin
- Protocolos diferentes (file, http, https) podem ser tratados como origens diferentes
- O acesso direto entre frames é bloqueado quando há violação de origem

---

## 9. Abordagem moderna recomendada

Em aplicações reais, a comunicação entre frames deve ser feita utilizando a API:

### postMessage

Essa API permite comunicação segura entre contextos isolados:

```javascript
window.postMessage({ texto: "dados" }, "*");
```

Vantagens:

- Funciona entre diferentes origens
- Não expõe diretamente o DOM
- Permite comunicação controlada e segura

---

## 10. Conclusão

Neste experimento, eu consegui observar na prática:

- Como funciona a comunicação entre frames em um ambiente controlado
- Como o Same-Origin Policy limita esse tipo de interação
- A importância de executar aplicações em um mesmo origin para comunicação direta
- A necessidade de usar mecanismos modernos como postMessage em aplicações reais

Esse comportamento demonstra como a web moderna prioriza isolamento e segurança entre origens para evitar ataques e vazamento de informações.
