### Regras de Anonimato e Segurança
- *AS01*: O identificador real do aluno (matrícula/nome) **nunca** deve ser persistido. Deve ser transformado via SHA-256 antes da inserção;
- *AS02*: O sistema deve permitir que o mesmo aluno envie feedbacks diferentes, mas o hash deve ser consistente para evitar spam.
- *AS03*: Um aluno pode enviar, no máximo, 7 feedbacks para o mesmo monitor em uma mesma turma. Por exemplo: se uma turma tem 2 monitores, ela só pode enviar 7 para o primeiro e 7 para o segundo.
- *AS04*: O Hash SHA-256 deve utilizar uma chave secreta armazenado apenas no arquivo .env para evitar que alguém com acesso ao banco descubra a identidade dos alunos por força bruta.
- *AS05*: Os campos `hash_aluno` e `data_submissao` em um feedback **nunca** podem ser editados após a criação, nem mesmo via `PATCH`


### Validações
- *V01*: O nome de um curso deve ser único
- *V02*: A sigla de um curso deve possuir no máximo 3 caracteres
- *V03*: O email do aluno deve terminar com `@alu.ufc.br`
- *V04*: O campo matrícula deve ser numérico
- *V05*: O campo matrícula deve possuir no máximo 7 caracteres
- *V06*: O campo de texto em Feedback deve possuir um limite mínimo de 2 caracteres
- *V07*: O campo de texto em Feedback deve possuir um limite máximo de 5000 caracteres
- *V08*: O campo createdAt em Feedback deve ser atribuído automaticamente
- *V09*: O campo `texto_feedback` (ou nome semelhante, ver no diagrama ER) não pode conter apenas espaços em branco ou caracteres de escape, p. ex., `\n`
- *V10*: O campo `semestre_ideal` deve ser um número entre 1 e 5
- *V11*: O campo `cod` na entidade Classroom deve ter exatamente 3 caracteres
- *V12*: O campo `cod` na entidade Subject deve ter no máximo 9 caracteres
- *V13*: O campo `isActive` na entidade Enrollment deve ser inserida no banco com `default=true`

### Integridade de Relacionamentos
- *IR01*: Um monitor só pode receber feedback por uma disciplina na qual ele está efetivamente vinculado. P. ex.: Não posso ser da turma de FUP-SI e dar Feedback para um monitor que está na turma de FUP-IA
- *IR02*: Não é possível deletar um curso que possua disciplinas vinculadas
- *IR03*: Não é possível deletar um monitor que possua feedbacks
- *IR04*: Não é possível cadastrar uma disciplina sem um professor responsável
- *IR05*: Um monitor não pode ser associado mais de uma vez à mesma turma

### Regras de Consulta
- *RC-01*: Nenhuam listagem GET pode retornar mais do que 10 registros por vez a menos que determinado por quem chama a rota
- *RC-02*: A busca por texto em Feedbacks deve ser **case-insensitive** para facilitar a busca
- *RC-03*: Por padrão, os feedbacks devem ser retornados do mais recente para o mais antigo
- *RC-04*: Deve ser possível listar todos os feedbacks de todos os monitores de uma turma