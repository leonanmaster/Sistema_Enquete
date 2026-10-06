from xmlrpc.server import SimpleXMLRPCServer
import bd

class EnqueteAPI:
    def criar_enquete(self, usuario, pergunta, opcoes, data_limite):
        if not usuario:
            return "Usuário não autorizado"
        return bd.inserir_enquete(usuario, pergunta, opcoes, data_limite)

    def votar(self, usuario, id_enquete, opcao):
        return bd.inserir_voto(usuario, id_enquete, opcao)

    def consultar_resultados(self, id_enquete):
        return bd.obter_resultados(id_enquete)

    def listar_enquetes_ativas(self):
        return bd.obter_enquetes_ativas()

def iniciar_servidor(ip="0.0.0.0", porta=8000):
    # Garante que o banco de dados e as tabelas são criados antes de abrir a rede
    bd.inicializar_banco()
    
    servidor = SimpleXMLRPCServer((ip, porta), allow_none=True)
    servidor.register_instance(EnqueteAPI())
    
    print(f"Servidor RPC de Enquetes a escutar em {ip}:{porta}...")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado de forma segura.")

if __name__ == "__main__":
    iniciar_servidor()