import sqlite3
from datetime import datetime

NOME_BANCO = "enquetes.db"

def inicializar_banco():
    """Cria as tabelas no banco de dados, se não existirem."""
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()

    # Tabela de Enquetes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enquetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            criador TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            data_limite TEXT NOT NULL
        )
    ''')

    # Tabela de Opções
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opcoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_enquete INTEGER NOT NULL,
            texto TEXT NOT NULL,
            FOREIGN KEY (id_enquete) REFERENCES enquetes (id)
        )
    ''')

    # Tabela de Votos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_enquete INTEGER NOT NULL,
            id_opcao INTEGER NOT NULL,
            utilizador TEXT NOT NULL,
            UNIQUE(id_enquete, utilizador),
            FOREIGN KEY (id_enquete) REFERENCES enquetes (id),
            FOREIGN KEY (id_opcao) REFERENCES opcoes (id)
        )
    ''')

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados inicializado com sucesso.")


def inserir_enquete(criador, pergunta, opcoes, data_limite):
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    try:
        # Insere a enquete e recupera o ID gerado automaticamente
        cursor.execute('''
            INSERT INTO enquetes (criador, pergunta, data_limite)
            VALUES (?, ?, ?)
        ''', (criador, pergunta, data_limite))
        id_enquete = cursor.lastrowid
        
        # Insere cada opção associada a este ID
        for texto_opcao in opcoes:
            cursor.execute('''
                INSERT INTO opcoes (id_enquete, texto)
                VALUES (?, ?)
            ''', (id_enquete, texto_opcao))
        
        conexao.commit()
        return id_enquete
    except Exception as e:
        conexao.rollback()
        return f"Erro ao criar enquete: {str(e)}"
    finally:
        conexao.close()

def inserir_voto(utilizador, id_enquete, id_opcao):
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    # Verifica o prazo da enquete
    cursor.execute("SELECT data_limite FROM enquetes WHERE id = ?", (id_enquete,))
    resultado = cursor.fetchone()
    if not resultado:
        conexao.close()
        return "Enquete não encontrada"
        
    data_limite_str = resultado[0]
    agora = datetime.now().isoformat()
    
    if agora > data_limite_str:
        conexao.close()
        return "Enquete encerrada"
        
    try:
        cursor.execute('''
            INSERT INTO votos (id_enquete, id_opcao, utilizador)
            VALUES (?, ?, ?)
        ''', (id_enquete, id_opcao, utilizador))
        conexao.commit()
        return "Sucesso"
    except sqlite3.IntegrityError:
        # O banco de dados dispara este erro devido à regra UNIQUE
        conexao.rollback()
        return "Voto já registrado"
    finally:
        conexao.close()

def obter_resultados(id_enquete):
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    
    cursor.execute('''
        SELECT o.id, o.texto, COUNT(v.id) 
        FROM opcoes o
        LEFT JOIN votos v ON o.id = v.id_opcao
        WHERE o.id_enquete = ?
        GROUP BY o.id
    ''', (id_enquete,))
    
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

def obter_enquetes_ativas():
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    agora = datetime.now().isoformat()
    
    cursor.execute('''
        SELECT id, pergunta, data_limite 
        FROM enquetes 
        WHERE data_limite > ?
    ''', (agora,))
    
    enquetes = cursor.fetchall()
    conexao.close()
    return enquetes