import platform
import psutil
import time
from datetime import timedelta

def get_sistema_info():
    sistema = platform.system()
    versao = platform.release()
    build_str = platform.version() # Ex: '10.0.22621'
    
    # CORREÇÃO DO WINDOWS 11:
    # O Python lê Windows 11 como 10 porque a Microsoft manteve o núcleo 10.0.
    # A solução é olhar o número da Build (Acima de 22000 é Win 11).
    if sistema == "Windows" and versao == "10":
        try:
            build = int(build_str.split('.')[2])
            if build >= 22000:
                versao = "11"
        except:
            pass

    nome_so = f"{sistema} {versao}"
    arquitetura = platform.machine()
    
    # Cálculo do Tempo Ligado (Uptime)
    boot_time = psutil.boot_time()
    uptime_segundos = int(time.time() - boot_time)
    tempo_ligado = str(timedelta(seconds=uptime_segundos))

    return {
        "so": nome_so,
        "arquitetura": arquitetura,
        "tempo_ligado": tempo_ligado
    }