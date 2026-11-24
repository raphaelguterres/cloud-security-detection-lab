# Evidências do laboratório AWS · M4

Revisões documentais registradas em 24/11/2026. Os exemplos usam dados fictícios. A operação na nuvem será registrada em uma etapa própria.

| Entrega | Evidência disponível | Validação pendente |
| --- | --- | --- |
| Escopo e README | AWS Free Plan, Ohio (`us-east-2`), limite de US$ 0 em cobranças e até 100 MiB de objetos fictícios em um bucket privado. [Limites](../README.md#custo) | Reconferir plano, elegibilidade e saldo antes do ensaio. |
| Infraestrutura | O [template](../infra/bucket-evidencias.json) declara um recurso `AWS::S3::Bucket`, quatro bloqueios de acesso público, SSE-S3, propriedade de objetos pelo dono do bucket e `DeletionPolicy: Delete`. A saída `BucketName` referencia o próprio recurso. | Registrar criação e remoção da mesma stack e do mesmo bucket em Ohio. |
| IAM | A mesma sessão STS recebeu `200` em `GetObject` e `403 AccessDenied` em `PutObject`. O operador confirmou a integridade do objeto. [Evidência em Ohio](VALIDACAO-IAM-S3-OHIO.md) | Aceite do proprietário. |
| CloudTrail | O sinal `PutBucketPolicy` foi validado com entradas fictícias. | Observar eventos reais de gerenciamento e concluir três detecções. |
| Encerramento | Procedimento aceito. A referência de custo para 100 MiB por um mês, dez operações de gravação ou listagem e dez leituras foi cerca de US$ 0,0023 a preço de tabela. | Vincular a remoção da stack ao inventário do S3 e verificar custo e créditos após a atualização do faturamento. |

## Evidência do sinal no CloudTrail

A regra combina `eventCategory = Management`, `eventSource = s3.amazonaws.com`, `eventName = PutBucketPolicy`, `awsRegion = us-east-2`, o nome exato do bucket do laboratório e `errorCode` ausente ou nulo. A revisão local considerou um exemplo de correspondência e quatro controles: erro `AccessDenied`, outra região, outro bucket e evento `GetBucketPolicy`.

## Evidência esperada no encerramento

Registre a ligação entre a revisão do template, a saída `BucketName` e o recurso inspecionado. Confirme que o bucket de teste está vazio, registre o estado `DELETE_COMPLETE` para a stack e o recurso e confira no inventário S3 a ausência do mesmo bucket. Registre a conferência de faturamento separadamente, após sua atualização. Publique somente os resultados sanitizados.
