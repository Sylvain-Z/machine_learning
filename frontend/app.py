import streamlit as st
import requests

# URL de l'API Flask
API_URL = 'http://localhost:5000/predict_price'

# Configuration de la page
st.set_page_config(page_title="Predicteur de prix d'avocats", page_icon="🥑")

st.title("Predicteur de prix d'avocats €🥑")

# Saisie des données par l'utilisateur
st.write("**Entrez les valeurs pour chaque caractéristique :**")
quality1 = st.number_input('Quality1', min_value=0.0, help="Example: 1036.74")
quality2 = st.number_input('Quality2', min_value=0.0, help="Example: 54454.85")
quality3 = st.number_input('Quality3', min_value=0.0, help="Example: 48.16")
small_bags = st.number_input('Small Bags', min_value=0.0, help="Example: 8603.62")
large_bags = st.number_input('Large Bags', min_value=0.0, help="Example: 93.25")
xlarge_bags = st.number_input('XLarge Bags', min_value=0.0, help="Example: 0.0")
year = st.number_input('Year', min_value=2000, max_value=2025, value=2015, help="Example: 2015")
type_ = st.selectbox('Type', ['conventional', 'organic'], help="Select avocado type")
region = st.selectbox('Region', [
    'Albany', 'Atlanta', 'BaltimoreWashington', 'Boise', 'Boston',
    'BuffaloRochester', 'California', 'Charlotte', 'Chicago',
    'Cincinnati', 'Columbus', 'DallasFtWorth', 'Denver', 'Detroit',
    'GrandRapids', 'GreatLakes', 'HarrisburgScranton', 'HartfordSpringfield',
    'Houston', 'Indianapolis', 'Jacksonville', 'LasVegas', 'LosAngeles',
    'Louisville', 'MiamiFtLauderdale', 'Midsouth', 'Nashville', 'NewOrleansMobile',
    'NewYork', 'Northeast', 'NorthernNewEngland', 'Orlando', 'Philadelphia',
    'PhoenixTucson', 'Pittsburgh', 'Plains', 'Portland', 'RaleighGreensboro',
    'RichmondNorfolk', 'Roanoke', 'Sacramento', 'SanDiego', 'SanFrancisco',
    'Seattle', 'SouthCarolina', 'SouthCentral', 'Southeast', 'Spokane',
    'StLouis', 'Syracuse', 'Tampa', 'TotalUS', 'West', 'WestTexNewMexico'
], help="Select region")

# Bouton de prédiction
if st.button("Prédire le prix"):
    input_data = {
        'Quality1': quality1,
        'Quality2': quality2,
        'Quality3': quality3,
        'Small Bags': small_bags,
        'Large Bags': large_bags,
        'XLarge Bags': xlarge_bags,
        'year': year,
        'type': type_,
        'region': region
    }
    
    try:
        response = requests.post(API_URL, json=input_data)
        response.raise_for_status()
        prediction = response.json().get('predicted_price', 'Erreur: clé non trouvée')
        st.success(f"Prix: {prediction:.2f}€")
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la requête : {e}")
    except ValueError:
        st.error("Erreur lors de la lecture de la réponse de l'API. Assurez-vous que l'API renvoie un JSON valide.")