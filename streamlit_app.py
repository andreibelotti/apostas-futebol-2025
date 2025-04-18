import streamlit as st
import pandas as pd
import os
from datetime import datetime

ARQUIVO_APOSTAS = "apostas.csv"
ARQUIVO_RESULTADOS = "resultados.csv"
DATA_LIMITE = "2025-05-01"

def carregar_apostas():
    if os.path.exists(ARQUIVO_APOSTAS):
        return pd.read_csv(ARQUIVO_APOSTAS)
    return pd.DataFrame()

def salvar_apostas(df):
    df.to_csv(ARQUIVO_APOSTAS, index=False)

def verificar_edicao(nome):
    df = carregar_apostas()
    if nome in df['Nome'].values:
        return df[df['Nome'] == nome].iloc[0]
    return None

def app():
    st.title("Apostas Brasileirão 2025")
    st.write("Preencha seus palpites abaixo. Você pode editar até 2 vezes antes do dia **01/05/2025**.")

    nome = st.text_input("Seu nome completo")
    if not nome:
        st.stop()

    aposta_existente = verificar_edicao(nome)
    edicoes = 0 if aposta_existente is None else aposta_existente['Edicoes']

    if edicoes >= 2:
        st.warning("Limite de 2 edições atingido para este nome.")
        st.stop()

    if datetime.today().date() > datetime.strptime(DATA_LIMITE, "%Y-%m-%d").date():
        st.warning("Prazo para enviar apostas expirado.")
        st.stop()

    time_coracao = st.selectbox("Seu time do coração", ["Atlético-MG", "Bahia", "Botafogo", "Corinthians", "Cruzeiro", "Flamengo", "Fluminense", "Fortaleza", "Grêmio", "Internacional", "Palmeiras", "Santos", "São Paulo", "Vasco", "Outros"])
    posicao_time = st.slider(f"Em qual posição o {time_coracao} vai terminar o Brasileirão?", 1, 20)

    campeao_br = st.text_input("Campeão Brasileiro")
    vice_br = st.text_input("Vice-campeão Brasileiro")
    g4 = st.text_area("G4 (4 times separados por vírgula)").split(",")
    artilheiro = st.text_input("Artilheiro do Brasileirão")
    craque = st.text_input("Craque do Brasileirão")
    revelacao = st.text_input("Revelação do Brasileirão")
    rebaixados = st.text_area("Rebaixados (4 times separados por vírgula)").split(",")

    copa_br = st.text_input("Campeão Copa do Brasil")
    libertadores = st.text_input("Campeão Libertadores")
    sula = st.text_input("Campeão Sul-Americana")
    champions = st.text_input("Campeão Champions League")
    super_mundial = st.text_input("Campeão Super Mundial")

    melhor_br = st.text_input("Time BR melhor colocado")
    pior_br = st.text_input("Time BR pior colocado")

    if st.button("Enviar/Atualizar Aposta"):
        nova_aposta = {
            "Nome": nome,
            "Time do Coração": time_coracao,
            "Posição do Seu Time": posicao_time,
            "Campeão BR": campeao_br,
            "Vice BR": vice_br,
            "G4": ",".join([t.strip() for t in g4]),
            "Artilheiro": artilheiro,
            "Craque": craque,
            "Revelação": revelacao,
            "Rebaixados": ",".join([t.strip() for t in rebaixados]),
            "Copa do Brasil": copa_br,
            "Libertadores": libertadores,
            "Sul-Americana": sula,
            "Champions": champions,
            "Super Mundial": super_mundial,
            "Melhor Time BR": melhor_br,
            "Pior Time BR": pior_br,
            "Edicoes": edicoes + 1,
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = carregar_apostas()
        df = df[df["Nome"] != nome]
        df = pd.concat([df, pd.DataFrame([nova_aposta])], ignore_index=True)
        salvar_apostas(df)
        st.success("Aposta salva com sucesso!")

    st.subheader("Ranking (pontuação será calculada depois)")
    df = carregar_apostas()
    st.dataframe(df.drop(columns=["Edicoes", "Data"]), use_container_width=True)

if __name__ == "__main__":
    app()