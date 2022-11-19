import collections
from datetime import time

import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import random

st.set_page_config(
    page_title="Pokedex!",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
# adding first generation to selectbox
count = 0
pkmn_list = []

url = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=151"
response = requests.get(url).json()


for i in response["results"]:
    pkmn_list.append(i["name"])

st.title("Unofficial Pokédex!")
sidebar = st.sidebar.selectbox(
    "Features",
    ["Pokedex", "Interactive Table", "Pokemon GO Regional Spawn Locations", "Pokemon Trivia","Type Chart", "Look-a-like"]
)

if sidebar == "Pokedex":
    input = st.selectbox(
        "Type in a Pokémon to learn about them!",
        pkmn_list
    )

    if not input:
        exit()
    # access to pokemon data
    url2 = "https://pokeapi.co/api/v2/pokemon/" + input
    response2 = requests.get(url2).json()

    col1, col2 = st.columns(2)

    with col1:
        # getting picture of pokemon
        sprites = response2["sprites"]
        other = sprites["other"]
        official_artwork = other["official-artwork"]
        sprite_url = official_artwork["front_default"]
        st.image(sprite_url, width=180)

        # geting stats of pokemon
        baseStat_data = []
        for i in response2["stats"]:
            base_stat = i["base_stat"]
            baseStat_data.append(base_stat)
        st.subheader("Base Stats")

        data = pd.DataFrame({
            'Value': baseStat_data,
            'Base Stat': ["HP", "Attack", "Defense",
                          "Special Attack", "Special Defense", "Speed"]
        })

        bar_chart = alt.Chart(data).mark_bar().encode(
            y='Value:Q',
            x='Base Stat:O',
        )
        st.altair_chart(bar_chart, use_container_width=True)

    with col2:
        type_list = []
        for i in response2["types"]:
            type = i["type"]
            type_list.append(type["name"])

        ability_list = []
        for i in response2["abilities"]:
            ability = i["ability"]
            ability_list.append(ability["name"])

        info_selected = st.radio(
            "Show Specific Pokemon Info",
            ('Weight/Height', 'Types', 'Abilities'))

        if info_selected == 'Weight/Height':
            st.write("Height: " + (str(response2["height"] /10)) + " m")
            st.write("Weight: " + (str(response2["weight"] /10)) + " kg")
        elif info_selected == 'Types':
                st.write("Type(s): " + ', '.join(type_list))
        else:
                st.write("Abilities: " + ', '.join(ability_list))

        if st.button("Hear Pokemon Sound"):
            st.audio("https://play.pokemonshowdown.com/audio/cries/"+input.lower()+".mp3", format='media/mp3')

if sidebar == "Pokemon GO Regional Spawn Locations":

    map_pkmn_list = []

    for i in response["results"]:
        if i["name"] in ('tauros', 'mr-mime', 'kangaskhan', 'farfetchd'):
            map_pkmn_list.append(i["name"])

    map_input = st.selectbox(
        "Type in a Pokémon to see where they spawn!",
        map_pkmn_list
    )

    PokeRegion_map = st.checkbox("See all the Pokémon regions on the map")

    if PokeRegion_map:
        if map_input == 'tauros':
            map_data = pd.DataFrame(
                np.array([[37.288426064651574, -95.77779794352075],
                          [37.420963291485512, -95.75930714466599],
                          [37.36105501657613, -95.6803010041048],
                          [37.562692632583683, -95.60045437268656],
                          [37.166521386048824, -95.7542641995238]]),
                columns=['lat', 'lon'])
        elif map_input == 'mr-mime':
            map_data = pd.DataFrame(
                np.array([[46.288426064651574, 1.77779794352075],
                          [46.320963291485512, 1.75930714466599],
                          [46.36105501657613, 1.6803010041048],
                          [46.262692632583683, 1.60045437268656],
                          [46.166521386048824, 1.7542641995238]]),
                columns=['lat', 'lon'])
        elif map_input == 'kangaskhan':
            map_data = pd.DataFrame(
                np.array([[-25.288426064651574, 133.77779794352075],
                          [-25.320963291485512, 133.75930714466599],
                          [-25.36105501657613, 133.6803010041048],
                          [-25.262692632583683, 133.60045437268656],
                          [-25.166521386048824, 133.7542641995238]]),
                columns=['lat', 'lon'])
        elif map_input == 'farfetchd':
            map_data = pd.DataFrame(
                np.array([[34.288426064651574, 100.77779794352075],
                          [34.320963291485512, 100.75930714466599],
                          [34.36105501657613, 100.6803010041048],
                          [34.262692632583683, 100.60045437268656],
                          [34.166521386048824, 100.7542641995238]]),
                columns=['lat', 'lon'])
        col1,col2 = st.columns(2)
        with col1:
            st.map(map_data)

        with col2:
            url5 = "https://pokeapi.co/api/v2/pokemon/"+map_input
            response5 = requests.get(url5).json()
            sprites = response5["sprites"]
            other = sprites["other"]
            official_artwork = other["official-artwork"]
            sprite_url = official_artwork["front_default"]
            st.image(sprite_url, width=300)

if sidebar == "Interactive Table":
    input = st.selectbox(
        "Type in a Pokémon to learn what moves they can learn!",
        pkmn_list
    )

    if not input:
        exit()
    # access to pokemon data
    url2 = "https://pokeapi.co/api/v2/pokemon/" + input
    response2 = requests.get(url2).json()
    sprites = response2["sprites"]
    other = sprites["other"]
    official_artwork = other["official-artwork"]
    sprite_url = official_artwork["front_default"]
    st.image(sprite_url, width=180)
    interactive_table_data = []
    levelL = []
    moveL = []
    accuracyL = []
    powerL = []
    categoryL = []
    typeL = []

    for i in response2["moves"]:
        for j in i["version_group_details"]:
            move_learn_method = j["move_learn_method"]
            version_group = j["version_group"]
            if move_learn_method["name"] == "level-up" and version_group["name"] == "sun-moon":
                move = i["move"]
                interactive_table_data.append(
                    {'name': move["name"],
                     'level_learned_at': j["level_learned_at"],
                     'url': move["url"]})

    for i in interactive_table_data:
        res = requests.get(i["url"]).json()
        damage_class = res["damage_class"]
        mtype = res["type"]
        levelL.append(i["level_learned_at"])
        moveL.append(i["name"].replace('-', ' ').title())
        accuracyL.append(res["accuracy"])
        powerL.append(res["power"])
        categoryL.append(damage_class["name"].capitalize())
        typeL.append(mtype["name"].capitalize())

        # setting color based on type


    def typeColor(val):
        if val == 'Normal':
            color = 'darkkhaki'
            return 'background-color: %s' % color
        elif val == 'Fire':
            color = 'darkorange'
            return 'background-color: %s' % color
        elif val == 'Water':
            color = 'cornflowerblue'
            return 'background-color: %s' % color
        elif val == 'Grass':
            color = 'limegreen'
            return 'background-color: %s' % color
        elif val == 'Electric':
            color = 'gold'
            return 'background-color: %s' % color
        elif val == 'Ice':
            color = 'paleturquoise'
            return 'background-color: %s' % color
        elif val == 'Fighting':
            color = 'darkred'
            return 'background-color: %s' % color
        elif val == 'Poison':
            color = 'darkmagenta'
            return 'background-color: %s' % color
        elif val == 'Ground':
            color = 'wheat'
            return 'background-color: %s' % color
        elif val == 'Flying':
            color = 'slateblue'
            return 'background-color: %s' % color
        elif val == 'Psychic':
            color = 'deeppink'
            return 'background-color: %s' % color
        elif val == 'Bug':
            color = 'yellowgreen'
            return 'background-color: %s' % color
        elif val == 'Rock':
            color = 'darkgoldenrod'
            return 'background-color: %s' % color
        elif val == 'Ghost':
            color = 'darkslateblue'
            return 'background-color: %s' % color
        elif val == 'Dark':
            color = 'saddlebrown'
            return 'background-color: %s' % color
        elif val == 'Dragon':
            color = 'indigo'
            return 'background-color: %s' % color
        elif val == 'Steel':
            color = 'lightsteelblue'
            return 'background-color: %s' % color
        elif val == 'Fairy':
            color = 'lightpink'
            return 'background-color: %s' % color
        else:
            return


    df = pd.DataFrame(
        {'Lvl.': levelL, 'Move': moveL, 'Type': typeL, 'Cat.': categoryL, 'Power': powerL, 'Accuracy': accuracyL})
    df = df.sort_values('Lvl.')
    df = df.replace(np.nan, 0, regex=True)
    df[['Power', 'Accuracy']] = df[['Power', 'Accuracy']].astype(int)
    df = df.replace(0, '—', regex=True)

    st.write(df.style.applymap(typeColor, subset='Type'))

if sidebar == "Pokemon Trivia":
    st.subheader("Welcome to Pokemon Trivia")

    url3 = "https://pokeapi.co/api/v2/pokemon/"+ str(random.randint(1,150))
    response3 = requests.get(url3).json()
    pkmnType_list = []
    types = response3['types']
    for i in types:
        type = i['type']
        pkmnType_list.append(type['name'].capitalize())
    if 'pokemon' not in st.session_state:
        st.session_state['pokemon'] = response3["name"]
    if 'pokemonType' not in st.session_state:
        st.session_state['pokemonType'] = pkmnType_list

    sprites = response3['sprites']
    other = sprites["other"]
    official_artwork = other["official-artwork"]
    sprite_url = official_artwork["front_default"]
    st.image(sprite_url, width=180)
    form = st.form("my_form")
    pokemon_name_answer_input = form.text_input("Name that Pokemon!")
    if pokemon_name_answer_input:
        if pokemon_name_answer_input.lower() == st.session_state['pokemon']:
            form.success("correct!")
            del st.session_state.pokemon
        else:
            form.error("The correct answer was "+st.session_state['pokemon'])
            del st.session_state.pokemon

    pokemon_type_answer_input = form.multiselect("Which type pokemon is this?",
                   ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground",
                    "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dark", "Dragon", "Steel", "Fairy"])

    form.form_submit_button("Submit")

    if len(pokemon_type_answer_input) > 0:
        if collections.Counter(pokemon_type_answer_input) == collections.Counter(st.session_state['pokemonType']):
            form.success("correct!")
        else:
            form.error("The correct answer was " + str(st.session_state['pokemonType']))
        del st.session_state.pokemonType


    if 'pokemon' not in st.session_state:
        st.session_state['pokemon'] = response3["name"]
    if 'pokemonType' not in st.session_state:
        st.session_state['pokemonType'] = pkmnType_list

