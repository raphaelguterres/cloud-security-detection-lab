# Laboratório AWS de Segurança em Nuvem e IaC

## Objetivo

Praticar a criação e a remoção de uma infraestrutura mínima por código, verificar permissões de privilégio mínimo e usar eventos de gerenciamento do CloudTrail para construir detecções reproduzíveis. O laboratório usa um projeto AWS separado da produção, com recursos regionais em `us-east-2` (Ohio) e dados fictícios.

## Custo

O laboratório opera em **Ohio** com limite de **US$ 0 em cobranças**. Antes de provisionar, confira se o **AWS Free Plan** está ativo, se há saldo de créditos e se as operações do ensaio são elegíveis. Se a AWS exigir mudança de plano, suspenda o ensaio em nuvem. [Regras do Free Plan](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html)

## Acesso e recursos

Use até **dois papéis IAM com sessões temporárias** e confiança restrita à conta do laboratório. O papel de provisionamento cria e remove somente os recursos aprovados. O papel de leitura consulta os eventos e os artefatos necessários à evidência, com permissões mínimas.

| Recurso | Limite aprovado |
| --- | --- |
| CloudTrail Event history | Consultar e exportar eventos de gerenciamento do laboratório em `us-east-2`. |
| Amazon S3 | Um bucket privado S3 Standard com acesso público bloqueado. Até **100 MiB** de objetos fictícios e limpeza no fim da sessão. |
| Monitoramento de custo | Saldo e validade no console. Até um orçamento com notificações se disponível no Free Plan e sem cobrança. |
| Estado de IaC e evidências | Estado em diretório local privado, fora do Git. Exportações sanitizadas para o relatório. |

Produção, contas de terceiros, dados reais, acesso público, EC2, RDS, NAT Gateway, CloudTrail Lake, trilhas adicionais, eventos de dados e ingestão em CloudWatch Logs ficam fora deste escopo. Ao encerrar o ensaio, confira o inventário, remova os recursos temporários criados e registre o estado final dos recursos e do custo.

## Entregas e estado

- [Template CloudFormation](infra/bucket-evidencias.json) de um bucket privado com SSE-S3, quatro bloqueios de acesso público e política de exclusão.
- [Evidências técnicas sanitizadas](docs/EVIDENCIAS-M4.md) de escopo, template, IAM, sinal CloudTrail e procedimento de encerramento.
- [Checklist do M4 na trilha](https://github.com/raphaelguterres/raphaelguterres/blob/main/roadmaps/PROGRESSO.md#m4--cloud-security-e-iac--110180-h-estimadas) para acompanhar os critérios técnicos.

O escopo e os documentos iniciais têm aceite. A criação e a remoção da stack e do mesmo bucket foram verificadas em Ohio. O proprietário aceitou a evidência em 24/11/2026. As validações do papel IAM e os eventos reais do CloudTrail ficam pendentes. [Evidência do ciclo em Ohio](docs/VALIDACAO-IAC-OHIO.md#aceite)
