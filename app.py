import hashlib
import os
from datetime import date

from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def artwork_label(prompt):
    """Build a small, fictional museum record from a stable prompt-derived seed."""
    seed = int(hashlib.sha256(prompt.encode("utf-8")).hexdigest(), 16)
    artists = [
        ("Mara Vélasquez", "b. 1994, lives and works between Verdun and the cloud"),
        ("Theo Wren", "b. 1988, keeps a studio above a laundromat in Montréal"),
        ("Iris K. Bell", "b. 1997, works in borrowed rooms and temporary tabs"),
        ("Soren Vale", "b. 1991, lives with three plants and an unreliable scanner"),
    ]
    titles = ["Study for a Soft Machine", "The Afternoon Refused to End", "Untitled (After the Weather)", "Notes Toward a Brighter Room"]
    mediums = ["Pigment, aluminum, and borrowed light", "Polyester, elastic, fatigue", "Compressed atmosphere, pixels, and dust", "Oil, municipal memory, and a low battery"]
    dimensions = ["102.0 × 76.0 cm", "91.4 × 121.9 cm", "76.2 × 76.2 cm", "48.3 × 61.0 cm"]
    provenances = [
        "Found under a radiator, 2026; private collection of a dépanneur; acquired by the museum after a tense negotiation.",
        "Commissioned for an unfinished apartment, 2026; passed between two night-shift workers; acquired from the artist.",
        "Made during a cancelled residency, 2026; held briefly in a grocery-store office; museum purchase.",
        "Retrieved from a studio move, 2026; private collection, Toronto; promised gift to the museum.",
    ]
    theorists = [
        ("Lina Orphe", "The Tender Machinery"),
        ("Émile Rocher", "A Small Theory of Looking"),
        ("Naomi Voss", "The Weather Inside Images"),
        ("Pavel Senn", "Objects That Wait"),
    ]
    artist, bio = artists[seed % len(artists)]
    theorist, book = theorists[(seed >> 7) % len(theorists)]
    title = titles[(seed >> 13) % len(titles)]
    medium = mediums[(seed >> 19) % len(mediums)]
    size = dimensions[(seed >> 25) % len(dimensions)]
    provenance = provenances[(seed >> 31) % len(provenances)]
    year = date.today().year
    label = (
        f"This work stages an encounter between the prompt's private desire and the public choreography of display. "
        f"Its surfaces keep slipping between evidence and invention, asking the viewer to notice what has been made "
        f"legible and what remains just out of frame. As {theorist} writes in *{book}*, images can behave like rooms: "
        f"they hold us briefly while rearranging the terms of our attention. Here, texture becomes a record of hesitation, "
        f"and the composition turns looking into a small, deliberate act of care."
    )
    return {"artist": artist, "bio": bio, "title": title, "year": year, "medium": medium,
            "dimensions": size, "provenance": provenance, "credit_line": "Gift of the artist's backpack", "label": label}


@app.route("/", methods=["GET", "POST"])
def index():
    artwork = None
    error = None
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if not prompt:
            error = "Please describe the image you would like to place in the gallery."
        else:
            try:
                response = client.images.generate(model="gpt-image-1", prompt=prompt, size="1024x1024", quality="medium", output_format="png")
                artwork = artwork_label(prompt)
                artwork["image_url"] = f"data:image/png;base64,{response.data[0].b64_json}"
            except Exception as exc:
                error = f"The studio could not complete this edition: {exc}"
    return render_template("index.html", artwork=artwork, error=error)


if __name__ == "__main__":
    app.run(debug=True)
