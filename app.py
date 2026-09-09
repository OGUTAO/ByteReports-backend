from flask import Flask, jsonify
from flask_cors import CORS
import cpu, ram, disco, gpu, placa_mae, diagnostico
import sistema, bateria, rede

app = Flask(__name__)
CORS(app)

@app.route('/api/hardware', methods=['GET'])
def hardware():
    relatorio = {
        "cpu": cpu.get_cpu_info(),
        "ram": ram.get_ram_info(),
        "armazenamento": disco.get_disco_info(),
        "video": gpu.get_gpu_info(),
        "placa_mae": placa_mae.get_placa_mae_info(),
        "sistema": sistema.get_sistema_info(),
        "bateria": bateria.get_bateria_info(),
        "rede": rede.get_rede_info()
    }
    relatorio["diagnostico_e_sugestoes"] = diagnostico.gerar_sugestoes(relatorio)
    relatorio["resumo_executivo"] = diagnostico.gerar_resumo(relatorio)
    return jsonify(relatorio)

if __name__ == '__main__':
    app.run(debug=True, port=5000)