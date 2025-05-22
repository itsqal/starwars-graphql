from database import get_db_connection, init_db

def seed_data():
    """Mengisi database dengan data awal Star Wars."""
    conn = get_db_connection()
    c = conn.cursor()

    # Bersihkan data lama
    c.execute("DELETE FROM character_starships")
    c.execute("DELETE FROM characters")
    c.execute("DELETE FROM starships")
    c.execute("DELETE FROM planets")
    c.execute("DELETE FROM species")
    c.execute("DELETE FROM factions")
    conn.commit()

    # Data planet
    planets = [
        ("Tatooine", "Arid", "Desert"),
        ("Alderaan", "Temperate", "Grasslands, Mountains"),
        ("Yavin IV", "Temperate, Humid", "Jungle, Rainforests"),
        ("Naboo", "Temperate", "Grassy Hills, Swamps"),
        ("Coruscant", "Temperate", "Cityscape"),
    ]
    c.executemany("INSERT INTO planets (name, climate, terrain) VALUES (?, ?, ?)", planets)
    planet_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM planets").fetchall()}

    # Data species
    species = [
        ("Human", 80, "Mammal", "Galactic Basic"),
        ("Droid", None, "Artificial", "Binary"),
        ("Wookiee", 400, "Mammal", "Shyriiwook"),
        ("Rodian", 20, "Reptilian", "Rodese"),
        ("Twi'lek", 70, "Mammal", "Twi'leki"),
    ]
    c.executemany("INSERT INTO species (name, average_lifespan, classification, language) VALUES (?, ?, ?, ?)", species)
    species_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM species").fetchall()}

    # Data factions
    factions = [
        ("Galactic Empire", "Authoritarian"),
        ("Rebel Alliance", "Democratic"),
        ("Jedi Order", "Peacekeeping"),
        ("Sith Order", "Authoritarian"),
        ("Bounty Hunters Guild", "Mercenary"),
    ]
    c.executemany("INSERT INTO factions (name, ideology) VALUES (?, ?)", factions)
    factions_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM factions").fetchall()}

    # Data karakter
    characters = [
        ("Luke Skywalker", species_ids["Human"], planet_ids["Tatooine"], factions_ids["Jedi Order"]),
        ("Leia Organa", species_ids["Droid"], planet_ids["Alderaan"], factions_ids["Rebel Alliance"]),
        ("Han Solo", species_ids["Human"], None, factions_ids["Rebel Alliance"]),
        ("C-3PO", species_ids["Droid"], None, factions_ids["Galactic Empire"]),
        ("Yoda", None, None, factions_ids["Jedi Order"]),
    ]
    c.executemany("INSERT INTO characters (name, species_id, home_planet_id, faction_id) VALUES (?, ?, ?, ?)", characters)
    character_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM characters").fetchall()}

    # Data kapal
    starships = [
        ("Millennium Falcon", "YT-1300 light freighter", "Corellian Engineering"),
        ("X-wing", "T-65 X-wing starfighter", "Incom Corporation"),
        ("TIE Fighter", "TIE/LN starfighter", "Sienar Fleet Systems"),
    ]
    c.executemany("INSERT INTO starships (name, model, manufacturer) VALUES (?, ?, ?)", starships)
    starship_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM starships").fetchall()}

    # Relasi karakter-kapal
    character_starships = [
        (character_ids["Han Solo"], starship_ids["Millennium Falcon"]),
        (character_ids["Luke Skywalker"], starship_ids["X-wing"]),
    ]
    c.executemany("INSERT INTO character_starships (character_id, starship_id) VALUES (?, ?)", character_starships)

    conn.commit()
    conn.close()
    print("Database berhasil diisi dengan data Star Wars!")

if __name__ == "__main__":
    init_db()  # Pastikan tabel ada
    seed_data()