---
id: REQ-001
tipo: requisito
titulo: Identificação codificada de elemento
codigo: F1.S1.P1
status: em_revisao
versao: 0.2.0
data: 2026-11-27
autor: Ricardo
classificacao: publico
---

# Identificação codificada de elemento

## Descrição
Todo elemento visível da interface tem um código único e estável, exibido no canto inferior esquerdo, que pode ser ocultado por um checkbox de configuração.

## Critérios de aceite
- [ ] Cada elemento visível (painel, quadro, janela, modal, formulário ou componente) tem um único código, que não muda enquanto o elemento existir
- [ ] O código aparece no canto inferior esquerdo do elemento
- [ ] O checkbox "Exibir código de identificação para manutenção nos elementos do sistema." controla a exibição
- [ ] O código de um elemento aposentado não é reutilizado
- [ ] O título do chamado de manutenção segue o formato `[código] descrição curta`
- [ ] O GLPI é o registro oficial das manutenções; o histórico do produto apenas cita o chamado
- [ ] Atualização do kit preserva o registro de códigos, a escala de responsáveis e o histórico do produto
- [ ] O repositório público não recebe dado pessoal, segredo nem identificação de cliente

## Rastreabilidade
- Regras de negócio: RN-001, RN-002, RN-003, RN-004, RN-005, RN-006, RN-007
- Tarefas do plano: F1.S1.P1
- Testes: A DEFINIR
