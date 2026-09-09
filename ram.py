import wmi
import psutil
from utils import bytes_para_gb

def obter_tipo_ddr(codigo):
    tipos = {20: "DDR", 21: "DDR2", 24: "DDR3", 26: "DDR4", 34: "DDR5"}
    return tipos.get(codigo, "Desconhecido")

def get_ram_info():
    info = {"total_gb": 0.0, "uso_medio_porcento": 0.0, "pentes_fisicos": []}
    try:
        mem = psutil.virtual_memory()
        info["total_gb"] = bytes_para_gb(mem.total)
        info["uso_medio_porcento"] = mem.percent
        
        w = wmi.WMI()
        for stick in w.Win32_PhysicalMemory():
            info["pentes_fisicos"].append({
                "capacidade_gb": bytes_para_gb(stick.Capacity),
                "tipo": obter_tipo_ddr(stick.SMBIOSMemoryType)
            })
    except Exception as e:
        info["erro"] = str(e)
    return info