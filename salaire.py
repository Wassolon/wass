import streamlit as st
import pandas as pd
import numpy as np

# Fonction pour le calcul de la paie avec arrondi et taux distincts
def calculer_paie(dataframe):
    # Arrondir les heures et calculer le paiement pour le présentiel
    dataframe['Heures Arrondies (Présentiel)'] = np.ceil(dataframe['Heures Présentiel'])
    dataframe['Somme à Payer (Présentiel)'] = dataframe['Heures Arrondies (Présentiel)'] * dataframe['Taux Entrée Présentiel']
    dataframe['Heures Réelles (Présentiel)'] = np.floor(dataframe['Somme à Payer (Présentiel)'] / dataframe['Taux Sortie Présentiel']) + 1
    dataframe['Paiement Net (Présentiel)'] = dataframe['Heures Réelles (Présentiel)'] * dataframe['Taux Sortie Présentiel']

    # Arrondir les heures et calculer le paiement pour le télétravail
    dataframe['Heures Arrondies (Télétravail)'] = np.ceil(dataframe['Heures Télétravail'])
    dataframe['Somme à Payer (Télétravail)'] = dataframe['Heures Arrondies (Télétravail)'] * dataframe['Taux Entrée Télétravail']
    dataframe['Heures Réelles (Télétravail)'] = np.floor(dataframe['Somme à Payer (Télétravail)'] / dataframe['Taux Sortie Télétravail']) + 1
    dataframe['Paiement Net (Télétravail)'] = dataframe['Heures Réelles (Télétravail)'] * dataframe['Taux Sortie Télétravail']

    # Calculer le total à payer en ajoutant les paiements du présentiel et du télétravail
    dataframe['Total à Payer'] = dataframe['Paiement Net (Présentiel)'] + dataframe['Paiement Net (Télétravail)']

    return dataframe

# Créer un DataFrame vide
data = {
    'Prénom': [],
    'Nom': [],
    'Heures Présentiel': [],
    'Heures Télétravail': [],
    'Taux Entrée Présentiel': [],
    'Taux Entrée Télétravail': [],
    'Taux Sortie Présentiel': [],
    'Taux Sortie Télétravail': []
}
df = pd.DataFrame(data)

# Interface utilisateur pour ajouter des employés
st.title('Calcul de la paie des employés avec gestion distincte des heures en présentiel et en télétravail// TRA-DICTION')

with st.form("employee_form"):
    prenom = st.text_input('Prénom de l\'employé')
    nom = st.text_input('Nom de l\'employé')
    heures_presentiel = st.number_input('Heures en présentiel', min_value=0.0, format="%.2f")
    heures_teletravail = st.number_input('Heures en télétravail', min_value=0.0, format="%.2f")
    taux_entree_presentiel = st.number_input('Taux horaire d\'entrée en présentiel', value=20.00, format="%.2f")
    taux_entree_teletravail = st.number_input('Taux horaire d\'entrée en télétravail', value=15.00, format="%.2f")
    taux_sortie_presentiel = st.number_input('Taux horaire de sortie en présentiel', value=12.00, format="%.2f")
    taux_sortie_teletravail = st.number_input('Taux horaire de sortie en télétravail', value=10.00, format="%.2f")
    submit_button = st.form_submit_button("Ajouter l'employé")
    if submit_button:
        new_data = {
            'Prénom': [prenom],
            'Nom': [nom],
            'Heures Présentiel': [heures_presentiel],
            'Heures Télétravail': [heures_teletravail],
            'Taux Entrée Présentiel': [taux_entree_presentiel],
            'Taux Entrée Télétravail': [taux_entree_teletravail],
            'Taux Sortie Présentiel': [taux_sortie_presentiel],
            'Taux Sortie Télétravail': [taux_sortie_teletravail]
        }
        new_df = pd.DataFrame(new_data)
        df = pd.concat([df, new_df], ignore_index=True)

# Bouton pour calculer la paie pour tous les employés
if st.button('Calculer la paie pour tous les employés'):
    result_df = calculer_paie(df)
    st.write(result_df[['Prénom', 'Nom', 'Total à Payer']])
