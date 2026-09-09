import wmi
import winreg
import subprocess

def get_placa_mae_info():
    info = {"fabricante": "Desconhecido", "modelo": "Placa Mãe Genérica (Notebook)"}
    
    # 1. Leitura profunda no Registro do Windows (Infalível para marcas como Dell, Lenovo, Acer, HP)
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS")
        fab_sys, _ = winreg.QueryValueEx(key, "SystemManufacturer")
        mod_sys, _ = winreg.QueryValueEx(key, "SystemProductName")
        winreg.CloseKey(key)
        
        if fab_sys and mod_sys and "oem" not in mod_sys.lower():
            info["fabricante"] = fab_sys
            info["modelo"] = mod_sys
            return info
    except:
        pass
    
    # 2. Leitura via CMD
    try:
        mod_cmd = subprocess.check_output("wmic csproduct get name", shell=True, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').split('\n')[1].strip()
        if mod_cmd and "oem" not in mod_cmd.lower():
            info["modelo"] = mod_cmd
            return info
    except:
        pass

    # 3. Leitura padrão WMI
    try:
        w = wmi.WMI()
        for board in w.Win32_BaseBoard():
            if board.Product and board.Product.lower() not in ["base board", "unknown"]:
                info["modelo"] = board.Product
                return info
    except:
        pass
        
    return info