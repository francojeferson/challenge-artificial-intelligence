# +A Educação - Engenheiro de Inteligência Artificial

[![N|Solid](https://maisaedu.com.br/hubfs/site-grupo-a/logo-mais-a-educacao.svg)](https://maisaedu.com.br/)

O objetivo deste desafio é avaliar as competências técnicas dos candidatos a Engenheiro de Inteligência Artificial na
Maior Plataforma de Educação do Brasil.

Neste teste prático, você será apresentado a um conjunto de dados simulado relacionado aos fundamentos de programação.
Seu objetivo é realizar a indexação dos diferentes tipos de dados e desenvolver um prompt de sistema de aprendizagem
adaptativa que gere conteúdos dinâmicos conforme as dificuldades e desconhecimentos do usuário sobre o tema.

# Sobre os dados

O conjunto de dados definidos para este teste é de propriedade intelectual da +A Educação e deverá ser utilizado
exclusivamente para esta finalidade, sendo composto por:

- **Textos:** Uma coleção de textos extraídos de módulos de aprendizagem.
- **PDFs:** Livros e manuais introdutórios sobre o conteúdo abordado.
- **Vídeos:** Pequenos vídeos de dicas de professor, que explicam o conteúdo abordado. Os vídeos estão em formatos .mp4

O conjunto de dados pode ser obtido
[clicando aqui](https://github.com/grupo-a/challenge-artificial-intelligence/tree/main/resources).

# Requisitos

## Etapa 1: Indexação dos Dados

Defina a ferramenta de indexação que considere adequada para o projeto. Recomenda-se escolher uma ferramenta que possa
suportar a geração dinâmica de conteúdos adaptativos no prompt de IA generativa. Indexe os diferentes tipos de dados
para permitir uma busca eficiente e relevante.

Os textos devem ser indexados para permitir uma busca eficiente por palavras-chave e frases relevantes.

Os PDFs devem ser processados para extrair texto pesquisável e metadados importantes.

Os vídeos devem ser transcritos, se possível, e indexados com base no texto transcrito, juntamente com metadados
descritivos.

As imagens devem ser indexadas considerando metadados relevantes, como tags, descrições e informações sobre o conteúdo
visual.

## Etapa 2: Prompt de Aprendizagem Adaptativa

Construa um prompt interativo, utilizando as tecnologias que julgar apropriadas, que identifique as dificuldades e
lacunas de conhecimento dos usuários em um diálogo fluido e intuitivo para avaliar e entender as áreas onde seu
conhecimento sobre um tema específico pode ser insuficiente. O escopo deve estar limitado ao conteúdo indexado. Durante
as interações, inclua mecanismos que permitam identificar as preferências dos usuários quanto ao formato de aprendizado
mais efetivo para eles, seja texto, vídeo ou áudio, adaptando-se assim às suas preferências pessoais de consumo de
conteúdo.

Baseado nas interações analise as dificuldades e gere conteúdos dinâmicos curtos em diferentes formatos (vídeos, áudios,
textos) para abordar as necessidades específicas de aprendizagem do usuário. Os conteúdos devem ser relevantes,
informativos e adaptados ao nível de conhecimento do usuário.

# Critérios de avaliação

- Qualidade de escrita do código.
- Organização do projeto.
- Lógica da solução implementada.
- Capacidade de escolher as tecnologias apropriadas para indexação de dados e desenvolvimento do sistema de aprendizagem
  adaptativa.
- Eficiência na manipulação de diferentes tipos de dados (textos, PDFs, vídeos).
- Competência na construção de prompts de IA que geram conteúdos adaptativos dinâmicos.
- Capacidade de integrar diferentes componentes do sistema (indexação, interface de usuário, geração de conteúdo) de
  forma coesa.

# Diferenciais

- Avaliação da capacidade do sistema em identificar corretamente as dificuldades dos usuários e adaptar o conteúdo de
  aprendizagem conforme necessário.
- Relevância, informatividade e adaptação do conteúdo gerado ao nível de conhecimento do usuário.
- Performance do sistema em diferentes condições de uso e sua capacidade de escalar conforme o aumento do número de
  usuários.

# Instruções de Execução

O sistema de aprendizagem adaptativa pode ser executado tanto localmente quanto em um ambiente containerizado usando
Docker. Siga as instruções abaixo para configurar e executar o projeto de acordo com sua preferência.

## Executando Localmente (localhost)

1. **Pré-requisitos**:

   - Certifique-se de ter o Python 3.8+ instalado em seu sistema. Você pode baixá-lo em
     [python.org](https://www.python.org/downloads/).
   - Baixe o modelo Vosk para transcrição de vídeos em português brasileiro ('vosk-model-small-pt-0.3') de
     [alphacephei.com](https://alphacephei.com/vosk/models) e coloque-o no diretório do projeto em
     './vosk-model-small-pt-0.3'.

2. **Clone o Repositório**:

   - Clone este repositório para sua máquina local usando `git clone <URL do repositório>` ou baixe o código-fonte
     diretamente.

3. **Instale as Dependências**:

   - Navegue até o diretório do projeto: `cd <diretório do projeto>`.
   - Instale as dependências listadas em 'requirements.txt' usando: `pip install -r requirements.txt`.
   - Nota: Pode ser necessário instalar dependências do sistema como 'ffmpeg' e 'libsndfile1' para processamento de
     vídeo e áudio. No Windows, você pode precisar de ferramentas adicionais para compilar 'pyaudio'; considere usar um
     ambiente virtual ou WSL (Windows Subsystem for Linux) se encontrar problemas.

4. **Execute o Sistema**:

   - Execute o script principal com: `python run.py`.
   - O sistema iniciará o processo de ingestão e indexação de recursos localizados no diretório 'resources'.
     Certifique-se de que os dados estejam disponíveis nesse diretório.
   - Monitore a saída no terminal para verificar o progresso. Se o modelo Vosk não for encontrado, ajuste o caminho no
     'video_ingestor.py' ou defina a variável de ambiente 'VOSK_MODEL_PATH'.
   - Para acessar a interface web, execute o servidor FastAPI com: `uvicorn adaptive_learning.ui.web_app:app --reload` e
     abra seu navegador em `http://localhost:8000`.

5. **Interrompa a Execução**:
   - Pressione Ctrl+C no terminal para interromper o processo, se necessário.

## Executando em um Ambiente Containerizado (Docker)

1. **Pré-requisitos**:

   - Certifique-se de ter o Docker Desktop instalado e em execução em seu sistema. Você pode baixá-lo no
     [site oficial do Docker](https://www.docker.com/products/docker-desktop).
   - Baixe o modelo Vosk para transcrição de vídeos em português brasileiro ('vosk-model-small-pt-0.3') de
     [alphacephei.com](https://alphacephei.com/vosk/models) e coloque-o no diretório do projeto em
     './vosk-model-small-pt-0.3'.

2. **Clone o Repositório**:

   - Clone este repositório para sua máquina local usando `git clone <URL do repositório>` ou baixe o código-fonte
     diretamente.

3. **Construa a Imagem Docker**:

   - Navegue até o diretório do projeto: `cd <diretório do projeto>`.
   - Execute o comando para construir a imagem Docker: `docker build -t adaptive-learning-system .`.
   - Este comando constrói uma imagem chamada 'adaptive-learning-system' usando o 'Dockerfile' atualizado, que inclui
     todos os arquivos do projeto e dependências.

4. **Execute um Contêiner Docker**:

   - Após a construção da imagem, execute um contêiner com o comando:
     `docker run -d -p 8000:8000 --name adaptive-learning-container adaptive-learning-system`.
   - Este comando executa um contêiner em modo detached ('-d'), mapeia a porta 8000 do host para a porta 8000 do
     contêiner ('-p 8000:8000'), nomeia o contêiner como 'adaptive-learning-container', e inicia o servidor web FastAPI
     automaticamente.
   - O contêiner executará o sistema de aprendizagem adaptativa, acessível via navegador em `http://localhost:8000`, com
     funcionalidades como persistência de sessão via localStorage e server-side storage, seleção de preferência de
     formato de conteúdo, e mecanismos de feedback com avaliações multidimensionais (geral, relevância, eficácia)
     totalmente integrados.

5. **Monitore a Saída**:

   - Você verá a saída de 'run.py' no terminal, mostrando o progresso da ingestão e indexação de recursos. Se encontrar
     problemas, verifique as mensagens de erro para orientação sobre dependências ausentes ou configuração.
   - Para visualizar os logs do contêiner, use `docker logs adaptive-learning-container`.

6. **Interrompa o Contêiner**:
   - Para parar o contêiner, use o comando `docker stop adaptive-learning-container` e, se desejar removê-lo, use
     `docker rm adaptive-learning-container`.

**Nota**: Se o caminho do modelo Vosk precisar de ajuste ou se você encontrar problemas de permissão com acesso a
arquivos, pode ser necessário modificar a variável de ambiente 'VOSK_MODEL_PATH' adicionando '-e
VOSK_MODEL_PATH=/caminho/para/o/modelo' ao comando 'docker run' com o caminho correto dentro do contêiner.

# Instruções de entrega

1. Crie um fork do repositório no seu GitHub
2. Faça o push do código desenvolvido no seu Github
3. Inclua um arquivo chamado COMMENTS.md explicando
   - Decisão da arquitetura utilizada
   - Lista de bibliotecas de terceiros utilizadas
   - O que você melhoraria se tivesse mais tempo
   - Quais requisitos obrigatórios que não foram entregues
4. Informe ao recrutador quando concluir o desafio junto com o link do repositório
5. Após revisão do projeto junto com a equipe de desenvolvimento deixe seu repositório privado

# Status do Projeto

O sistema de aprendizagem adaptativa está em um estágio avançado de desenvolvimento com as seguintes realizações:

- **Indexação de Dados**: Todos os tipos de recursos (texto, PDF, vídeo, imagem) foram ingeridos e indexados com sucesso
  para recuperação eficiente.
- **Prompt de Aprendizagem Adaptativa**: Um prompt interativo foi construído utilizando spaCy para análise semântica,
  identificando lacunas de conhecimento e preferências de formato do usuário (texto, vídeo, áudio).
- **Interface do Usuário**: Interface web totalmente implementada com FastAPI (backend) e React (frontend), integrada ao
  Prompt Engine para entrega dinâmica de conteúdo, acessível em `http://localhost:8000`, com persistência de sessão via
  localStorage e armazenamento no servidor, seleção de preferência de formato de conteúdo, e mecanismo de feedback
  aprimorado com avaliações multidimensionais (geral, relevância, eficácia).
- **Testes**: Testes de integração atualizados para endpoints de API (mensagem e feedback) em 'test_integration.py', com
  todos os testes passando, validando funcionalidade central, interação do usuário, responsividade da UI, e precisão na
  adaptação de conteúdo.
- **Documentação**: Atualizações contínuas em arquivos de memória (`progress.md`, `productContext.md`,
  `activeContext.md`, `raw_reflection_log.md`) e documentos do projeto (`PRD.md`, `COMMENTS.md`, `README.md`,
  `adaptive_learning/ui/README.md`) para refletir o estado atual, melhorias recentes, e próximos passos.

**Pendências**:

- Integração de frameworks avançados de NLP (como LangChain ou LlamaIndex) para geração de conteúdo mais contextual e
  personalizado.
- Testes adicionais de ponta a ponta para cenários de usuário diversos e casos extremos.
- Otimização de desempenho para grandes conjuntos de dados e usuários concorrentes.
- Gerenciamento final do repositório e entrega conforme instruções do projeto.
