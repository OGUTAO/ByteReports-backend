import psutil
import time

# Variáveis globais para guardar a leitura anterior e comparar com a atual
last_net_io = psutil.net_io_counters()
last_time = time.time()

def get_rede_info():
    global last_net_io, last_time
    
    current_net_io = psutil.net_io_counters()
    current_time = time.time()
    
    time_diff = current_time - last_time
    if time_diff == 0: 
        time_diff = 1 # Evita travamento por divisão por zero
        
    # Calcula os bytes por segundo daquele exato momento
    bytes_recv_per_sec = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_diff
    bytes_sent_per_sec = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_diff
    
    # Converte de Bytes para Megabits por segundo (Mbps) - Padrão de velocidade de internet
    download_mbps = (bytes_recv_per_sec * 8) / 1_000_000
    upload_mbps = (bytes_sent_per_sec * 8) / 1_000_000
    
    # Atualiza a "memória" para a próxima leitura
    last_net_io = current_net_io
    last_time = current_time
    
    # Mantém o histórico total em GB
    recebido_gb = current_net_io.bytes_recv / (1024**3)
    enviado_gb = current_net_io.bytes_sent / (1024**3)

    return {
        "download_mbps": round(download_mbps, 2),
        "upload_mbps": round(upload_mbps, 2),
        "recebido_gb": round(recebido_gb, 2),
        "enviado_gb": round(enviado_gb, 2)
    }