import requests     
import sqlite3

#banco de dados SQLite
db_name = 'sla.db'

conexao = sqlite3.connect(db_name)
cursor = conexao.cursor()

# Criar tabela de usuários
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        email TEXT,
        telefone TEXT
    )
""")
try:
    conexao = sqlite3.connect(db_name)
    cursor = conexao.cursor()
    print("Conexão com o banco de dados SQLite bem-sucedida.")
    #Consumir API REST
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    if response.status_code == 200:
        usuarios = response.json()

        try:
            for un in usuarios:
                id_usuario = un['id']
                nome = un['name']       
                email = un['email']
                telefone = un['phone']

                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = ?", (id_usuario,))
                existe = cursor.fetchone()[0]
                #inserir dados na tabela
                if not existe:
                    cursor.execute("""
                        INSERT INTO usuarios (id, nome, email, telefone) 
                        VALUES (?, ?, ?, ?)
                    """, (id_usuario, nome, email, telefone))

                    print(f"✅ Usuário {nome} inserido no banco.")

                else:
                    print(f"⚠️ Usuário {nome} já existe, pulando...")
        except Exception as e:  
            print(f"Erro ao consumir API:", response.status_code)

        #salvar as mudanças no bd
    conexao.commit()
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

finally:
    if conexao:
        conexao.close()
        print("Conexão com o banco de dados SQLite fechada.")