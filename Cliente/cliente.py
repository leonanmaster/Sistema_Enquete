import xmlrpc.client
import sys
from datetime import datetime

def exibir_menu():
    print("\n--- Sistema de Votação Online ---")
    print("1. Criar Enquete")
    print("2. Votar")
    print("3. Consultar Resultados")
    print("4. Listar Enquetes Ativas")
    print("5. Sair")
    return input("Escolha uma opção: ")

def main():
    ip_servidor = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    porta = "8000"
    url = f"http://{ip_servidor}:{porta}"
    
    print(f"Ligando ao servidor em {url}...")
    
    try:
        # Cria o proxy que traduzirá as chamadas locais em requisições RPC
        servidor = xmlrpc.client.ServerProxy(url, allow_none=True)
        usuario = input("Introduza o seu nome de utilizador: ")
        
        while True:
            opcao = exibir_menu()
            
            if opcao == '1':
                pergunta = input("Pergunta da enquete: ")
                opcoes_str = input("Opções separadas por vírgula (ex: Sim,Não,Talvez): ")
                opcoes = [op.strip() for op in opcoes_str.split(',')]
                # Formato ISO 8601 (bd)
                data_limite = input("Data limite (YYYY-MM-DDTHH:MM:SS): ") 
                
                resposta = servidor.criar_enquete(usuario, pergunta, opcoes, data_limite)
                print(f"Resposta do servidor: {resposta}")
                
            elif opcao == '2':
                id_enquete = int(input("ID da Enquete: "))
                id_opcao = int(input("ID da Opção escolhida: "))
                

                resposta = servidor.votar(usuario, id_enquete, id_opcao)
                print(f"Resposta do servidor: {resposta}")
                
            elif opcao == '3':
                id_enquete = int(input("ID da Enquete para consulta: "))
                
                resultados = servidor.consultar_resultados(id_enquete)
                print("Resultados:")
                for r in resultados:
                    # r[0] = id, r[1] = texto, r[2] = contagem
                    print(f"Opção {r[0]} ({r[1]}): {r[2]} votos")
                    
            elif opcao == '4':
                ativas = servidor.listar_enquetes_ativas()
                print("Enquetes Ativas:")
                for e in ativas:
                    print(f"ID: {e[0]} | Pergunta: {e[1]} | Limite: {e[2]}")
                    
            elif opcao == '5':
                print("A encerrar o cliente.")
                break
            else:
                print("Opção inválida.")
                
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Verifique se o IP está correto e o servidor está  no ar.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()