# ByteReports

Um aplicativo modular em Python projetado para ler informações detalhadas de hardware em computadores Windows e gerar relatórios simples, explicativos e úteis para usuários leigos.

## Funcionalidades

* **Leitura Profunda:** Utiliza o WMI do Windows para acessar dados que bibliotecas comuns não conseguem (como pentes físicos de RAM e versão da BIOS).
* **Arquitetura Modular:** O back-end é dividido em módulos (`cpu.py`, `ram.py`, `gpu.py`, etc.), permitindo que o front-end solicite apenas os dados necessários.

## Tecnologias Utilizadas

* Python 3.x
* Bibliotecas principais: `wmi`, `psutil`, `py-cpuinfo`, `gputil`



## Passo definitivo de instalação do Back-end no CMD em uma nova máquina:

PASSO 1: Os Programas Obrigatórios (Devem ser instalados antes de qualquer outro passo)
1° Python: Baixe e instale o Python (marque a caixa "Add Python to PATH" durante a instalação, isso é crucial).
2° Node.js: Baixe e instale o Node.js (ele já vem com o npm embutido).

PASSO 2: Abrir a pasta do Back-end no CMD/
Bash:
cd "local_onde_esta_a_pasta" "nome_da_pasta"

PASSO 3: Configurar o Back-end (Python)
Bash:
pip install flask flask-cors psutil wmi GPUtil py-cpuinfo pypiwin32

PASSO 4: Rodar o Back-end/
Bash: 
python app.py
