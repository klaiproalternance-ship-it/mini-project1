import streamlit as st
import requests
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="DevOps Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom styles for a premium look
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    h1 {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 4px;
        color: #94a3b8;
        font-weight: 600;
        border: 1px solid #334155;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6366f1 !important;
        color: white !important;
        border-color: #6366f1 !important;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_URL = "http://localhost:8000"

st.title("📊 DevOps Monitoring Dashboard")

# Initialize session state for charts
if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []
if "memory_history" not in st.session_state:
    st.session_state.memory_history = []

# Define Tabs
tab1, tab2 = st.tabs(["🖥️ Métriques Système", "🔌 Gestion des Serveurs"])

# Tab 1: System Metrics
with tab1:
    st.write("### Métriques en Temps Réel de l'Hôte")
    
    # Placeholders for live updates
    metric_placeholder = st.empty()
    chart_placeholder = st.empty()
    
    # Cache data fetching with 2 second TTL
    @st.cache_data(ttl=2)
    def fetch_metrics():
        try:
            r = requests.get(f"{API_URL}/metrics", timeout=1.5)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    metrics = fetch_metrics()
    
    if metrics:
        cpu = metrics["cpu_percent"]
        mem = metrics["memory_percent"]
        mem_gb = metrics["memory_used_gb"]
        disk = metrics["disk_percent"]
        
        # Add to history
        st.session_state.cpu_history.append(cpu)
        st.session_state.memory_history.append(mem)
        
        # Keep only the last 60 points
        st.session_state.cpu_history = st.session_state.cpu_history[-60:]
        st.session_state.memory_history = st.session_state.memory_history[-60:]
        
        # Render metrics cards
        with metric_placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Processeur (CPU)", f"{cpu} %")
            col2.metric("Mémoire vive (RAM)", f"{mem} %", f"{mem_gb} GB utilisé")
            col3.metric("Disque principal", f"{disk} %")
            
        # Render line chart
        with chart_placeholder.container():
            st.write("#### Historique des métriques (Dernières 60 secondes)")
            chart_df = pd.DataFrame({
                "CPU (%)": st.session_state.cpu_history,
                "Mémoire (%)": st.session_state.memory_history
            })
            st.line_chart(chart_df)
    else:
        st.warning("Impossible de se connecter à l'API backend sur http://localhost:8000. Assurez-vous que le serveur FastAPI est démarré.")

# Tab 2: Servers Management
with tab2:
    st.write("### Liste des Serveurs Surveillés")
    
    # Cache servers fetching with 5 second TTL
    @st.cache_data(ttl=5)
    def fetch_servers():
        try:
            r = requests.get(f"{API_URL}/servers", timeout=2.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return []
        
    servers = fetch_servers()
    
    if servers:
        # Style status cells for visualization
        df = pd.DataFrame(servers)
        df = df[["id", "name", "host", "port", "status"]]
        
        def color_status(val):
            if val == "UP":
                return "background-color: rgba(16, 185, 129, 0.2); color: #10b981; font-weight: bold;"
            elif val == "DEGRADED":
                return "background-color: rgba(245, 158, 11, 0.2); color: #f59e0b; font-weight: bold;"
            elif val == "DOWN":
                return "background-color: rgba(239, 68, 68, 0.2); color: #ef4444; font-weight: bold;"
            return "color: #94a3b8;"

        try:
            styled_df = df.style.map(color_status, subset=["status"])
            st.dataframe(styled_df, use_container_width=True)
        except Exception:
            st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun serveur enregistré pour le moment.")
        
    st.write("---")
    
    # Registration form
    col_form, col_check = st.columns(2)
    
    with col_form:
        with st.form("add_server_form", clear_on_submit=True):
            st.write("#### ➕ Enregistrer un nouveau serveur")
            srv_name = st.text_input("Nom du serveur", placeholder="Webserver Production")
            srv_host = st.text_input("Hôte / IP", value="127.0.0.1")
            srv_port = st.number_input("Port", min_value=1, max_value=65535, value=80)
            srv_key = st.text_input("Clé API", type="password", value="dev-secret-key")
            
            submit_btn = st.form_submit_button("Ajouter le serveur")
            if submit_btn:
                if not srv_name or not srv_host:
                    st.error("Le nom et l'hôte sont obligatoires.")
                else:
                    payload = {
                        "name": srv_name,
                        "host": srv_host,
                        "port": int(srv_port)
                    }
                    headers = {"X-API-Key": srv_key}
                    try:
                        r = requests.post(f"{API_URL}/servers", json=payload, headers=headers, timeout=2.0)
                        if r.status_code == 201:
                            st.success(f"Serveur '{srv_name}' ajouté avec succès !")
                            st.cache_data.clear() # Force reload
                            time.sleep(1)
                            st.rerun()
                        elif r.status_code == 403:
                            st.error("Clé API invalide ou manquante.")
                        else:
                            st.error(f"Erreur API ({r.status_code}) : {r.text}")
                    except Exception as e:
                        st.error(f"Erreur de connexion : {e}")

    with col_check:
        st.write("#### ⚡ Actions rapides")
        if servers:
            server_names = [s["name"] for s in servers]
            selected_srv_name = st.selectbox("Sélectionner un serveur", server_names)
            selected_srv = next(s for s in servers if s["name"] == selected_srv_name)
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("Vérifier la santé 📡"):
                    try:
                        r = requests.post(f"{API_URL}/servers/{selected_srv['id']}/check", timeout=2.0)
                        if r.status_code == 200:
                            st.info("Vérification de santé lancée en arrière-plan.")
                            st.cache_data.clear()
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Impossible de lancer la vérification.")
                    except Exception as e:
                        st.error(f"Erreur : {e}")
                        
            with col_btn2:
                srv_del_key = st.text_input("Clé API pour suppression", type="password", value="dev-secret-key", key="del_key")
                if st.button("Supprimer le serveur 🗑️"):
                    headers = {"X-API-Key": srv_del_key}
                    try:
                        r = requests.delete(f"{API_URL}/servers/{selected_srv['id']}", headers=headers, timeout=2.0)
                        if r.status_code == 200:
                            st.success(f"Serveur '{selected_srv['name']}' supprimé.")
                            st.cache_data.clear()
                            time.sleep(1)
                            st.rerun()
                        elif r.status_code == 403:
                            st.error("Clé API invalide.")
                        else:
                            st.error(f"Erreur : {r.text}")
                    except Exception as e:
                        st.error(f"Erreur : {e}")
        else:
            st.info("Enregistrez d'abord un serveur pour afficher les actions rapides.")

# Auto-rerun loop if we are currently looking at Tab 1
# Streamlit rerun sleep to keep the loop CPU friendly
time.sleep(2)
st.rerun()
