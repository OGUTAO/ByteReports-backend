import wmi
import psutil
from utils import bytes_para_gb

def get_disco_info():
    info = {"discos_fisicos": [], "particoes": []}
    try:
        w = wmi.WMI()
        for disco in w.Win32_DiskDrive():
            info["discos_fisicos"].append({
                "modelo": disco.Model,
                "saude_smart": disco.Status
            })
    except Exception:
        pass
        
    for part in psutil.disk_partitions(all=False):
        if part.fstype:
            try:
                uso = psutil.disk_usage(part.mountpoint)
                info["particoes"].append({
                    "letra": part.device.replace("\\", ""),
                    "total_gb": bytes_para_gb(uso.total),
                    "livre_gb": bytes_para_gb(uso.free),
                    "uso_porcento": uso.percent
                })
            except Exception:
                pass
                
    return info