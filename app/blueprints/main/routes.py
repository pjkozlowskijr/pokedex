from flask import render_template, request, flash
import requests
from .forms import PokeLookupForm
from flask_login import login_required
from .import bp as main

@main.route("/", methods=["GET"])
def index():
    return render_template("index.html.j2")

@main.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    form = PokeLookupForm()
    if request.method == "POST":
        pokemon = form.poke_name.data.lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = requests.get(url)
        if not response.ok:
            flash("There was an error, most likely because the Pokemon you entered does not exist. Please try again.", "danger")
            return render_template("lookup.html.j2", form=form)
        if not response.json():
            flash("There was an unexpected error. Please try again.", "danger")
            return render_template("lookup.html.j2", form=form)
        poke_data = response.json()
        pokemon_dict = {
            "name": poke_data["species"]["name"],
            "sprite": poke_data["sprites"]["other"]["home"]["front_default"],
            "base_experience": poke_data["base_experience"],
            "ability_name": poke_data["abilities"][0]["ability"]["name"],
            "attack_base": poke_data["stats"][1]["base_stat"],
            "hp_base": poke_data["stats"][0]["base_stat"],
            "defense_base":poke_data["stats"][2]["base_stat"],
        }
        return render_template("lookup.html.j2", pokemon_table=pokemon_dict, form=form)
    return render_template("lookup.html.j2", form=form)
