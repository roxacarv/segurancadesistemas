# Buffer Overflow - Relatório Completo de Exploração (Ambiente de Laboratório)

## Ambiente utilizado nos estudos
- Kali Linux rodando no VirtualBox: isolamento de ambiente do host
- GDB: para debug de forma mais detalhada
- GCC: compilação do programa escrito em C

## 1. Código vulnerável utilizado

O programa que usei foi o seguinte:

```c
#include <stdio.h>
#include <string.h>

void vulnerable(char *input) {
    char buffer[64];
    strcpy(buffer, input);
}

int main(int argc, char *argv[]) {
    if(argc < 2) {
        printf("Uso: %s <input>\n", argv[0]);
        return 1;
    }

    vulnerable(argv[1]);
    printf("Programa finalizado.\n");
    return 0;
}
```

---

## 2. Por que o código é vulnerável

A vulnerabilidade ocorre devido ao uso de `strcpy`, que não realiza verificação de tamanho da entrada.

### Problema central

- O buffer possui tamanho fixo de 64 bytes
- A entrada do usuário pode ser arbitrariamente maior
- `strcpy` copia até encontrar `\0`, sem limites

Isso permite:

- sobrescrita de memória adjacente ao buffer
- corrupção do stack frame
- alteração do fluxo de execução

---

## 3. Compilação do binário para ambiente de teste

De forma a facilitar os testes, compilei o binário com as seguintes flags:

```bash
gcc -g -fno-stack-protector -z execstack -no-pie vuln.c -o vuln
```

### Efeito das flags

- `-g`: adiciona símbolos de debug
- `-fno-stack-protector`: remove canários de stack
- `-z execstack`: permite execução em stack (não essencial aqui)
- `-no-pie`: evita randomização do binário principal

---

## 4. Primeiros testes e comportamento observado

### Teste inicial

Entrada:

```bash
./vuln $(python3 -c "print('A'*100)")
```

Resultado:

- segmentation fault
- sem controle direto de RIP

Conclusão inicial incorreta:

> achei que 64 + 8 bytes seriam suficientes para alcançar RIP

---

## 5. Uso de GDB para análise

Pra tornar a análise mais fácil, utilizei o GDB me focando em:

- registradores
- stack
- frame da função

Exemplo:

```gdb
info registers
x/80gx $rsp
```

Observações importantes:

- a stack continha padrões de entrada
- o buffer estava sendo sobrescrito
- RIP ainda não era controlado inicialmente <- esse foi a maior dificuldade

---

## 6. Uso de cyclic pattern para identificar offset

Utilizei o padrão cíclico para análise de offset:

```python
from pwn import *
print(cyclic(200))
```

E posteriormente:

```python
cyclic_find(valor)
```

### Problema encontrado

Inicialmente houve confusão entre:

- interpretação de 32-bit
- interpretação de 64-bit

Isso levou a valores incorretos de offset no início da análise.

---

## 7. Correção da estratégia

Após análise detalhada da stack no GDB:

- observei que o RIP estava sendo sobrescrito parcialmente
- valores do cyclic apareciam na memória da stack

Assim finalmente idenfiquei o stack correto:

> 70 bytes

---

## 8. Confirmação do controle de RIP

Após ajuste do payload:

```bash
python3 -c "print('A'*70 + 'BBBBBBBB')"
```

Resultado no GDB:

```
rip = 0x424242424242
```

### Interpretação

- o valor 0x42 corresponde a "B"
- o RIP foi sobrescrito com sucesso
- controle de fluxo foi alcançado

---

## 9. Erros e mudanças de estratégia durante análise

### Erro 1: suposição de offset fixo

Pensei que inicialmente o layout seria:

```
64 bytes buffer + 8 bytes saved rbp = 72 bytes
```

Isso não se confirmou devido a:

- padding de stack
- alinhamento da ABI

---

### Erro 2: interpretação incorreta de cyclic (64-bit)

Houve inconsistência no valor do RIP entre 32 e 64-bits, o que causou cálculos incorretos de offset.

---

### Ajuste de estratégia

- análise direta da stack no GDB
- validação empírica do overwrite
- uso do valor real observado no RIP

---

## 10. Resultado final da exploração

O experimento demonstrou:

- presença de buffer overflow clássico
- possibilidade de sobrescrita de RIP
- controle de fluxo da execução

---

## 11. Como tornar o código seguro

### Problema principal

Uso de `strcpy` sem verificação de tamanho.

---

### Soluções recomendadas

#### 1. Substituir strcpy por strncpy

```c
strncpy(buffer, input, sizeof(buffer) - 1);
buffer[63] = '\0';
```

---

#### 2. Usar funções seguras padrão

- `snprintf`
- `strlcpy`

---

#### 3. Validação de entrada

- limitar tamanho máximo de entrada
- rejeitar entradas acima do limite

---

#### 4. Proteções de compilação (defensivo)

- Stack canaries (`-fstack-protector-strong`)
- ASLR habilitado
- PIE habilitado
- NX stack

---

## 12. Conclusão

Este exercício demonstrou um buffer overflow clássico em ambiente controlado, passando por:

- identificação da vulnerabilidade
- análise com GDB
- uso de padrões cíclicos
- correção de offset
- confirmação de controle de RIP

O aprendizado principal é que buffer overflow não depende apenas de overflow em si, mas da estrutura real da stack, otimizações do compilador e alinhamento da ABI.
