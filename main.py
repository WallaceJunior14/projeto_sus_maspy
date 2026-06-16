# arquivo: main.py

from maspy import *
from agentes.secretaria_saude import AgenteSecretariaSaude
from agentes.ubs_mock import AgenteUBSMock

def inicializar_sistema():
    print("[SISTEMA] Iniciando a configuração do ambiente Maspy...")
    
    # Ativa os logs internos para vermos as execuções (útil para o vídeo da entrega)
    #Admin().start_logger(enable_console=True)
    
    # 1. Instanciando os agentes
    secretaria = AgenteSecretariaSaude("Secretaria_Estadual", 500)
    ubs1 = AgenteUBSMock("UBS_Centro")
    ubs2 = AgenteUBSMock("UBS_ZonaNorte")
    ubs3 = AgenteUBSMock("UBS_ZonaSul")
    
    # 2. Criando o canal de comunicação do SUS
    canal_sus = Channel("Canal_SUS")
    
    # 3. Conectando todos os agentes ao canal
    Admin().connect_to([secretaria, ubs1, ubs2, ubs3], canal_sus)
    
    # 4. Gatilho Inicial: Adiciona o objetivo na secretaria para começar tudo!
    secretaria.add(Goal("iniciar_distribuicao", (500,)))
    
    print("[SISTEMA] Ambiente configurado. Iniciando execução dos agentes...")
    Admin().start_system()

if __name__ == "__main__":
    inicializar_sistema()