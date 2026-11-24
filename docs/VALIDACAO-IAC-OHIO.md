# Validação do ciclo CloudFormation e S3 em Ohio

**Data** 24/11/2026 · **Região** `us-east-2` · **Estado** Ciclo verificado e aceito pelo proprietário.

## Verificação antes da criação

- A API do Free Tier retornou `FREE` e `ACTIVE`, com saldo positivo de créditos. A AWS lista CloudFormation, CloudShell e S3 entre os serviços disponíveis no Free Tier de projetos. O CloudFormation não cobra tarifa adicional para o provedor nativo `AWS::*`. [Plano gratuito](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html) · [Serviços disponíveis](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html) · [Preço do CloudFormation](https://aws.amazon.com/cloudformation/pricing/)
- A CLI validou o [template publicado](https://github.com/raphaelguterres/cloud-security-detection-lab/blob/288a42b64fb2404f0ba23424847120a418b6b6ba/infra/bucket-evidencias.json). SHA-256 `9f6e78034c596c7bac1b552c2d822622477ee18bd4c80f16f7546dac5ea21814`. O inventário regional inicial retornou zero buckets.
- O ensaio usou o corpo do template diretamente na API do CloudFormation. A stack declarou um único bucket. Nenhum objeto foi enviado e o plano permaneceu gratuito.

## Evidência observada

| Recurso | Criação registrada em UTC | Remoção registrada em UTC |
| --- | --- | --- |
| `AWS::CloudFormation::Stack` | `CREATE_COMPLETE` às 20:53:13.551 | `DELETE_COMPLETE` às 20:53:37.542 |
| `BucketEvidencias` · `AWS::S3::Bucket` | `CREATE_COMPLETE` às 20:53:12.923 | `DELETE_COMPLETE` às 20:53:37.240 |

A saída `BucketName` correspondeu ao identificador físico de `BucketEvidencias` durante a criação. Uma checagem intermediária de propriedades do bucket terminou sem resultado individual conclusivo e acionou a limpeza programada. Em uma conferência independente iniciada às **20:54:36 UTC**, `DescribeStackEvents` confirmou os quatro estados da tabela e a igualdade do identificador físico do bucket nos dois eventos. A listagem regional do S3 retornou **zero correspondências para esse mesmo bucket** após a remoção.

As proteções de acesso público, criptografia e propriedade dos objetos constam no template. A verificação em execução dessas propriedades fica pendente. Os identificadores físicos e as respostas brutas foram omitidos do registro público.

## Custo observado

Após o encerramento, a API voltou a retornar `FREE` e `ACTIVE`, com saldo de créditos igual ao da linha de base. O painel AWS Settings mostrou **US$ 0,00** na conferência imediata. Essa leitura registra o valor exibido no momento do ensaio. A conferência após a consolidação do faturamento permanece no critério de custo do M4. [Como conferir a fatura](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/getting-viewing-bill.html)

## Aceite

- [x] Em 24/11/2026, o proprietário aceitou a evidência de criação e remoção da stack e do mesmo bucket em Ohio, incluindo a verificação cruzada do inventário S3 e as limitações registradas.
