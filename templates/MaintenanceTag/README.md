# MaintenanceTag

Modelo para o projeto que consome o kit. Nenhuma tela deste repositório inclui este trecho.

## Instalação

1. Copie `maintenance-tag.css` para a folha de estilo do projeto.
2. Copie o checkbox para a tela de configuração, uma vez.
3. Em cada elemento visível, use a classe `elemento`, o atributo `data-maint-id` com o código do registro, e um `span.maint-tag` com o mesmo código.
4. O código fica no canto inferior esquerdo. Ele só aparece, na tela e na impressão, quando o checkbox está marcado.

O registro continua em `.glpi/manutencao/registro-codigos.json`. Este modelo não grava o registro.
