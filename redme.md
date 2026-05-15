📖 Documentação do Código: Gerenciador Copa 2026
1. Importação de Bibliotecas
Python

import streamlit as st
import json
import os
import pandas as pd

    streamlit: Biblioteca principal que cria a interface visual e transforma o código Python num site local.

    json: Utilizada para converter o teu progresso num formato de texto que o computador consegue salvar e ler depois.

    os: Serve para o Python "olhar" para a pasta do Windows e verificar se o ficheiro de dados já existe.

    pandas: Usada especificamente para criar a tabela visual de figurinhas repetidas na aba de estatísticas.

2. Funções de Backend (Persistência)
Python

def carregar_dados():
    try:
        if os.path.exists(NOME_ARQUIVO_JSON):
            with open(NOME_ARQUIVO_JSON, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        st.error("Erro ao carregar o arquivo JSON.")
    return {}

    try...except: Este bloco é uma proteção. Se o ficheiro JSON estiver corrompido ou bloqueado, o programa não "crasha" (não fecha com erro), ele apenas avisa e começa um registo novo.

    json.load: Lê as informações guardadas no disco e coloca-as dentro do programa.

3. Gestão de Estado (Session State)
Python

if 'meu_album' not in st.session_state:
    st.session_state.meu_album = carregar_dados()

    st.session_state: É a memória temporária do teu navegador. Como o Streamlit recarrega o código todo a cada clique, isto garante que o que escreveste não se apague sozinho enquanto o site está aberto.

4. Estrutura de Dados e Lógica de Limites
Python

selecoes = { "Brasil": "BRA", "México": "MEX", ... }
limite = 14 if sigla == "CC" else (19 if sigla == "FWC" else 20)

    Dicionário selecoes: Mapeia o nome real da seleção para a sigla que está no teu PDF (ex: BRA, HAI, CC).

    Lógica de Limite: Define automaticamente o tamanho de cada categoria: 14 para as da Coca-Cola, 19 para a História da Taça (FWC) e 20 para as seleções comuns.

5. Interface de Inventário
Python

cols = st.columns(4)
for n in range(1, limite + 1):
    cod = f"{sigla}{n}"
    nova_qtd = st.number_input(f"Qtd {cod}", ..., key=f"nb_{cod}")
    st.session_state.meu_album[cod] = nova_qtd

    st.columns(4): Organiza os campos de entrada em 4 colunas para que a página não fique demasiado longa e seja fácil de usar no portátil Acer.

    number_input: Onde inseres a quantidade: 0 se não tens, 1 se já colaste, e 2 ou mais para repetidas.

6. Cálculo de Estatísticas
Python

total_distintas = sum(1 for v in st.session_state.meu_album.values() if v > 0)
total_repetidas = sum(max(0, v - 1) for v in st.session_state.meu_album.values())

    total_distintas: Conta quantas figurinhas tens (não importa se é 1 ou 10), para saber o progresso de colagem.

    total_repetidas: Soma apenas o que tens "a mais" (ex: se tens 3 da BRA1, ele soma 2 para a lista de trocas).

7. Salvamento Manual
Python

if st.sidebar.button("💾 Salvar Tudo"):
    salvar_dados(st.session_state.meu_album)

    Botão Lateral: Executa a função que escreve todos os teus dados atuais no ficheiro meu_progresso_v2.json. É o que garante que o teu trabalho fica guardado para o dia seguinte.



1. Importação de Bibliotecas

    import streamlit as st: Importa o framework que cria a interface visual do seu site local.

    import json: Importa a biblioteca para ler e salvar arquivos no formato JSON (seu banco de dados).

    import os: Biblioteca do sistema operacional para verificar se arquivos existem nas suas pastas.

    import pandas as pd: Ferramenta de análise de dados usada aqui para criar a tabela de repetidas.

2. Configurações Iniciais

    st.set_page_config(page_title="Copa 2026 - Master Control", layout="wide"): Define o título da aba no navegador e faz o site ocupar a largura total da tela.

    NOME_ARQUIVO_JSON = "meu_progresso_v2.json": Cria uma variável com o nome do arquivo onde os dados serão salvos.

3. Função de Carregar Dados (Backend)

    def carregar_dados():: Define a função que busca os dados salvos anteriormente.

    try:: Inicia um bloco de teste; se algo der errado aqui dentro, o programa não "quebra".

    if os.path.exists(NOME_ARQUIVO_JSON):: Verifica se o arquivo JSON já existe na pasta copa.

    with open(NOME_ARQUIVO_JSON, "r") as f:: Abre o arquivo apenas para leitura ("r").

    return json.load(f): Converte o texto do arquivo JSON de volta para um dicionário Python.

    except (json.JSONDecodeError, IOError):: Se o arquivo estiver corrompido ou inacessível, captura o erro.

    return {}: Se não houver arquivo ou houver erro, retorna um dicionário vazio para começar do zero.

4. Função de Salvar Dados

    def salvar_dados(dados):: Função que recebe as informações atuais e as grava no computador.

    with open(NOME_ARQUIVO_JSON, "w") as f:: Abre (ou cria) o arquivo para escrita ("w").

    json.dump(dados, f): Transforma o dicionário do Python em texto JSON e salva no arquivo.

5. Memória da Sessão

    if 'meu_album' not in st.session_state:: Verifica se o site acabou de ser aberto.

    st.session_state.meu_album = carregar_dados(): Se for a primeira vez, carrega os dados do JSON para a memória do navegador.

6. Estrutura do Álbum (Baseada no seu PDF)

    selecoes = { ... }: Um dicionário que mapeia o nome completo da seleção para a sigla usada no PDF (ex: "Brasil" -> "BRA").

    sel_nome = st.selectbox("Escolha a Seleção:", list(selecoes.keys())): Cria o menu suspenso com os nomes das seleções.

    sigla = selecoes[sel_nome]: Pega a sigla da seleção que você escolheu no menu.

    limite = 14 if sigla == "CC" else (19 if sigla == "FWC" else 20): Lógica para saber se a página tem 14, 19 ou 20 figurinhas, conforme as regras do seu PDF.

7. Interface de Inventário

    cols = st.columns(4): Divide a área central em 4 colunas verticais.

    for n in range(1, limite + 1):: Um loop que repete o código para cada figurinha daquela seleção.

    cod = f"{sigla}{n}": Monta o código da figurinha (ex: BRA1, BRA2).

    qtd_atual = st.session_state.meu_album.get(cod, 0): Busca no seu progresso quantas você tem daquela figurinha; se não tiver nada, assume 0.

    nova_qtd = st.number_input(...): Cria o campo onde você digita ou clica para mudar a quantidade.

    st.session_state.meu_album[cod] = nova_qtd: Atualiza a memória do navegador com o novo valor que você digitou.

8. Aba de Estatísticas

    total_distintas = sum(1 for v in st.session_state.meu_album.values() if v > 0): Conta quantas figurinhas diferentes você tem coladas (quantidade maior que zero).

    total_repetidas = sum(max(0, v - 1) for v in st.session_state.meu_album.values()): Soma apenas o que você tem a mais (ex: se tem 3, conta 2 como repetidas).

    st.metric(...): Exibe aqueles números grandes e bonitos no topo da página.

    lista_repetidas = [...]: Cria uma lista filtrada apenas com as figurinhas que têm quantidade maior que 1.

    st.table(pd.DataFrame(lista_repetidas)): Usa o Pandas para formatar essa lista em uma tabela organizada para você levar nas trocas.

9. Botão de Salvar

    if st.sidebar.button("💾 Salvar Tudo"):: Cria o botão na barra lateral.

    salvar_dados(st.session_state.meu_album): Quando clicado, chama a função lá do início para gravar tudo permanentemente no arquivo JSON.

Fiz uma revisão minuciosa (pente fino) comparando a explicação anterior com o código final. Notei que alguns detalhes técnicos de sintaxe e lógica de exibição não foram detalhados "linha por linha" na resposta anterior.

Aqui estão as explicações das partes que faltavam ou que podem ser detalhadas para o seu nível de Software Engineering na FIAP:
1. Detalhes de Sintaxe no Backend

    with open(NOME_ARQUIVO_JSON, "r") as f:: O comando with é um "Gerenciador de Contexto". Ele garante que o arquivo seja fechado automaticamente pelo Python assim que terminar de ler, mesmo que ocorra um erro, evitando que o arquivo fique "preso" na memória.

    as f: Define que, dentro desse bloco de código, chamaremos o arquivo aberto pelo apelido de f.

2. Lógica de Posicionamento (Layout)

    with cols[(n-1)%4]:: Esta é uma lógica matemática (operador de módulo %). Como temos 4 colunas, o cálculo (n-1)%4 garante que a figurinha 1 vá para a coluna 0, a figurinha 2 para a coluna 1... e a figurinha 5 volte para a coluna 0, criando as linhas da grade perfeitamente.

3. Gerenciamento de Identificadores (Keys)

    key=f"nb_{cod}": No Streamlit, cada elemento visual (como o campo de número) precisa de uma "chave" única. Usamos o código da figurinha (ex: nb_BRA1) para que o Python não confunda os valores de diferentes figurinhas.

4. Lógica Avançada de Estatísticas

    sum(1 for v in st.session_state.meu_album.values() if v > 0): Isso é uma "compreensão de lista". Estamos criando uma lista temporária de "1s" para cada figurinha que tem quantidade maior que zero e somando tudo para ter o total de únicas coladas.

    max(0, v - 1): Usamos a função max para garantir que o número de repetidas nunca seja negativo. Se você tem 0 figurinhas, 0 - 1 daria -1, mas o max(0, -1) retorna 0.

    vagas_totais = sum(...): Esta linha percorre todas as siglas do dicionário selecoes e soma os espaços disponíveis (14, 19 ou 20) para dar o número total de figurinhas que existem no álbum do seu PDF.

5. Interface de Resumo

    c1, c2, c3 = st.columns(3): Cria três colunas pequenas e iguais para colocar os indicadores de desempenho lado a lado.

    c3.metric(..., f"{(total_distintas/vagas_totais)*100:.1f}%"): O código :.1f é um formatador que limita o resultado da divisão a apenas uma casa decimal (ex: 85.4%), deixando a interface mais limpa para consulta.

Aqui está uma versão aprimorada e profissional do seu README.md, detalhando as funcionalidades de rastreamento de figurinhas (faltantes e repetidas) e a estrutura lógica por trás do sistema.📖 Documentação do Sistema de Gerenciamento - Copa 2026Este documento detalha o funcionamento dos módulos de Figurinhas Faltantes e Figurinhas Repetidas, projetados para oferecer uma visão analítica e organizada do progresso da sua coleção.🛠️ Arquitetura das FuncionalidadesO sistema utiliza o st.session_state para manter a persistência dos dados enquanto você navega pelas abas, cruzando as informações inseridas no inventário com as regras específicas de cada coleção.1. 🔍 Painel de Figurinhas FaltantesEste módulo resolve o problema de identificar "buracos" na coleção sem a necessidade de conferência manual folha por folha.Lógica de Filtro: O algoritmo itera sobre cada chave do dicionário de seleções e verifica, dentro do limite numérico de cada uma (14, 19 ou 20), quais chaves possuem valor zero ou inexistente.Interface Retrátil: Conforme exibido em Captura de tela 2026-05-13 185535.png, as seleções são agrupadas em expanders que mostram o total de itens ausentes no título, economizando espaço visual.Visualização de Conteúdo: Ao abrir um expander, os códigos faltantes são apresentados em uma lista separada por vírgulas para facilitar a leitura rápida.2. ♻️ Módulo de Trocas (Figurinhas Repetidas)A aba de estatísticas foi atualizada para transformar a antiga tabela em um sistema de inventário de trocas dinâmico.Cálculo de Excedentes: O sistema ignora a primeira unidade (destinada ao álbum) e contabiliza apenas o saldo extra ($Quantidade - 1$).Padronização Visual: Para manter a consistência com a aba de faltantes (seguindo o modelo de Captura de tela 2026-05-13 185754.png), as repetidas agora também são organizadas por seleção.Indicador de Volume: O título de cada seção informa quantas repetidas você possui daquela seleção específica (ex: "Possuo 6 repetidas de Argentina").Detalhamento de Códigos: Internamente, o código exibe o identificador da figurinha e a quantidade de cópias disponíveis para troca, como POR2 (x2).📊 Regras de Negócio IntegradasO sistema respeita as variações de tamanho das coleções da Copa 2026:Coca-Cola (CC): Limitado a 14 cromos.FIFA World Cup History (FWC): Limitado a 19 cromos.Seleções Nacionais: Padronizadas em 20 cromos cada.🚀 Vantagens desta ImplementaçãoSincronização em Tempo Real: Qualquer alteração feita na aba de inventário atualiza instantaneamente as listas de faltantes e repetidas.Preparação para Trocas: Você pode abrir o aplicativo em um encontro de colecionadores e saber exatamente o que tem para oferecer apenas lendo os títulos dos expanders.Interface Limpa: O uso de componentes retráteis evita o excesso de informação (scroll infinito) na tela do celular ou computador.