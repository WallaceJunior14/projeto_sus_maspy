# arquivo: main.py
from maspy import *
from agentes.secretaria_saude import AgenteSecretariaSaude
from agentes.ubs import AgenteUBS
from agentes.frota_logistica import AgenteFrotaLogistica

def inicializar_sistema():
    print("[SISTEMA] Iniciando a configuração do ambiente Maspy...")
    
    # 1. Instanciando o agente central (Secretaria) com 500 kits em estoque
    secretaria = AgenteSecretariaSaude("Secretaria_Estadual", 500)
    
    # 2. Instanciando as UBSs com cenários heterogêneos (Membro 2)
    # UBS Centro: População média, muitos casos, estoque zerado (Alta urgência esperada)
    ubs1 = AgenteUBS("UBS_Centro", populacao=10000, casos_24h=150, estoque_local=0)
    
    # UBS Zona Norte: População grande, poucos casos, estoque moderado (Baixa urgência esperada)
    ubs2 = AgenteUBS("UBS_ZonaNorte", populacao=25000, casos_24h=50, estoque_local=10)
    
    # UBS Zona Sul: População pequena, casos moderados, estoque baixo (Média/Alta urgência)
    ubs3 = AgenteUBS("UBS_ZonaSul", populacao=5000, casos_24h=60, estoque_local=2)

    # . Instanciando a Frota Logística 
    # Parametros: nome, x_inicial, y_inicial, custo_por_km [cite: 11]
    veiculo1 = AgenteFrotaLogistica("Fiorino01", x_inicial=0, y_inicial=0, custo_km=2.50) 
    veiculo2 = AgenteFrotaLogistica("Caminhao02", x_inicial=40, y_inicial=50, custo_km=4.20) 
    
    # 3. Criando o canal de comunicação do SUS
    canal_sus = Channel("Canal_SUS")
    
    # 4. Conectando todos os agentes ativos ao canal
    Admin().connect_to([secretaria, ubs1, ubs2, ubs3, veiculo1, veiculo2], canal_sus)
    
    # 5. Gatilho Inicial: Ativa o objetivo na secretaria para disparar o Contract-Net
    secretaria.add(Goal("iniciar_distribuicao", (500,)))
    
    print("[SISTEMA] Ambiente configurado. Iniciando execução dos agentes...")
    Admin().start_system()

if __name__ == "__main__":
    inicializar_sistema()