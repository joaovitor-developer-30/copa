import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Copa 2026 - Master Control", layout="wide")

NOME_ARQUIVO_JSON = "meu_progresso_v2.json"

# --- FUNÇÕES DE BACKEND ---
def carregar_dados():
    try:
        if os.path.exists(NOME_ARQUIVO_JSON):
            with open(NOME_ARQUIVO_JSON, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        st.error("Erro ao carregar o arquivo JSON. Iniciando zerado.")
    return {}

def salvar_dados(dados):
    try:
        with open(NOME_ARQUIVO_JSON, "w") as f:
            json.dump(dados, f)
        st.sidebar.success("💾 Progresso salvo com sucesso!")
    except IOError:
        st.sidebar.error("Erro ao gravar no arquivo.")

if 'meu_album' not in st.session_state:
    st.session_state.meu_album = carregar_dados()

# --- ESTRUTURA DO ÁLBUM ---
selecoes = {
    "Fifa World Cup History": "FWC", "México": "MEX", "África do Sul": "RSA",
    "Coreia do Sul": "KOR", "Rep. Tcheca": "CZE", "Canadá": "CAN",
    "Bósnia": "BIH", "Catar": "QAT", "Suíça": "SUI", "Brasil": "BRA",
    "Marrocos": "MAR", "Haiti": "HAI", "Escócia": "SCO", "Estados Unidos": "USA",
    "Paraguai": "PAR", "Austrália": "AUS", "Turquia": "TUR", "Alemanha": "GER",
    "Curaçao": "CUW", "Costa do Marfim": "CIV", "Equador": "ECU", "Holanda": "NED",
    "Japão": "JPN", "Suécia": "SWE", "Tunísia": "TUN", "Bélgica": "BEL",
    "Egito": "EGY", "Irã": "IRN", "Nova Zelândia": "NZL", "Espanha": "ESP",
    "Cabo Verde": "CPV", "Arábia Saudita": "KSA", "Uruguai": "URU", "França": "FRA",
    "Senegal": "SEN", "Iraque": "IRQ", "Noruega": "NOR", "Argentina": "ARG",
    "Argélia": "ALG", "Áustria": "AUT", "Jordânia": "JOR", "Portugal": "POR",
    "Congo": "COD", "Uzbequistão": "UZB", "Colômbia": "COL", "Inglaterra": "ENG",
    "Croácia": "CRO", "Gana": "GHA", "Panamá": "PAN", "Coca-Cola": "CC"
}

st.title("⚽ Gerenciador de Cartas - Copa 2026")

aba_geral, aba_stats, aba_faltantes = st.tabs([
    "📋 Inventário & Repetidas", 
    "📊 Estatísticas e Progresso", 
    "🔍 Faltantes"
])

# --- ABA 1: GESTÃO MANUAL ---
with aba_geral:
    sel_nome = st.selectbox("Escolha a Seleção:", list(selecoes.keys()))
    sigla = selecoes[sel_nome]
    limite = 14 if sigla == "CC" else (19 if sigla == "FWC" else 20)

    st.subheader(f"Gerenciando: {sel_nome}")
    cols = st.columns(4)

    for n in range(1, limite + 1):
        cod = f"{sigla}{n}"
        qtd_atual = st.session_state.meu_album.get(cod, 0)
        
        with cols[(n-1)%4]:
            nova_qtd = st.number_input(f"Qtd {cod}", min_value=0, value=qtd_atual, key=f"nb_{cod}")
            st.session_state.meu_album[cod] = nova_qtd

# --- ABA 2: ESTATÍSTICAS E REPETIDAS (ATUALIZADA) ---
with aba_stats:
    st.header("📊 Resumo do Álbum")
    
    total_distintas = sum(1 for v in st.session_state.meu_album.values() if v > 0)
    total_repetidas = sum(max(0, v - 1) for v in st.session_state.meu_album.values())
    vagas_totais = sum(14 if s == "CC" else (19 if s == "FWC" else 20) for s in selecoes.values())
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Únicas Coladas", f"{total_distintas} / {vagas_totais}")
    c2.metric("Total de Repetidas", total_repetidas)
    c3.metric("Progresso %", f"{(total_distintas/vagas_totais)*100:.1f}%")

    st.divider()
    st.subheader("♻️ Figurinhas para Trocar")
    
    # Lógica de expanders para repetidas (conforme Captura de tela 2026-05-13 185526.png)
    tem_repetida = False
    for nome_sel, sigla in selecoes.items():
        limite = 14 if sigla == "CC" else (19 if sigla == "FWC" else 20)
        lista_extras = []
        
        for n in range(1, limite + 1):
            cod = f"{sigla}{n}"
            qtd = st.session_state.meu_album.get(cod, 0)
            if qtd > 1:
                lista_extras.append(f"{cod} (x{qtd-1})")
        
        if lista_extras:
            tem_repetida = True
            with st.expander(f"Possuo {len(lista_extras)} repetidas de {nome_sel}"):
                st.write(", ".join(lista_extras))

    if not tem_repetida:
        st.info("Você ainda não tem figurinhas repetidas.")

# --- ABA 3: FALTANTES (CONFORME Captura de tela 2026-05-13 185535.png) ---
with aba_faltantes:
    st.header("❌ O que falta para completar")
    
    faltam_alguma = False
    for nome_sel, sigla in selecoes.items():
        limite = 14 if sigla == "CC" else (19 if sigla == "FWC" else 20)
        lista_faltantes = []
        
        for n in range(1, limite + 1):
            cod = f"{sigla}{n}"
            if st.session_state.meu_album.get(cod, 0) == 0:
                lista_faltantes.append(cod)
        
        if lista_faltantes:
            faltam_alguma = True
            with st.expander(f"Faltam {len(lista_faltantes)} em {nome_sel}"):
                st.write(", ".join(lista_faltantes))
                
    if not faltam_alguma:
        st.success("🎉 Álbum completo!")

# --- SIDEBAR ---
if st.sidebar.button("💾 Salvar Tudo"):
    salvar_dados(st.session_state.meu_album)