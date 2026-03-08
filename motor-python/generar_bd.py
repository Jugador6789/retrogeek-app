import sqlite3
import random

def construir_base_datos():
    print("Iniciando la construcción MASIVA de la base de datos RetroGeek (Portable)...")
    conexion = sqlite3.connect("tienda_retrogeek.db")
    cursor = conexion.cursor()

    # 1. Limpiar tablas existentes para evitar duplicados al correrlo en otras PCs
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
            tag TEXT
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

    # 3. MEGA LISTA DE JUEGOS REALES (Lista completa para portabilidad)
    lista_juegos = [
        # --- SHOOTERS Y ACCIÓN ---
        (730, "Counter-Strike 2", 0.00, 4.5, "Valve", 2, "Shooter"),
        (1172470, "Apex Legends", 0.00, 4.3, "Respawn", 2, "Shooter"),
        (359550, "Rainbow Six Siege", 399.00, 4.5, "Ubisoft", 2, "Shooter"),
        (1085660, "Destiny 2", 0.00, 4.2, "Bungie", 2, "Shooter"),
        (578080, "PUBG: BATTLEGROUNDS", 0.00, 4.0, "KRAFTON", 2, "Shooter"),
        (379720, "DOOM", 399.00, 4.8, "id Software", 2, "Shooter"),
        (782330, "DOOM Eternal", 799.00, 4.9, "id Software", 3, "Shooter"),
        (1240440, "Halo Infinite", 0.00, 4.1, "343 Industries", 3, "Shooter"),
        (1238810, "Battlefield V", 799.00, 4.2, "DICE", 3, "Shooter"),
        (1237970, "Titanfall 2", 599.00, 4.9, "Respawn", 2, "Shooter"),
        (49520, "Borderlands 2", 399.00, 4.8, "Gearbox", 1, "Shooter"),
        (397540, "BioShock Infinite", 599.00, 4.8, "Irrational Games", 2, "Shooter"),
        (550, "Left 4 Dead 2", 123.99, 4.9, "Valve", 1, "Shooter"),
        (220, "Half-Life 2", 123.99, 4.9, "Valve", 1, "Shooter"),
        (222880, "Insurgency", 299.00, 4.4, "New World", 1, "Shooter"),
        (581320, "Insurgency: Sandstorm", 599.00, 4.5, "New World", 3, "Shooter"),
        (594650, "Hunt: Showdown", 799.00, 4.3, "Crytek", 3, "Shooter"),
        (393380, "Squad", 999.00, 4.5, "Offworld Industries", 3, "Shooter"),
        (686810, "Hell Let Loose", 899.00, 4.4, "Team17", 3, "Shooter"),
        (2357570, "Overwatch 2", 0.00, 3.5, "Blizzard", 2, "Shooter"),
        (1361210, "Warhammer 40K: Darktide", 799.00, 4.1, "Fatshark", 4, "Shooter"),
        (2535960, "Helldivers 2", 799.00, 4.7, "Arrowhead", 3, "Shooter"),
        (230410, "Warframe", 0.00, 4.8, "Digital Extremes", 2, "Shooter"),
        (440, "Team Fortress 2", 0.00, 4.9, "Valve", 1, "Shooter"),

        # --- MUNDO ABIERTO & RPG ---
        (271590, "Grand Theft Auto V", 599.00, 4.8, "Rockstar Games", 2, "Mundo Abierto"),
        (1174180, "Red Dead Redemption 2", 1299.00, 4.9, "Rockstar Games", 3, "Mundo Abierto"),
        (1091500, "Cyberpunk 2077", 1299.00, 4.6, "CD PROJEKT RED", 4, "RPG"),
        (292030, "The Witcher 3: Wild Hunt", 799.00, 4.9, "CD PROJEKT RED", 2, "RPG"),
        (489830, "The Elder Scrolls V: Skyrim", 799.00, 4.8, "Bethesda", 2, "RPG"),
        (377160, "Fallout 4", 399.00, 4.5, "Bethesda", 2, "RPG"),
        (22380, "Fallout: New Vegas", 199.00, 4.8, "Obsidian", 1, "RPG"),
        (1245620, "Elden Ring", 1199.00, 4.9, "FromSoftware", 3, "RPG"),
        (1086940, "Baldur's Gate 3", 1299.00, 4.9, "Larian Studios", 3, "RPG"),
        (990080, "Hogwarts Legacy", 1199.00, 4.6, "Avalanche", 4, "Mundo Abierto"),
        (1716740, "Starfield", 1399.00, 3.8, "Bethesda", 4, "RPG"),
        (1817070, "Marvel's Spider-Man", 1199.00, 4.9, "Insomniac", 3, "Mundo Abierto"),
        (1151640, "Horizon Zero Dawn", 999.00, 4.8, "Guerrilla", 3, "Mundo Abierto"),
        (2420110, "Horizon Forbidden West", 1199.00, 4.8, "Guerrilla", 4, "Mundo Abierto"),
        (1190460, "Death Stranding", 799.00, 4.6, "Kojima Productions", 3, "Mundo Abierto"),
        (2208920, "Assassin's Creed Valhalla", 1199.00, 4.3, "Ubisoft", 3, "Mundo Abierto"),
        (812140, "Assassin's Creed Odyssey", 1199.00, 4.5, "Ubisoft", 3, "Mundo Abierto"),
        (1569040, "God of War", 999.00, 4.9, "Santa Monica", 3, "RPG"),
        (524220, "NieR:Automata", 799.00, 4.8, "Square Enix", 2, "RPG"),
        (1687950, "Persona 5 Royal", 1199.00, 4.9, "ATLUS", 2, "RPG"),
        (1113000, "Persona 4 Golden", 399.00, 4.9, "ATLUS", 1, "RPG"),
        (638970, "Yakuza 0", 399.00, 4.9, "Ryu Ga Gotoku", 2, "RPG"),
        (1376220, "Yakuza: Like a Dragon", 1199.00, 4.8, "Ryu Ga Gotoku", 2, "RPG"),
        (582010, "Monster Hunter: World", 599.00, 4.6, "Capcom", 3, "RPG"),
        (1446780, "Monster Hunter Rise", 799.00, 4.7, "Capcom", 2, "RPG"),
        (374320, "Dark Souls III", 999.00, 4.8, "FromSoftware", 2, "RPG"),
        (236430, "Dark Souls II", 799.00, 4.6, "FromSoftware", 2, "RPG"),
        (814380, "Sekiro: Shadows Die Twice", 1299.00, 4.9, "FromSoftware", 3, "RPG"),
        (1888160, "ARMORED CORE VI", 1199.00, 4.8, "FromSoftware", 3, "RPG"),
        (1328670, "Mass Effect Legendary Edition", 1199.00, 4.8, "BioWare", 2, "RPG"),
        (435150, "Divinity: Original Sin 2", 899.00, 4.9, "Larian Studios", 2, "RPG"),
        (291650, "Pillars of Eternity", 599.00, 4.6, "Obsidian", 1, "RPG"),
        (238960, "Path of Exile", 0.00, 4.6, "Grinding Gear Games", 2, "RPG"),
        (359870, "Final Fantasy X/X-2 HD", 599.00, 4.8, "Square Enix", 1, "RPG"),

        # --- SUPERVIVENCIA ---
        (252490, "Rust", 450.00, 4.2, "Facepunch", 2, "Supervivencia"),
        (346110, "ARK: Survival Evolved", 399.00, 4.1, "Studio Wildcard", 3, "Supervivencia"),
        (892970, "Valheim", 355.00, 4.8, "Iron Gate", 2, "Supervivencia"),
        (1623730, "Palworld", 335.00, 4.5, "Pocketpair", 3, "Supervivencia"),
        (264710, "Subnautica", 334.99, 4.8, "Unknown Worlds", 2, "Supervivencia"),
        (848450, "Subnautica: Below Zero", 334.99, 4.6, "Unknown Worlds", 2, "Supervivencia"),
        (242760, "The Forest", 355.00, 4.8, "Endnight Games", 2, "Supervivencia"),
        (1326470, "Sons Of The Forest", 599.00, 4.6, "Endnight Games", 3, "Supervivencia"),
        (648800, "Raft", 355.00, 4.8, "Redbeet", 1, "Supervivencia"),
        (108600, "Project Zomboid", 355.00, 4.7, "The Indie Stone", 1, "Supervivencia"),
        (275850, "No Man's Sky", 1149.00, 4.5, "Hello Games", 2, "Supervivencia"),
        (105600, "Terraria", 113.99, 4.9, "Re-Logic", 1, "Supervivencia"),
        (211820, "Starbound", 280.00, 4.6, "Chucklefish", 1, "Supervivencia"),
        (322330, "Don't Starve Together", 280.00, 4.8, "Klei", 1, "Supervivencia"),
        (282070, "This War of Mine", 229.00, 4.8, "11 bit studios", 1, "Supervivencia"),

        # --- HORROR ---
        (2050650, "Resident Evil 4 Remake", 1199.00, 4.9, "Capcom", 3, "Horror"),
        (883710, "Resident Evil 2 Remake", 799.00, 4.8, "Capcom", 2, "Horror"),
        (1693980, "Dead Space Remake", 1199.00, 4.7, "Motive", 4, "Horror"),
        (739630, "Phasmophobia", 185.99, 4.7, "Kinetic Games", 2, "Horror"),
        (381210, "Dead by Daylight", 229.99, 4.4, "Behaviour", 2, "Horror"),
        (282140, "SOMA", 400.00, 4.8, "Frictional Games", 1, "Horror"),
        (418370, "Resident Evil 7", 399.00, 4.8, "Capcom", 2, "Horror"),
        (1196590, "Resident Evil Village", 799.00, 4.8, "Capcom", 3, "Horror"),
        (214490, "Alien: Isolation", 799.00, 4.9, "Creative Assembly", 2, "Horror"),
        (241100, "Outlast", 199.00, 4.8, "Red Barrels", 1, "Horror"),

        # --- INDIES Y PLATAFORMAS ---
        (413150, "Stardew Valley", 179.99, 4.9, "ConcernedApe", 1, "Indie"),
        (1145360, "Hades", 279.99, 4.9, "Supergiant Games", 1, "Indie"),
        (2302700, "Hades II", 599.00, 4.9, "Supergiant Games", 2, "Indie"),
        (367520, "Hollow Knight", 179.99, 4.9, "Team Cherry", 1, "Indie"),
        (280160, "Cuphead", 355.00, 4.9, "Studio MDHR", 1, "Indie"),
        (504230, "Celeste", 355.00, 4.9, "Extremely OK Games", 1, "Indie"),
        (588650, "Dead Cells", 450.00, 4.8, "Motion Twin", 1, "Indie"),
        (250900, "The Binding of Isaac: Rebirth", 280.00, 4.9, "Nicalis", 1, "Indie"),
        (646570, "Slay the Spire", 450.00, 4.9, "Mega Crit Games", 1, "Indie"),
        (391540, "Undertale", 180.00, 4.9, "tobyfox", 1, "Indie"),
        (400, "Portal", 180.00, 4.9, "Valve", 1, "Indie"),
        (620, "Portal 2", 180.00, 4.9, "Valve", 1, "Indie"),
        (311690, "Enter the Gungeon", 280.00, 4.8, "Dodge Roll", 1, "Indie"),
        (460950, "Katana ZERO", 280.00, 4.9, "Askiisoft", 1, "Indie"),
        (241600, "Rogue Legacy", 280.00, 4.5, "Cellar Door Games", 1, "Indie"),
        (1150690, "OMORI", 355.00, 4.9, "OMOCAT", 1, "Indie"),

        # --- ESTRATEGIA Y SIMULACIÓN ---
        (289070, "Civilization VI", 1199.00, 4.5, "Firaxis", 2, "Estrategia"),
        (8930, "Civilization V", 599.00, 4.8, "Firaxis", 1, "Estrategia"),
        (394360, "Hearts of Iron IV", 799.00, 4.6, "Paradox", 2, "Estrategia"),
        (281990, "Stellaris", 799.00, 4.5, "Paradox", 2, "Estrategia"),
        (236850, "Europa Universalis IV", 799.00, 4.5, "Paradox", 2, "Estrategia"),
        (1158310, "Crusader Kings III", 999.00, 4.7, "Paradox", 2, "Estrategia"),
        (268500, "XCOM 2", 1199.00, 4.5, "Firaxis", 2, "Estrategia"),
        (813780, "Age of Empires II: Definitive", 355.00, 4.8, "Xbox Game Studios", 1, "Estrategia"),
        (1142710, "Total War: WARHAMMER III", 1199.00, 4.3, "CREATIVE ASSEMBLY", 3, "Estrategia"),
        (259900, "Cities: Skylines", 599.00, 4.8, "Colossal Order", 2, "Simulación"),
        (427520, "Factorio", 600.00, 4.9, "Wube Software", 1, "Simulación"),
        (294100, "RimWorld", 600.00, 4.9, "Ludeon Studios", 1, "Simulación"),
        (4000, "Garry's Mod", 123.99, 4.9, "Facepunch", 1, "Simulación"),
        (244850, "Space Engineers", 355.00, 4.5, "Keen Software House", 2, "Simulación"),

        # --- MULTIJUGADOR, DEPORTES Y CARRERAS ---
        (945360, "Among Us", 57.99, 4.6, "Innersloth", 1, "Multijugador"),
        (1097150, "Fall Guys", 0.00, 4.2, "Mediatonic", 1, "Multijugador"),
        (252950, "Rocket League", 0.00, 4.7, "Psyonix", 1, "Multijugador"),
        (570, "Dota 2", 0.00, 4.4, "Valve", 1, "Multijugador"),
        (1551360, "Forza Horizon 5", 1199.00, 4.7, "Playground Games", 3, "Carreras"),
        (244210, "Assetto Corsa", 355.00, 4.8, "Kunos Simulazioni", 2, "Carreras"),
        (228380, "Wreckfest", 599.00, 4.7, "Bugbear", 2, "Carreras"),
        (310560, "DiRT Rally", 355.00, 4.6, "Codemasters", 2, "Carreras")
    ]

    # Diccionario de hardware simulado según nivel de exigencia (1 al 4)
    specs = {
        1: {"min_cpu": "Intel Core i3-3220", "min_gpu": "NVIDIA GTX 650", "min_ram": 4, "rec_cpu": "Intel Core i5-4460", "rec_gpu": "NVIDIA GTX 960", "rec_ram": 8},
        2: {"min_cpu": "Intel Core i5-6600K", "min_gpu": "NVIDIA GTX 1050 Ti", "min_ram": 8, "rec_cpu": "AMD Ryzen 5 3600", "rec_gpu": "NVIDIA GTX 1660 Super", "rec_ram": 16},
        3: {"min_cpu": "Intel Core i5-8400", "min_gpu": "NVIDIA GTX 1060 6GB", "min_ram": 12, "rec_cpu": "Intel Core i7-10700K", "rec_gpu": "NVIDIA RTX 3060", "rec_ram": 16},
        4: {"min_cpu": "Intel Core i7-6700K", "min_gpu": "NVIDIA RTX 2070", "min_ram": 16, "rec_cpu": "Intel Core i9-12900K", "rec_gpu": "NVIDIA RTX 4070", "rec_ram": 32}
    }

    nombres_us = ["DarkKnight", "CyberNinja", "GamerPro99", "PixelQueen", "RetroMaster", "PraiseTheSun", "KratosFan"]
    comentarios = ["GOTY indiscutible.", "Corre perfecto en mi PC.", "Una obra maestra.", "Mejor que el original.", "Muy exigente, pero vale la pena.", "Gráficos increíbles.", "Juegazo, 10/10."]

    juegos_insertados_ids = []

    # 4. Inserción de juegos e imágenes oficiales de Steam
    for juego in lista_juegos:
        app_id, titulo, precio, puntaje, dev, exigencia, tag = juego
        img_url = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{app_id}/header.jpg"
        
        cursor.execute("INSERT INTO juegos (titulo, precio, imagen_url, puntuacion, desarrollador, tag) VALUES (?, ?, ?, ?, ?, ?)", (titulo, precio, img_url, puntaje, dev, tag))
        juego_id = cursor.lastrowid
        juegos_insertados_ids.append(juego_id)

        req = specs[exigencia]
        cursor.execute("INSERT INTO requisitos (juego_id, tipo, cpu, gpu, ram_gb) VALUES (?, ?, ?, ?, ?)", (juego_id, "Mínimos", req["min_cpu"], req["min_gpu"], req["min_ram"]))
        cursor.execute("INSERT INTO requisitos (juego_id, tipo, cpu, gpu, ram_gb) VALUES (?, ?, ?, ?, ?)", (juego_id, "Recomendados", req["rec_cpu"], req["rec_gpu"], req["rec_ram"]))
        
        for _ in range(2):
            cursor.execute("INSERT INTO resenas (juego_id, usuario, comentario, estrellas) VALUES (?, ?, ?, ?)", (juego_id, random.choice(nombres_us), random.choice(comentarios), random.randint(4, 5)))

    # 5. PRE-CARGAR LA BIBLIOTECA DEL USUARIO (Selecciona 25 juegos al azar)
    juegos_comprados = random.sample(juegos_insertados_ids, 25)
    for j_id in juegos_comprados:
        cursor.execute("INSERT INTO biblioteca (juego_id) VALUES (?)", (j_id,))

    conexion.commit()
    conexion.close()
    print(f"¡Éxito total! Base de datos 'tienda_retrogeek.db' generada con {len(lista_juegos)} juegos en catálogo y 25 juegos en la Biblioteca personal.")

if __name__ == "__main__":
    construir_base_datos()