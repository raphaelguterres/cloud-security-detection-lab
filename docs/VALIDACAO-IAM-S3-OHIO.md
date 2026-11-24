# M4 · Validação de privilégio mínimo no S3

**Data** 24/11/2026 · **Região** Ohio (`us-east-2`) · **Estado** Teste real concluído, aguardando aceite.

## Escopo

Um bucket privado temporário criado pelo [template do laboratório](../infra/bucket-evidencias.json), um único objeto fictício e um papel temporário. O papel tinha uma única política com `s3:GetObject` no ARN exato do objeto. A confiança foi limitada ao papel operador já autorizado. O teste assumiu o papel com credenciais STS de 15 minutos, mantidas em memória. O bucket tinha os quatro controles de bloqueio de acesso público, criptografia SSE-S3 e propriedade forçada ao dono do bucket, confirmados pela API do S3.

## Resultado observado

No ensaio final, às **21:14:44 UTC**, a mesma sessão STS fez as duas chamadas sobre o mesmo objeto. A identidade foi comparada antes e depois por `GetCallerIdentity`.

| Operação | Resultado real |
| --- | --- |
| `GetObject` de controle, pelo operador | HTTP `200`, conteúdo igual ao objeto preparado |
| `GetObject`, pela sessão de teste | HTTP `200`, conteúdo igual ao original |
| `PutObject`, pela mesma sessão de teste | HTTP `403`, código `AccessDenied` |
| `GetObject` de conferência, pelo operador | Conteúdo e ETag iguais ao original após a tentativa de sobrescrita |

A leitura do papel havia recebido `AccessDenied` nas duas tentativas anteriores. No ensaio final, as avaliações consultadas no simulador retornaram `explicitDeny` para ambas as ações, enquanto as chamadas reais retornaram os resultados da tabela. A causa da divergência não foi confirmada. A evidência de aceite se baseia nas chamadas efetivas ao S3. Outros objetos e listagem pelo papel ficaram fora deste ensaio.

## Limpeza e custo

O objeto fictício, a política e o papel temporário foram removidos. `GetRole` retornou `NoSuchEntity`. O CloudFormation registrou `DELETE_COMPLETE` para a stack e o bucket, e a listagem regional confirmou a ausência do bucket. A verificação final terminou às **21:14:50 UTC**, sem erro de limpeza.

O Free Plan estava ativo antes e depois, o saldo de créditos foi igual na leitura imediata e o painel mostrou **US$ 0,00** após o teste. A conferência do faturamento consolidado faz parte do critério de custo do M4. [Plano gratuito da AWS](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html)

Este registro omite identificadores da conta, do bucket e do papel, credenciais e respostas brutas.

## Aceite

- [ ] O proprietário aceita a evidência de leitura permitida e escrita negada para a mesma sessão IAM, com a integridade do objeto e a limpeza dos recursos verificadas.
