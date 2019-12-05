import sqlite3

# conectando...
conn = sqlite3.connect('usersLOCAL.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE pessoa (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE feature_points (
        id_points INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        point0 INTEGER NOT NULL,
        point1 INTEGER NOT NULL
);
""")

cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (1, 0, 48);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (2, 0, 36);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (3, 0, 16);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (4, 3, 48);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (5, 7, 48);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (6, 7, 9);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (7, 8, 57);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (8, 9, 54);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (9, 13, 54);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (10, 16, 54);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (11, 16, 45);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (12, 17, 36);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (13, 17, 21);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (14, 21, 39);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (15, 21, 27);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (16, 21, 22);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (17, 22, 42);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (18, 22, 26);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (19, 22, 27);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (20, 26, 45);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (21, 27, 35);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (22, 27, 33);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (23, 27, 31);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (24, 31, 48);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (25, 31, 39);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (26, 31, 36);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (27, 31, 35);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (28, 33, 51);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (29, 35, 54);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (30, 35, 45);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (31, 35, 42);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (32, 36, 48);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (33, 36, 39);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (34, 42, 45);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (35, 45, 54);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (36, 48, 54);""")
cursor.execute("""INSERT INTO feature_points (id_points, point0, point1) VALUES (37, 51, 57);""")
conn.commit()

cursor.execute("""
CREATE TABLE distances (
        id_distance INTEGER NOT NULL,
        distance_gravity FLOAT NOT NULL,
        id_pessoa INTEGER,
        FOREIGN KEY (id_pessoa) REFERENCES pessoa(id),
        PRIMARY KEY (id_distance, id_pessoa)
);
""")


print('Tabelas criadas com sucesso.')
# desconectando...
conn.close()
