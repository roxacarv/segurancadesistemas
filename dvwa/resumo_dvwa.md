# DVWA - Resumo Final

## Brute Force
- **Problema Geral**: A aplicação tenta se proteger contra ataques de força bruta usando um token CSRF para dificultar automação, mas o fluxo permite obter tokens válidos sem muita dificuldade.
- **Como foi quebrado**: Foi criado um script em Python que faz um GET para capturar o token atualizado e depois envia um POST com tentativa de login usando esse token válido. O sucesso é identificado pela presença de um texto específico na resposta, contornando a troca constante de token.
- **Solução**: Implementar bloqueio temporário após várias tentativas falhas e aplicar rate limiting por IP.
- **Detalhes**: [Brute Force](bruteforce/brute.md)

## Command Injection
- **Problema Geral**: A aplicação recebe um IP do usuário e repassa direto para o shell do sistema, usando uma blacklist incompleta para tentar impedir abusos.
- **Como foi quebrado**: Inserindo comandos adicionais como `|| whoami`, foi possível contornar o filtro e executar comandos arbitrários no sistema.
- **Solução**: Utilizar whitelist (validando estritamente o formato de IP) ou evitar chamadas ao shell, usando bibliotecas nativas.
- **Detalhes**: [Command Injection](command_injection/command_injection.md)

## CSRF
- **Problema Geral**: O token CSRF é gerado corretamente, mas fica exposto e pode ser reutilizado em requisições inseguras.
- **Como foi quebrado**: Um script consegue obter o token válido e reutilizá-lo para forjar requisições, já que não há validação adequada de origem.
- **Solução**: Exigir senha atual para ações críticas, validar cabeçalhos como Origin/Referer e reduzir a validade dos tokens.
- **Detalhes**: [CSRF](csrf/csrf.md)

## File Inclusion e File Upload
- **Problema Geral**: A aplicação valida apenas a extensão do arquivo e faz verificações superficiais no include de arquivos.
- **Como foi quebrado**: Foi feito upload de uma imagem com código PHP embutido, depois executado via File Inclusion usando `file://`.
- **Solução**: Bloquear execução no diretório de upload e validar conteúdo de forma segura. Também restringir caminhos de inclusão.
- **Detalhes**: [File Inclusion e File Upload](file_inclusion_upload/file_inclusion_upload.md)

## Insecure CAPTCHA
- **Problema Geral**: O CAPTCHA possui lógica de bypass deixada no código.
- **Como foi quebrado**: Alterando parâmetros da requisição, foi possível acionar um modo de validação falso.
- **Solução**: Remover qualquer lógica de debug e validar CAPTCHA apenas via servidor externo oficial.
- **Detalhes**: [Insecure CAPTCHA](recaptcha/recaptcha.md)

## SQL Injection e SQL Injection (Blind)
- **Problema Geral**: Dados controlados pelo usuário chegam diretamente às queries SQL sem proteção.
- **Como foi quebrado**: Injeção direta em variáveis de sessão/cookies. No modo blind, a extração foi feita analisando respostas da aplicação.
- **Solução**: Usar sempre prepared statements e tratar qualquer input como não confiável.
- **Detalhes**: [SQL Injection e Blind](sql_injection_and_blind/sql_injection_and_blind.md)

## Weak Session IDs
- **Problema Geral**: IDs de sessão previsíveis baseados em lógica fraca.
- **Como foi quebrado**: Foi possível prever sessões futuras analisando padrões e sequência dos IDs.
- **Solução**: Utilizar geradores criptograficamente seguros fornecidos pela linguagem.
- **Detalhes**: [Weak Session IDs](weak_session_ids/weak_session_ids.md)

## XSS (DOM)
- **Problema Geral**: O DOM é manipulado com base em dados da URL sem validação.
- **Como foi quebrado**: Inserindo payloads na URL, o navegador executa código malicioso diretamente no DOM.
- **Solução**: Escapar corretamente os dados e tratar como texto ao invés de HTML.
- **Detalhes**: [XSS (DOM)](xss/dom/xss_dom.md)

## XSS (Reflected)
- **Problema Geral**: Entradas do usuário são refletidas diretamente na resposta HTML.
- **Como foi quebrado**: Uso de vetores alternativos como SVG e eventos HTML para contornar filtros básicos.
- **Solução**: Escapar toda saída e aplicar encoding consistente.
- **Detalhes**: [XSS (Reflected)](xss/reflected/xss_reflected.md)

## XSS (Stored)
- **Problema Geral**: Dados maliciosos são armazenados e exibidos posteriormente sem sanitização.
- **Como foi quebrado**: Manipulando requisições, foi possível salvar código malicioso que executa ao ser exibido.
- **Solução**: Validar no backend e escapar sempre na saída.
- **Detalhes**: [XSS (Stored)](xss/stored/xss_stored.md)

## CSP Bypass
- **Problema Geral**: A CSP permite execução de scripts locais inseguros.
- **Como foi quebrado**: Uso de endpoints vulneráveis (como JSONP) para executar código mesmo com CSP ativa.
- **Solução**: Definir CSP mais restritiva e remover endpoints inseguros.
- **Detalhes**: [CSP Bypass](csp_bypass/csp_bypass.md)

## JavaScript
- **Problema Geral**: Lógica crítica foi implementada no frontend.
- **Como foi quebrado**: O código JS foi analisado e replicado, permitindo gerar valores válidos.
- **Solução**: Nunca confiar no cliente. Mover validações críticas para o backend.
- **Detalhes**: [JavaScript](javascript/javascript.md)
