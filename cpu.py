import platform
import psutil
import wmi
import pythoncom

def get_cpu_info():
    nome_cpu = "Processador Desconhecido"
    
    try:
        # Pede permissão para a Thread do Windows
        pythoncom.CoInitialize()
        w = wmi.WMI()
        for proc in w.Win32_Processor():
            nome_cpu = proc.Name.strip()
            break
    except Exception as e:
        print("Aviso: Falha ao ler CPU via WMI:", e)
        nome_cpu = platform.processor()
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass

    # Tira a média exata de uso imitando o Gerenciador de Tarefas
    uso_medio = psutil.cpu_percent(interval=0.5)

    return {
        "nome": nome_cpu,
        "uso_medio_porcento": round(uso_medio, 1)
    }