if sidebar == "Type Chart":

    type_list = {
        'normal': 0,
        'water': 0,
        'fire': 0,
        'grass': 0,
        'electric': 0,
        'ice': 0,
        'fighting': 0,
        'flying': 0,
        'poison': 0,
        'rock': 0,
        'psychic': 0,
        'fairy': 0,
        'steel': 0,
        'dark': 0,
        'bug': 0,
        'ghost': 0,
        'dragon': 0,
        'ground': 0
    }
    for i in response["results"]:
        url4 = "https://pokeapi.co/api/v2/pokemon/" + i["name"]
        response4 = requests.get(url4).json()
        for j in response4["types"]:
            ptype = j["type"]
            type_list[ptype["name"]] += 1

    data = pd.DataFrame({
        'Amount': [type_list['normal'],
                   type_list['water'],
                   type_list['fire'],
                   type_list['grass'],
                   type_list['electric'],
                   type_list['ice'],
                   type_list['fighting'],
                   type_list['flying'],
                   type_list['poison'],
                   type_list['rock'],
                   type_list['psychic'],
                   type_list['fairy'],
                   type_list['steel'],
                   type_list['dark'],
                   type_list['bug'],
                   type_list['ghost'],
                   type_list['dragon'],
                   type_list['ground']],
        'Types': ["Normal", "Water", "Fire", "Grass", "Electric", "Ice", "Fighting", "Flying", "Poison", "Rock",
                  "Psychic", "Fairy", "Steel", "Dark", "Bug", "Ghost", "Dragon", "Ground"]
    })

    bar_chart = alt.Chart(data).mark_bar().encode(
        y='Amount:Q',
        x='Types:O',
    )
    st.altair_chart(bar_chart, use_container_width=True)

if sidebar == "Look-a-like":
    uploaded_file = st.file_uploader("Upload a picture of yourself to find your look a like", type=['png', 'jpg'])
    if uploaded_file is not None:

        col1,col2 = st.columns(2)
        bytes_data = uploaded_file.getvalue()
        st.balloons()
        with col1:
            st.image(bytes_data, width=300) #prints first image
        url3 = "https://pokeapi.co/api/v2/pokemon/" + str(random.randint(1, 150))
        response3 = requests.get(url3).json()
        sprites = response3["sprites"]
        other = sprites["other"]
        official_artwork = other["official-artwork"]
        sprite_url = official_artwork["front_default"]
        with col2:
            st.image(sprite_url, width=300) #prints second image
