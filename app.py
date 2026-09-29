import os
import streamlit as st
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Cadastro de carros", page_icon="🚘")
load_dotenv()
CAMINHO_CREDENCIAL = os.getenv("FIREBASE_CREDENTIALS_PATH")

@st.cache_resource
def conectar_firebase(caminho_credencial):
    if not firebase_admin._apps:
        cred = credentials.Certificate(caminho_credencial)
        firebase_admin.initialize_app(cred)
    return firestore.client()

if not CAMINHO_CREDENCIAL:
    st.error("Erro: Variável FIREBASE_CREDENTIALS_PATH não configurada no arquivo .env.")
    st.stop()

try:
    db = conectar_firebase(CAMINHO_CREDENCIAL)
except Exception as e:
    st.error(f"Erro ao conectar com o Firebase: {e}")
    st.stop()

st.title("🚘 Cadastro de carros")
st.caption("Conectado ao Firestore do Firebase")

aba_vendedores, aba_compradores, aba_cadastro, aba_lista, aba_consulta = st.tabs(
    ["🧑‍💼 Vendedores", "🧑‍💻 Compradores", "➕ Cadastrar", "📋 Carros cadastrados", "🔎 Consultar"]
)

# VENDEDORES
with aba_vendedores:
    with st.form("form_vendedor", clear_on_submit=True):
        nome = st.text_input("Nome do vendedor")
        idade = st.number_input("Idade", min_value=18, max_value=120, step=1)

        if st.form_submit_button("Cadastrar"):
            if nome.strip():
                db.collection("Vendedores").add({"nome": nome.strip(), "idade": int(idade)})
                st.success(f"Vendedor '{nome}' cadastrado!")
            else:
                st.warning("Informe o nome.")

# COMPRADORES
with aba_compradores:
    with st.form("form_comprador", clear_on_submit=True):
        nome = st.text_input("Nome do comprador")
        idade = st.number_input("Idade", min_value=18, max_value=120, step=1)

        if st.form_submit_button("Cadastrar"):
            if nome.strip():
                db.collection("Compradores").add({"nome": nome.strip(), "idade": int(idade)})
                st.success(f"Comprador '{nome}' cadastrado!")
            else:
                st.warning("Informe o nome.")

# CADASTRO
with aba_cadastro:
    with st.form("form_carro", clear_on_submit=True):
        nome = st.text_input("Nome do carro")
        valor = st.number_input("Valor", min_value=0, max_value=10000000000, step=1)

        if st.form_submit_button("Cadastrar"):
            if nome.strip():
                db.collection("carros").add({"nome": nome.strip(), "valor": int(valor)})
                st.success(f"Carro '{nome}' cadastrado!")
            else:
                st.warning("Informe o nome.")

# LISTA
with aba_lista:
    if st.button("🔄 Atualizar lista"):
        st.rerun()

    carros = [{"id": d.id, **d.to_dict()} for d in db.collection("carros").stream()]

    if not carros:
        st.info("Nenhum carro cadastrado.")

    for carro in carros:
        col1, col2, col3, col4 = st.columns([4, 3, 1, 1])
        col1.write(f"*{carro.get('nome', '—')}*")
        col2.write(f"{carro.get('valor', '—')} reais")

        if col4.button("🗑️", key=carro["id"]):
            db.collection("carros").document(carro["id"]).delete()
            st.rerun()

# CONSULTA
with aba_consulta:
    st.subheader("🧑‍💼 Vendedores")

    vendedores = [{"id": d.id, **d.to_dict()} for d in db.collection("Vendedores").stream()]

    for vendedor in vendedores:
        col1, col2, col3 = st.columns([4, 3, 1])
        col1.write(f"*{vendedor.get('nome', '—')}*")
        col2.write(f"{vendedor.get('idade', '—')} anos")

    st.divider()

    st.subheader("🧑‍💻 Compradores")

    compradores = [{"id": d.id, **d.to_dict()} for d in db.collection("Compradores").stream()]

    for comprador in compradores:
        col1, col2, col3 = st.columns([4, 3, 1])
        col1.write(f"*{comprador.get('nome', '—')}*")
        col2.write(f"{comprador.get('idade', '—')} anos")