# DVWA - Command Injection (High) — Diário de Estudos

## Contexto

O objetivo foi explorar a vulnerabilidade de Command Injection no DVWA em nível HIGH, identificando como a filtragem funciona e como contorná-la.

---

## Observação inicial

A aplicação recebe um IP e executa internamente um comando semelhante a:

ping -c 4 <ip>

Isso indica que qualquer entrada fornecida pode ser interpretada diretamente pelo shell.

---

## Testes iniciais

Primeiro validei o comportamento normal:

127.0.0.1

O sistema retornou o resultado esperado do ping.

---

## Tentativa de injeção

Em seguida testei:

127.0.0.1 || whoami

Resultado:

www-data

Isso confirmou que o comando adicional foi executado, caracterizando a vulnerabilidade.

---

## Análise do código fonte

O código relevante:

$target = trim($_REQUEST['ip']);

$substitutions = array(
    '&'  => '',
    ';'  => '',
    '| ' => '',
    '-'  => '',
    '$'  => '',
    '('  => '',
    ')'  => '',
    '`'  => '',
    '||' => '',
);

$target = str_replace(array_keys($substitutions), $substitutions, $target);

$cmd = shell_exec('ping -c 4 ' . $target);

---

## Análise da proteção

A proteção utiliza:

- trim() para remover espaços nas extremidades
- str_replace() como blacklist

Problemas identificados:

1. trim() não remove espaços internos
2. A blacklist depende de padrões exatos
3. Não há validação real do formato da entrada
4. O shell ainda interpreta a string resultante

---

## Motivo do bypass

Mesmo com a tentativa de remover '||', a filtragem é frágil:

- A substituição não considera contexto
- Pequenas variações de espaçamento podem alterar o resultado final
- O shell interpreta os comandos mesmo após modificações parciais

O payload utilizado:

127.0.0.1 || whoami

Permitiu a execução de comando adicional após o ping.

---

## Testes adicionais

Realizei variações para validar o comportamento:

127.0.0.1||whoami -- cobre essa possibilidade
127.0.0.1 ||    whoami -- não cobre essa possibilidade
127.0.0.1 | whoami -- cobre essa possibilidade 

Esses testes demonstraram que a filtragem não cobre todas as possibilidades.

---

## Conclusão

A aplicação continua vulnerável mesmo em nível HIGH devido a:

- Uso de blacklist incompleta
- Falta de validação adequada de entrada
- Confiança excessiva em funções como trim()

O comportamento do shell permite interpretar a entrada de forma não prevista pelo desenvolvedor, possibilitando a execução de comandos arbitrários.

---

## Observação final

Uma possível abordagem para tornar mais seguro, seria validar a entrada utilizando whitelist, aceitando apenas IPs válidos, em vez de tentar remover padrões perigosos.
