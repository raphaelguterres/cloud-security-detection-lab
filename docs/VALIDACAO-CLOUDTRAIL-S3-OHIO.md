# Três detecções de gerenciamento do S3 em Ohio

**Data** 24/11/2026 · **Região** `us-east-2` · **Resultado** Três sinais identificados em eventos reais do laboratório.

O ensaio usou a conta AWS Free Plan do laboratório. Um bucket vazio e temporário foi criado em Ohio. Os quatro controles do S3 Block Public Access estavam ativos e a política aplicada apenas negava solicitações sem TLS. A API do S3 confirmou que a política não era pública. O bucket foi removido e a consulta final ao mesmo recurso retornou HTTP `404`. A janela foi de **22:13:31 a 22:13:38 UTC**. [Planos da AWS](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html)

## Resultado do histórico

O CloudTrail Event history retornou os três eventos de gerenciamento para a mesma conta e o mesmo bucket em Ohio, sem código de erro. A tabela mostra os resultados da execução local do detector sobre os campos sanitizados coletados no histórico. [Histórico do CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html) · [Eventos do S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging-s3-info.html)

| Horário UTC | Evento | Resultado |
| --- | --- | --- |
| 22:13:33 | `PutBucketPublicAccessBlock` | `info`. A mudança manteve os quatro bloqueios ativos. |
| 22:13:34 | `PutBucketPolicy` | `review`. Política do bucket alterada. A checagem do S3 confirmou que a política era privada. |
| 22:13:37 | `DeleteBucket` | `review`. Remoção detectada e confirmada pela checagem do recurso. |

O detector limita a entrada à conta, à região e ao nome exato do bucket. Os testes cobrem a ausência de sinal para outra conta, outro bucket, outra região, eventos de dados, erros de permissão e chamadas de leitura. O detector emite um único resultado por ID de evento. Uma flag de bloqueio explicitamente falsa produz `high` na fixture sintética. Nenhum bloqueio público foi desativado na AWS.

## Reproduzir sem acessar a AWS

```sh
python -B -m unittest discover -s detections -v
python -B detections/s3_management.py detections/fixtures/ohio-s3-management-sanitized.json --account-id 000000000000 --bucket example-ohio-bucket
```

O [JSON publicado](../detections/fixtures/ohio-s3-management-sanitized.json) é uma projeção dos eventos reais. A conta, o bucket e os IDs foram substituídos por marcadores. Políticas completas, identidades e outros campos desnecessários foram omitidos. A execução valida a detecção por leitura do histórico e processamento offline.

O plano permaneceu **FREE / ACTIVE** e os créditos permaneceram em **US$ 100,00** na consulta imediata antes e depois. A consulta ao Event history é gratuita. O ensaio não criou trilha, CloudTrail Lake, logs de dados ou recursos em produção. O faturamento consolidado segue no critério de encerramento do M4.
