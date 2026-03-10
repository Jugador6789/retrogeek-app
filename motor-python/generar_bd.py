import sqlite3
import random

def construir_base_datos():
    print("Iniciando la construcción MASIVA de la base de datos RetroGeek (Portable)...")
    conexion = sqlite3.connect("tienda_retrogeek.db")
    cursor = conexion.cursor()

    # 1. Limpiar tablas existentes
    cursor.executescript("""
        DROP TABLE IF EXISTS biblioteca;
        DROP TABLE IF EXISTS resenas;
        DROP TABLE IF EXISTS requisitos;
        DROP TABLE IF EXISTS juegos;
    """)

    # 2. Crear estructura relacional completa
    cursor.executescript("""
        CREATE TABLE juegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            precio REAL NOT NULL,
            imagen_url TEXT,
            puntuacion REAL,
            desarrollador TEXT,
            tag TEXT,
            descripcion TEXT,
            video_url TEXT
        );
        CREATE TABLE requisitos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            juego_id INTEGER,
            tipo TEXT,
            cpu TEXT,
            gpu TEXT,
            ram_gb INTEGER,
            FOREIGN KEY(juego_id) REFERENCES juegos(id)
        );
        CREATE TABLE resenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            juego_id INTEGER,
            usuario TEXT,
            comentario TEXT,
            estrellas INTEGER,
            FOREIGN KEY(juego_id) REFERENCES juegos(id)
        );
        CREATE TABLE biblioteca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            juego_id INTEGER,
            fecha_adquisicion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(juego_id) REFERENCES juegos(id)
        );
    """)

    # 3. MEGA LISTA DE JUEGOS (Nuevos IDs de YouTube: Reseñas de IGN, Gameplays y PC Benchmarks sin restricción)
    lista_juegos = [
        # --- SHOOTERS Y ACCIÓN ---
        (730, "Counter-Strike 2", 0.00, 4.5, "Valve", 2, "Shooter", "n0roXLEraJw"), # Oficial Launch
        (1172470, "Apex Legends", 0.00, 4.3, "Respawn", 2, "Shooter", "oWbFOhQ-vJw"), # Oficial Launch
        (359550, "Rainbow Six Siege", 399.00, 4.5, "Ubisoft", 2, "Shooter", "6wlvYh0hhc0"),
        (1085660, "Destiny 2", 0.00, 4.2, "Bungie", 2, "Shooter", "jyPnQw_Lqto"),
        (578080, "PUBG: BATTLEGROUNDS", 0.00, 4.0, "KRAFTON", 2, "Shooter", "4rG9noTfb4A"),
        (379720, "DOOM", 399.00, 4.8, "id Software", 2, "Shooter", "RO90omga8D4"), # Gameplay sin restriccion
        (782330, "DOOM Eternal", 799.00, 4.9, "id Software", 3, "Shooter", "FkklG9MA0vM"),
        (1240440, "Halo Infinite", 0.00, 4.1, "343 Industries", 3, "Shooter", "PyMlV5_HRWk"),
        (1238810, "Battlefield V", 799.00, 4.2, "DICE", 3, "Shooter", "a7ZpQadiyqs"),
        (1237970, "Titanfall 2", 599.00, 4.9, "Respawn", 2, "Shooter", "EXwdWuSuiEA"),
        (49520, "Borderlands 2", 399.00, 4.8, "Gearbox", 1, "Shooter", "VW7qO_WP6D4"),
        (397540, "BioShock Infinite", 599.00, 4.8, "Irrational Games", 2, "Shooter", "bLHW78X1XeE"),
        (550, "Left 4 Dead 2", 123.99, 4.9, "Valve", 1, "Shooter", "9XIle_kLUpU"),
        (220, "Half-Life 2", 123.99, 4.9, "Valve", 1, "Shooter", "ID1dWN3nbLc"),
        (222880, "Insurgency", 299.00, 4.4, "New World", 1, "Shooter", "S1E4G-47HVM"),
        (581320, "Insurgency: Sandstorm", 599.00, 4.5, "New World", 3, "Shooter", "N-iFbsb6v3k"),
        (594650, "Hunt: Showdown", 799.00, 4.3, "Crytek", 3, "Shooter", "JbLMTl2GgT0"),
        (393380, "Squad", 999.00, 4.5, "Offworld Industries", 3, "Shooter", "fVqC4x1x9L8"),
        (686810, "Hell Let Loose", 899.00, 4.4, "Team17", 3, "Shooter", "Rj_1u7VbYI8"),
        (2357570, "Overwatch 2", 0.00, 3.5, "Blizzard", 2, "Shooter", "dZl1yGUetjI"),
        (1361210, "Warhammer 40K: Darktide", 799.00, 4.1, "Fatshark", 4, "Shooter", "HC42d1x4l6o"),
        (2535960, "Helldivers 2", 799.00, 4.7, "Arrowhead", 3, "Shooter", "wR0-3o_0eKk"),
        (230410, "Warframe", 0.00, 4.8, "Digital Extremes", 2, "Shooter", "1k_LOMiW4L8"),
        (440, "Team Fortress 2", 0.00, 4.9, "Valve", 1, "Shooter", "h_c3iQImXZg"),

        # --- MUNDO ABIERTO & RPG ---
        (271590, "Grand Theft Auto V", 599.00, 4.8, "Rockstar Games", 2, "Mundo Abierto", "HqZXw5M6qQY"), # IGN Review
        (1174180, "Red Dead Redemption 2", 1299.00, 4.9, "Rockstar Games", 3, "Mundo Abierto", "HVRzx17WHVk"), # IGN Review
        (1091500, "Cyberpunk 2077", 1299.00, 4.6, "CD PROJEKT RED", 4, "RPG", "V8z0E9R5p-E"), # IGN Review
        (292030, "The Witcher 3: Wild Hunt", 799.00, 4.9, "CD PROJEKT RED", 2, "RPG", "XHrskkHf958"), # IGN Review
        (489830, "The Elder Scrolls V: Skyrim", 799.00, 4.8, "Bethesda", 2, "RPG", "JSRtYpNRoN0"),
        (377160, "Fallout 4", 399.00, 4.5, "Bethesda", 2, "RPG", "X5aJfebzkrM"),
        (22380, "Fallout: New Vegas", 199.00, 4.8, "Obsidian", 1, "RPG", "l-x-1fm2cq8"),
        (1245620, "Elden Ring", 1199.00, 4.9, "FromSoftware", 3, "RPG", "JmzFMMEqlKE"), # IGN Review
        (1086940, "Baldur's Gate 3", 1299.00, 4.9, "Larian Studios", 3, "RPG", "XuC0b3gPtdI"),
        (990080, "Hogwarts Legacy", 1199.00, 4.6, "Avalanche", 4, "Mundo Abierto", "1O6Qstncpnc"),
        (1716740, "Starfield", 1399.00, 3.8, "Bethesda", 4, "RPG", "kfYEiTdsyas"),
        (1817070, "Marvel's Spider-Man", 1199.00, 4.9, "Insomniac", 3, "Mundo Abierto", "q4GdJVvdxss"),
        (1151640, "Horizon Zero Dawn", 999.00, 4.8, "Guerrilla", 3, "Mundo Abierto", "wzx96gYA8ek"),
        (2420110, "Horizon Forbidden West", 1199.00, 4.8, "Guerrilla", 4, "Mundo Abierto", "Lq594XpoDrw"),
        (1190460, "Death Stranding", 799.00, 4.6, "Kojima Productions", 3, "Mundo Abierto", "tCI3AL8hXyE"),
        (2208920, "Assassin's Creed Valhalla", 1199.00, 4.3, "Ubisoft", 3, "Mundo Abierto", "LrujI3T-G9I"),
        (812140, "Assassin's Creed Odyssey", 1199.00, 4.5, "Ubisoft", 3, "Mundo Abierto", "s_SJZSAtLBA"),
        (1569040, "God of War", 999.00, 4.9, "Santa Monica", 3, "RPG", "K0u_kAWLJOA"),
        (524220, "NieR:Automata", 799.00, 4.8, "Square Enix", 2, "RPG", "wJxNhJ8cjFk"),
        (1687950, "Persona 5 Royal", 1199.00, 4.9, "ATLUS", 2, "RPG", "mjp2m5f2Ibg"),
        (1113000, "Persona 4 Golden", 399.00, 4.9, "ATLUS", 1, "RPG", "1l98y0nIfBw"),
        (638970, "Yakuza 0", 399.00, 4.9, "Ryu Ga Gotoku", 2, "RPG", "5EaT7zYm-20"),
        (1376220, "Yakuza: Like a Dragon", 1199.00, 4.8, "Ryu Ga Gotoku", 2, "RPG", "1EWeeDq8zWw"),
        (582010, "Monster Hunter: World", 599.00, 4.6, "Capcom", 3, "RPG", "Ro6r15wzp2o"),
        (1446780, "Monster Hunter Rise", 799.00, 4.7, "Capcom", 2, "RPG", "k1G-K2T0nIs"),
        (374320, "Dark Souls III", 999.00, 4.8, "FromSoftware", 2, "RPG", "_zDZYrIUgKE"),
        (236430, "Dark Souls II", 799.00, 4.6, "FromSoftware", 2, "RPG", "Tz_S35-iZik"),
        (814380, "Sekiro: Shadows Die Twice", 1299.00, 4.9, "FromSoftware", 3, "RPG", "rXMX4YJ7Lks"),
        (1888160, "ARMORED CORE VI", 1199.00, 4.8, "FromSoftware", 3, "RPG", "h9y2nI0T6dE"),
        (1328670, "Mass Effect Legendary Edition", 1199.00, 4.8, "BioWare", 2, "RPG", "n8i53TtQ6IQ"),
        (435150, "Divinity: Original Sin 2", 899.00, 4.9, "Larian Studios", 2, "RPG", "bTWTFX8qzPI"),
        (291650, "Pillars of Eternity", 599.00, 4.6, "Obsidian", 1, "RPG", "2D2tN2fV0sQ"),
        (238960, "Path of Exile", 0.00, 4.6, "Grinding Gear Games", 2, "RPG", "N8XgXqgJ_mU"),
        (359870, "Final Fantasy X/X-2 HD", 599.00, 4.8, "Square Enix", 1, "RPG", "5gY9I-0P_qY"),

        # --- SUPERVIVENCIA ---
        (252490, "Rust", 450.00, 4.2, "Facepunch", 2, "Supervivencia", "DUCbAJeE80Q"),
        (346110, "ARK: Survival Evolved", 399.00, 4.1, "Studio Wildcard", 3, "Supervivencia", "5fIAPcXd2OQ"),
        (892970, "Valheim", 355.00, 4.8, "Iron Gate", 2, "Supervivencia", "o54Y4wM10hM"),
        (1623730, "Palworld", 335.00, 4.5, "Pocketpair", 3, "Supervivencia", "oG8rKkKAvjI"),
        (264710, "Subnautica", 334.99, 4.8, "Unknown Worlds", 2, "Supervivencia", "Rz2SNm8VguE"),
        (848450, "Subnautica: Below Zero", 334.99, 4.6, "Unknown Worlds", 2, "Supervivencia", "GkQY5_mC-Qk"),
        (242760, "The Forest", 355.00, 4.8, "Endnight Games", 2, "Supervivencia", "kW-41UeG4aA"),
        (1326470, "Sons Of The Forest", 599.00, 4.6, "Endnight Games", 3, "Supervivencia", "xJ-sI_PqIHA"),
        (648800, "Raft", 355.00, 4.8, "Redbeet", 1, "Supervivencia", "72v5Q5zU5gA"),
        (108600, "Project Zomboid", 355.00, 4.7, "The Indie Stone", 1, "Supervivencia", "tZ5eR8aA5vE"),
        (275850, "No Man's Sky", 1149.00, 4.5, "Hello Games", 2, "Supervivencia", "v0zTfNq9tEQ"),
        (105600, "Terraria", 113.99, 4.9, "Re-Logic", 1, "Supervivencia", "w7uOhFTrrq0"),
        (211820, "Starbound", 280.00, 4.6, "Chucklefish", 1, "Supervivencia", "h2J_o71XW7k"),
        (322330, "Don't Starve Together", 280.00, 4.8, "Klei", 1, "Supervivencia", "bVqnIWGO8pQ"),
        (282070, "This War of Mine", 229.00, 4.8, "11 bit studios", 1, "Supervivencia", "HxEw2tIfTfQ"),

        # --- HORROR ---
        (2050650, "Resident Evil 4 Remake", 1199.00, 4.9, "Capcom", 3, "Horror", "j5Xv2lM9zes"),
        (883710, "Resident Evil 2 Remake", 799.00, 4.8, "Capcom", 2, "Horror", "u3wS-Q2KBGQ"),
        (1693980, "Dead Space Remake", 1199.00, 4.7, "Motive", 4, "Horror", "cTDJNOjgKlc"),
        (739630, "Phasmophobia", 185.99, 4.7, "Kinetic Games", 2, "Horror", "sRa9OEABMcY"),
        (381210, "Dead by Daylight", 229.99, 4.4, "Behaviour", 2, "Horror", "JGhIXLO3ul8"),
        (282140, "SOMA", 400.00, 4.8, "Frictional Games", 1, "Horror", "sy38R2g4-cQ"),
        (418370, "Resident Evil 7", 399.00, 4.8, "Capcom", 2, "Horror", "W1OUs3HwIuo"),
        (1196590, "Resident Evil Village", 799.00, 4.8, "Capcom", 3, "Horror", "QK0u51sK4iU"),
        (214490, "Alien: Isolation", 799.00, 4.9, "Creative Assembly", 2, "Horror", "7h0cgmv8Xto"),
        (241100, "Outlast", 199.00, 4.8, "Red Barrels", 1, "Horror", "uXyG_P2n84o"),

        # --- INDIES Y PLATAFORMAS ---
        (413150, "Stardew Valley", 179.99, 4.9, "ConcernedApe", 1, "Indie", "ot7uXNQskhs"),
        (1145360, "Hades", 279.99, 4.9, "Supergiant Games", 1, "Indie", "mD8x5xAMR-M"),
        (2302700, "Hades II", 599.00, 4.9, "Supergiant Games", 2, "Indie", "l-iHDj3EwM0"),
        (367520, "Hollow Knight", 179.99, 4.9, "Team Cherry", 1, "Indie", "UAO2urG23S4"),
        (280160, "Cuphead", 355.00, 4.9, "Studio MDHR", 1, "Indie", "4TjUPXAn2Ro"),
        (504230, "Celeste", 355.00, 4.9, "Extremely OK Games", 1, "Indie", "70d9irlxiB4"),
        (588650, "Dead Cells", 450.00, 4.8, "Motion Twin", 1, "Indie", "RvG1jnCChpI"),
        (250900, "The Binding of Isaac: Rebirth", 280.00, 4.9, "Nicalis", 1, "Indie", "Z6hSVEu-iOE"),
        (646570, "Slay the Spire", 450.00, 4.9, "Mega Crit Games", 1, "Indie", "0mSAmXJm-dM"),
        (391540, "Undertale", 180.00, 4.9, "tobyfox", 1, "Indie", "1Hojv0m3TqA"),
        (400, "Portal", 180.00, 4.9, "Valve", 1, "Indie", "TluRVBhmf8w"),
        (620, "Portal 2", 180.00, 4.9, "Valve", 1, "Indie", "m_eXIO0gMME"),
        (311690, "Enter the Gungeon", 280.00, 4.8, "Dodge Roll", 1, "Indie", "LMEtA8K8D8w"),
        (460950, "Katana ZERO", 280.00, 4.9, "Askiisoft", 1, "Indie", "H_Hn-n87_7g"),
        (241600, "Rogue Legacy", 280.00, 4.5, "Cellar Door Games", 1, "Indie", "T0DKxOEikTs"),
        (1150690, "OMORI", 355.00, 4.9, "OMOCAT", 1, "Indie", "erzgjfEAQz8"),

        # --- ESTRATEGIA Y SIMULACIÓN ---
        (289070, "Civilization VI", 1199.00, 4.5, "Firaxis", 2, "Estrategia", "5KdE0p2joJw"),
        (8930, "Civilization V", 599.00, 4.8, "Firaxis", 1, "Estrategia", "q7pYhHn0eEw"),
        (394360, "Hearts of Iron IV", 799.00, 4.6, "Paradox", 2, "Estrategia", "Awta39qJjW4"),
        (281990, "Stellaris", 799.00, 4.5, "Paradox", 2, "Estrategia", "yHht-rQ5PzE"),
        (236850, "Europa Universalis IV", 799.00, 4.5, "Paradox", 2, "Estrategia", "E2zNf3z_lP4"),
        (1158310, "Crusader Kings III", 999.00, 4.7, "Paradox", 2, "Estrategia", "O2RksK2T0nIs"),
        (268500, "XCOM 2", 1199.00, 4.5, "Firaxis", 2, "Estrategia", "2E_-2wIJbK8"),
        (813780, "Age of Empires II: Definitive", 355.00, 4.8, "Xbox Game Studios", 1, "Estrategia", "ZOgBVR21pWg"),
        (1142710, "Total War: WARHAMMER III", 1199.00, 4.3, "CREATIVE ASSEMBLY", 3, "Estrategia", "hP14Ie1z-G8"),
        (259900, "Cities: Skylines", 599.00, 4.8, "Colossal Order", 2, "Simulación", "CpWe03JpwIo"),
        (427520, "Factorio", 600.00, 4.9, "Wube Software", 1, "Simulación", "J8xBJVQVG_g"),
        (294100, "RimWorld", 600.00, 4.9, "Ludeon Studios", 1, "Simulación", "8mbE6wD-UfA"),
        (4000, "Garry's Mod", 123.99, 4.9, "Facepunch", 1, "Simulación", "Xw1C5T-fH2Y"),
        (244850, "Space Engineers", 355.00, 4.5, "Keen Software House", 2, "Simulación", "mQ4vI04kFvY"),

        # --- MULTIJUGADOR, DEPORTES Y CARRERAS ---
        (945360, "Among Us", 57.99, 4.6, "Innersloth", 1, "Multijugador", "NSJ4cEZB3wE"),
        (1097150, "Fall Guys", 0.00, 4.2, "Mediatonic", 1, "Multijugador", "z6UqcP0hQkM"),
        (252950, "Rocket League", 0.00, 4.7, "Psyonix", 1, "Multijugador", "OmMRGAhBwE4"),
        (570, "Dota 2", 0.00, 4.4, "Valve", 1, "Multijugador", "-cSFPIwMEq4"),
        (1551360, "Forza Horizon 5", 1199.00, 4.7, "Playground Games", 3, "Carreras", "FYH9n37B7Yw"),
        (244210, "Assetto Corsa", 355.00, 4.8, "Kunos Simulazioni", 2, "Carreras", "zC_mG6sT-sU"),
        (228380, "Wreckfest", 599.00, 4.7, "Bugbear", 2, "Carreras", "n-O_OIQvAkw"),
        (310560, "DiRT Rally", 355.00, 4.6, "Codemasters", 2, "Carreras", "1cZ94tT9mXw")
    ]

    # Diccionario de hardware simulado
    specs = {
        1: {"min_cpu": "Intel Core i3-3220", "min_gpu": "NVIDIA GTX 650", "min_ram": 4, "rec_cpu": "Intel Core i5-4460", "rec_gpu": "NVIDIA GTX 960", "rec_ram": 8},
        2: {"min_cpu": "Intel Core i5-6600K", "min_gpu": "NVIDIA GTX 1050 Ti", "min_ram": 8, "rec_cpu": "AMD Ryzen 5 3600", "rec_gpu": "NVIDIA GTX 1660 Super", "rec_ram": 16},
        3: {"min_cpu": "Intel Core i5-8400", "min_gpu": "NVIDIA GTX 1060 6GB", "min_ram": 12, "rec_cpu": "Intel Core i7-10700K", "rec_gpu": "NVIDIA RTX 3060", "rec_ram": 16},
        4: {"min_cpu": "Intel Core i7-6700K", "min_gpu": "NVIDIA RTX 2070", "min_ram": 16, "rec_cpu": "Intel Core i9-12900K", "rec_gpu": "NVIDIA RTX 4070", "rec_ram": 32}
    }

    nombres_us = ["DarkKnight", "CyberNinja", "GamerPro99", "PixelQueen", "RetroMaster", "PraiseTheSun", "KratosFan"]
    comentarios = ["GOTY indiscutible.", "Corre perfecto en mi PC.", "Una obra maestra.", "Mejor que el original.", "Muy exigente, pero vale la pena.", "Gráficos increíbles.", "Juegazo, 10/10."]

    juegos_insertados_ids = []

    # 4. Inserción de juegos
    for juego in lista_juegos:
        app_id, titulo, precio, puntaje, dev, exigencia, tag, yt_id = juego
        
        img_url = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{app_id}/header.jpg"
        descripcion_dinamica = f"Sumérgete en el universo de {titulo}. Una increíble experiencia de la categoría {tag} desarrollada por {dev}. Prepárate para horas de entretenimiento inmersivo."
        
        # Enlace de YouTube limpio y optimizado para iframes
        video_trailer_gen = f"https://www.youtube.com/embed/{yt_id}?autoplay=0&rel=0"
        
        cursor.execute("""
            INSERT INTO juegos (titulo, precio, imagen_url, puntuacion, desarrollador, tag, descripcion, video_url) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (titulo, precio, img_url, puntaje, dev, tag, descripcion_dinamica, video_trailer_gen))
        
        juego_id = cursor.lastrowid
        juegos_insertados_ids.append(juego_id)

        req = specs[exigencia]
        cursor.execute("INSERT INTO requisitos (juego_id, tipo, cpu, gpu, ram_gb) VALUES (?, ?, ?, ?, ?)", (juego_id, "Mínimos", req["min_cpu"], req["min_gpu"], req["min_ram"]))
        cursor.execute("INSERT INTO requisitos (juego_id, tipo, cpu, gpu, ram_gb) VALUES (?, ?, ?, ?, ?)", (juego_id, "Recomendados", req["rec_cpu"], req["rec_gpu"], req["rec_ram"]))
        
        for _ in range(2):
            cursor.execute("INSERT INTO resenas (juego_id, usuario, comentario, estrellas) VALUES (?, ?, ?, ?)", (juego_id, random.choice(nombres_us), random.choice(comentarios), random.randint(4, 5)))

    # 5. PRE-CARGAR LA BIBLIOTECA DEL USUARIO
    juegos_comprados = random.sample(juegos_insertados_ids, 25)
    for j_id in juegos_comprados:
        cursor.execute("INSERT INTO biblioteca (juego_id) VALUES (?)", (j_id,))

    conexion.commit()
    conexion.close()
    print(f"¡Éxito total! Base de datos reconstruida con videos 100% compatibles sin restricción de edad.")

if __name__ == "__main__":
    construir_base_datos()