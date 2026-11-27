---
id: GLO-001
tipo: glossario
titulo: Manutenção por código
codigo: F1.S1.P2
status: rascunho
versao: 0.1.0
data: 2026-11-27
autor: Ricardo
classificacao: publico
---

# Manutenção por código

## Termos
| Termo ou sigla | Significado | Contexto de uso |
|---|---|---|
| código | Identificador único e estável de um elemento. A primeira letra indica o tipo. O código de um elemento aposentado não volta a ser usado. | Canto inferior esquerdo do elemento e título do chamado |
| elemento | Painel, quadro, janela, modal, formulário ou componente visível que recebe um código. | Interface do sistema |
| chamado | Registro de manutenção no GLPI. O título traz o código entre colchetes e uma descrição curta. O chamado é o registro oficial da manutenção. | Abertura e acompanhamento da manutenção |
| F | Fase do trabalho. | Plano e espelho no GLPI |
| S | Sessão dentro de uma fase. | Plano e espelho no GLPI |
| P | Tarefa dentro de uma sessão, ancorada em um commit. | Plano, commit e tarefa do GLPI |
| F/S/P | Código relativo da fase, da sessão e da tarefa, no formato `F#.S#.P#`. Chamado e projeto não entram nesse código. | Itens de plano, commits e tarefas |
| natureza de manutenção | Classificação do chamado: corretiva, adaptativa, perfectiva, preventiva ou codificação. | Triagem do chamado |
