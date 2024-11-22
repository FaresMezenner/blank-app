import streamlit as st
import requests

# ---- Barre Supérieure ----
st.markdown(
    """
    <style>
    .top-bar {
        background-color: #ed1a3a;
        padding: 10px 20px;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
    }
    .logo {
        max-height: 50px;
        margin-right: 20px;
    }
    </style>

    <div class="top-bar">
        <img src="https://companieslogo.com/img/orig/GLE.PA-96858a7b.svg?t=1720244492&download=true" alt="Logo de l'entreprise" class="logo"
        style="border: 2px solid white;"
        >
        <h2 style="color:white; margin:0;">Soumission de Documents</h2>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- Formulaire Principal ----
st.title("Formulaire de demande de crédit a la consommation")

# Champs de téléversement
uploaded_files = {}
file_descriptions = {
    "cert_nes": "Acte de naissance",
    "id_card": "Carte d'identité algérienne",
    "fishe_fam": "Fiche familiale (pour les clients mariés)",
    "fishe_ind": "Fiche individuelle (pour les clients célibataires)",
    "res": "Justificatif de domicile (e.g., certificat de résidence ou facture de service public)",
    "att_cnas": "Attestation d'affiliation à la CNAS",
    "empl_stat_fees": "État de frais (pour les employés, avec détails sur l'emploi et les revenus)",
    "empl_fishe_paies": "Bulletins de salaire des trois derniers mois",
    "empl_cdd": "Contrat à durée indéterminée (si disponible)",
    "lib_dec_fisc": "Dernière déclaration IRG (pour commerçants et travailleurs indépendants)",
    "lib_maj_casnon": "Extrait de mise à jour CASNOS (pour commerçants et travailleurs indépendants)",
    "lib_cp_bf1": "La dernière déclaration fiscale (pour commerçants et travailleurs indépendants)",
    "lib_cp_bf2": "L'avant-dernière déclaration fiscale",
    "lib_cp_bf3": "L'antépénultième déclaration fiscale",
    "ret_card": "Notification ou carte de retraite",
    "relv_compte": "Relevé de compte des six derniers mois (si non client SGA ou retraité)",
    "prf_add_inc": "Contrat de location notarié (valable >1 an)",
    "just_pre": "Facture pro forma pour les biens à acheter",
    "dem_signed": "Demande de crédit signée",
    "dem_cons": "Demande de consultation du centre des risques ménagers",
    "att_vend": "Certificat du vendeur pour un produit fabriqué en Algérie",
    "oth1": "Fichier supplémentaire CCP (modèle SGA)",
    "oth2": "Chèque barré CCP/banques (pour crédit AUTO)",
    "oth3": "Engagement de gage pour AUTO/MOTO PPO (>700,000DZD)",
    "oth4": "Engagement d’assurance tout risque (>700,000DZD pour motos)",
    "extra": "Fichier supplémentaire",
}

st.markdown("### Téléversez vos fichiers")
for file_key, file_desc in file_descriptions.items():
    uploaded_files[file_key] = st.file_uploader(file_desc, type=["pdf", "jpg", "jpeg", "png"])

# Champ Selfie
st.markdown("### Prenez un Selfie")
selfie = st.camera_input("Prenez une photo en direct (obligatoire)")

# Fonction pour envoyer les fichiers au backend
def envoyer_fichiers(api_url, fichiers, selfie):
    files = []

    # Ajouter les fichiers téléversés
    for cle, fichier in fichiers.items():
        if fichier is not None:
            files.append(("files", fichier.getvalue()))
    
    # Ajouter le selfie
    if selfie is not None:
        files.append(("files", selfie.getvalue()))
    
    try:
        response = requests.post(api_url, files=files)
        if response.status_code == 200:
            st.success("Fichiers envoyés avec succès !")
        else:
            st.error(f"Erreur lors de l'envoi : {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")

# Bouton de soumission
if st.button("Soumettre"):
    
    if selfie is None:
        st.error("Veuillez prendre un selfie avant de soumettre.")
    else:
        st.info("Envoi des fichiers...")
        api_endpoint = "https://docs-analyser.onrender.com/"  # Remplacez par votre URL API
        envoyer_fichiers(api_endpoint, uploaded_files, selfie)
