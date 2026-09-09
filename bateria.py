import psutil
import wmi
import pythoncom

def get_bateria_info():
    info = {"tem_bateria": False}
    
    try:
        bat = psutil.sensors_battery()
        
        if bat:
            info = {
                "tem_bateria": True,
                "porcento": round(bat.percent, 1),
                "conectada": bat.power_plugged,
                "ciclos": "Desconhecido"
            }
            
            try:
                pythoncom.CoInitialize()
                
                w = wmi.WMI(namespace=r"root\wmi")
                for bateria in w.BatteryCycleCount():
                    info["ciclos"] = bateria.CycleCount
                    break
            except Exception as e:
                print("Aviso: Falha ao ler ciclos da bateria via WMI:", e)
            finally:
                try:
                    pythoncom.CoUninitialize()
                except:
                    pass
                    
        return info
    except Exception as e:
        print("Erro geral ao ler status da bateria:", e)
        return {"tem_bateria": False}