Scenario: Developer Productivity with Claude You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks. It uses built-in tools (Read, Write, Bash, Edit) with MCP servers. A team wants to add a "cancel renewal" workflow to a legacy subscription service. The initial implementation point is unclear because cancellation behavior appears split across command-line scripts, web handlers, and scheduled jobs. In earlier similar tasks, immediate edits repeatedly targeted the wrong abstraction and had to be rolled back after tests exposed broken shared behavior. Which workflow should the tool recommend first?

---

[ ] A - Instruct Claude to read every repository file first, then implement changes in the same extended session.
[ ] B - Proceed with direct execution, relying on test failures to reveal hidden dependencies and guide successive corrective edits.
[ ] C - Start separate direct-execution sessions for each suspected module, then manually combine the resulting edits later.
[ ] D - Use plan mode to map relevant flows and compare implementation points before allowing file modifications.

---

### TRANSLATED QUESTION
Cenário: Produtividade do Desenvolvedor com o Claude Agent SDK
Você está construindo ferramentas de produtividade para desenvolvedores usando o Claude Agent SDK. O agente ajuda engenheiros a explorar bases de código desconhecidas, entender sistemas legados, gerar código boilerplate e automatizar tarefas repetitivas. Ele usa ferramentas nativas (Read, Write, Bash, Edit) com servidores MCP. Um time quer adicionar um fluxo de "cancelar renovação" a um serviço de assinaturas legado. O ponto inicial de implementação é incerto, pois o comportamento de cancelamento parece estar espalhado entre scripts de linha de comando, handlers web e jobs agendados. Em tarefas semelhantes anteriores, edições imediatas repetidamente miraram na abstração errada e tiveram que ser revertidas depois que os testes revelaram comportamento compartilhado quebrado.
Qual fluxo de trabalho a ferramenta deveria recomendar primeiro?
Alternativas traduzidas:

A) Instruir o Claude a ler todos os arquivos do repositório primeiro, e depois implementar as mudanças na mesma sessão estendida.
B) Prosseguir com execução direta, confiando que falhas de teste vão revelar dependências ocultas e guiar edições corretivas sucessivas.
C) Iniciar sessões de execução direta separadas para cada módulo suspeito, depois combinar manualmente as edições resultantes.
D) Usar o modo de planejamento (plan mode) para mapear os fluxos relevantes e comparar pontos de implementação antes de permitir modificações de arquivo.
---

### EXPLANATION (TECH LEAD)

Explicação:
A pergunta está testando o entendimento de quando usar plan mode versus execução direta em fluxos de trabalho agentic com o Claude Agent SDK — um dos temas centrais da certificação.
O sinal-chave no enunciado é: "o ponto inicial de implementação é incerto" + "comportamento espalhado entre múltiplos lugares" + "em tarefas anteriores, edições imediatas erraram a abstração e tiveram que ser revertidas". Isso é literalmente a definição de um problema com alta incerteza estrutural: você não sabe onde a lógica de cancelamento realmente vive nem como os componentes se relacionam antes de tocar no código.
Por que a alternativa D é a correta:
O plan mode existe exatamente para esse cenário: antes de qualquer edição, o agente investiga (lê, busca, mapeia relações) e produz um plano que pode ser revisado por um humano — sem risco de side effects, porque nenhuma escrita acontece ainda. Isso permite comparar os candidatos a "ponto de implementação" (script CLI, handler web, job agendado) e decidir com base em evidência, não em suposição. Dado o histórico de retrabalho por abstrações erradas, investir em mapeamento antes de editar é a escolha que reduz risco e retrabalho.
Por que as outras estão erradas:

A) Ler todo o repositório é ineficiente e não resolve o problema real, que não é falta de leitura, mas falta de um plano estruturado de comparação entre pontos de implementação. Além disso, fazer a leitura e a implementação "na mesma sessão estendida" reintroduz o risco de editar antes de entender a relação entre os módulos — é uma falsa sensação de "pesquisa" sem a disciplina do plan mode.
B) É exatamente o padrão que já falhou antes ("early similar tasks" tiveram que ser revertidas). Confiar em falhas de teste para revelar dependências ocultas é reativo, caro e já provou não funcionar nesse contexto específico.
C) Paralelizar sessões de execução direta por módulo suspeito ainda assume que você já sabe quais são os módulos certos — e ainda gera o problema extra de reconciliar manualmente edições feitas às cegas em paralelo. É uma variação do erro de B, só que distribuída.

Dica importante: Um padrão recorrente nas perguntas da certificação é: incerteza sobre escopo/impacto + histórico de retrabalho por escrita prematura → plan mode. Sempre que o enunciado mencionar "não está claro onde", "comportamento espalhado" ou "já tivemos que reverter", isso é o sinal para investigação/planejamento antes de execução.
---

### 🚸 CHILDREN EXPLANATION 

A missão do robô ajudante 🤖
Imagina que você tem um robô assistente super esperto que te ajuda a arrumar uma casa gigante e bagunçada — só que essa casa tem 100 anos e foi reformada um monte de vezes por pessoas diferentes. Ninguém mais lembra direito onde ficam os fios de eletricidade, os canos de água, nada disso!
Agora seu chefe pede: "Robô, por favor, desliga aquele interruptor de luz velho que ninguém usa mais."
Só que tem um probleminha: esse interruptor pode estar ligado em vários lugares escondidos da casa — talvez ele também controle a luz do porão, ou o alarme, ou até a geladeira! E da última vez que o robô mexeu em algo parecido sem checar antes, ele desligou sem querer a geladeira inteira, e teve que consertar tudo de novo. Que trabalheira! 😅
Então, o que o robô deveria fazer agora?

🅰️ Ler a casa inteira, cômodo por cômodo, e já sair mexendo em tudo ao mesmo tempo → Ele ia demorar uma eternidade e ainda ia se confundir, porque ler tudo não é a mesma coisa que entender como as coisas se conectam.
🅱️ Só ir mexendo e torcer para descobrir o que dá errado depois → Já vimos que isso quebrou a geladeira da última vez! Péssima ideia repetir o mesmo erro.
🅲️ Mandar vários robozinhos mexerem em partes diferentes da casa ao mesmo tempo, sem se falar → Ainda pior — agora são vários robôs bagunçando coisas escondidas ao mesmo tempo, e depois alguém tem que juntar a bagunça toda de todo mundo.
🅳️ Primeiro fazer um mapa da casa, seguindo os fios e canos com cuidado, ANTES de mexer em qualquer coisa → ✅ Essa é a ideia mais esperta!

É como quando você monta um quebra-cabeça: antes de forçar as peças, você primeiro olha todas as peças e imagina onde elas se encaixam, né? Isso é exatamente o que o "plan mode" (modo de planejar) faz: o robô olha, investiga, desenha um mapa de como tudo se conecta — e só DEPOIS que ele (ou você) confirma que o mapa faz sentido, ele começa a mexer de verdade.
Assim, ninguém desliga a geladeira sem querer de novo! 🧊❌
---

### CORRECT ANSWER

[ ] B - Replace fetch_url with a load_document tool that accepts catalog document IDs or approved URLs and validates before fetching.



