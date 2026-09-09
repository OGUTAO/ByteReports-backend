import wmi
import pythoncom
import GPUtil

def get_gpu_info():
    info = {"placas": []}
    try:
        # Inicializa o COM do Windows para esta Thread do Flask
        pythoncom.CoInitialize()
        
        w = wmi.WMI()
        
        # Puxa os dados avançados da NVIDIA (Uso Real e Temperatura via GPUtil)
        nv_gpus = []
        try:
            nv_gpus = GPUtil.getGPUs()
        except:
            pass
            
        # O laço for garante que ele leia TODAS as placas
        for gpu in w.Win32_VideoController():
            nome = gpu.Name or "GPU Desconhecida"
            nome_lower = nome.lower()
            
            # 1. FILTRO DE FANTASMAS (Ignora telas virtuais do Meta/Citrix e drivers básicos)
            if "virtual" in nome_lower or "basic display" in nome_lower or "software" in nome_lower:
                continue
                
            # 2. CLASSIFICAÇÃO (Dedicada vs Integrada)
            tipo = "Dedicada"
            if "nvidia" in nome_lower or "geforce" in nome_lower:
                tipo = "Dedicada"
            elif "intel" in nome_lower and any(x in nome_lower for x in ["hd", "uhd", "iris", "graphics"]):
                tipo = "Integrada"
            elif "amd" in nome_lower or "radeon" in nome_lower:
                if "rx " in nome_lower:
                    tipo = "Dedicada"
                elif "graphics" in nome_lower or "vega" in nome_lower:
                    tipo = "Integrada"
                    
            # 3. LEITURA DE VRAM
            try:
                vram_bytes = abs(int(gpu.AdapterRAM))
                vram_gb = round(vram_bytes / (1024**3), 1)
                vram_str = f"{vram_gb} GB" if vram_gb > 0 else "N/A"
            except:
                vram_str = "N/A"
            
            uso = 0
            temp = None
            
            # 4. LEITURA EM TEMPO REAL (Sobrescreve com dados do GPUtil se for NVIDIA)
            if "nvidia" in nome_lower:
                for nv in nv_gpus:
                    uso = int(nv.load * 100)
                    temp = nv.temperature
                    vram_str = f"{round(nv.memoryTotal / 1024, 1)} GB"
                    break
                    
            info["placas"].append({
                "nome": nome,
                "tipo": tipo,
                "uso": uso,
                "driver_versao": gpu.DriverVersion or "N/A",
                "vram_gb": vram_str,
                "temperatura_c": temp
            })
            
    except Exception as e:
        print("Erro ao tentar ler as Placas de Vídeo:", e)
        
    finally:
        # Fecha a comunicação no final para evitar vazamento de memória
        try:
            pythoncom.CoUninitialize()
        except:
            pass
            
    return info