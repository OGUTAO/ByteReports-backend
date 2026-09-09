def gerar_sugestoes(relatorio):
    ram_gb = relatorio.get("ram", {}).get("total_gb", 0)
    gpus = relatorio.get("video", {}).get("placas", [])
    cpu_uso = relatorio.get("cpu", {}).get("uso_medio_porcento", 0)
    particoes = relatorio.get("armazenamento", {}).get("particoes", [])
    tempo_ligado = relatorio.get("sistema", {}).get("tempo_ligado", "")
    
    tem_dedicada = any(g.get("tipo") == "Dedicada" for g in gpus)
    tem_integrada = any(g.get("tipo") == "Integrada" for g in gpus)

    dicas = {
        "Trabalho Leve (Navegação, Pacote Office)": [],
        "Trabalho Médio (Multitarefas, Sistemas Web)": [],
        "Trabalho Pesado (Programação, VMs, Dados)": [],
        "Jogos": [],
        "Gravação de Vídeos (Streaming)": [],
        "Design e Edição": []
    }

    # REGRAS DE SAÚDE DO PROCESSADOR
    if cpu_uso < 60:
        msg_cpu = f"✅ PERFEITO: O Processador está trabalhando com folga (Uso atual: {cpu_uso}%). Há capacidade de processamento de sobra para não travar nas tarefas diárias."
    elif cpu_uso < 85:
        msg_cpu = f"⚠️ AVISO: O Processador está com uso elevado ({cpu_uso}%). O sistema ainda responde bem, mas abrir programas pesados simultâneos pode causar lentidão."
    else:
        msg_cpu = f"⚠️ CRÍTICO: O Processador está sobrecarregado (Uso: {cpu_uso}%). O limite físico foi atingido, o que causa travamentos severos e superaquecimento da máquina."

    # REGRAS DE SAÚDE DO DISCO
    msg_disco = "✅ PERFEITO: O Armazenamento possui excelente espaço livre. O Windows tem área de sobra para salvar arquivos temporários e manter o PC rápido."
    for p in particoes:
        if p.get("uso_porcento", 0) >= 85:
            msg_disco = f"⚠️ CRÍTICO: O Disco {p.get('letra')} está no limite crítico de espaço ({p.get('uso_porcento')}% de uso). Discos muito cheios perdem drasticamente a velocidade, travando o sistema."
            break
            
    for perfil in dicas:
        dicas[perfil].append(msg_cpu)
        dicas[perfil].append(msg_disco)

    # REGRAS DE RAM E VÍDEO (Com Margem de Erro de 3GB para Leitura do Windows)
    if ram_gb < 6: dicas["Trabalho Leve (Navegação, Pacote Office)"].append(f"⚠️ CRÍTICO: O sistema conta com apenas {ram_gb}GB de RAM. O próprio Windows e navegadores consomem isso apenas para manter o computador ligado. A Bytebros recomenda um upgrade urgente.")
    else: dicas["Trabalho Leve (Navegação, Pacote Office)"].append(f"✅ PERFEITO: Com {ram_gb}GB de RAM, o computador tem memória com folga para rodar o sistema e pacotes de escritório de forma perfeitamente fluida.")

    if ram_gb < 13: dicas["Trabalho Médio (Multitarefas, Sistemas Web)"].append(f"⚠️ AVISO: Multitarefas eficientes hoje exigem 16GB de RAM. O Windows usará o armazenamento como 'memória de apoio', causando lentidão. Recomendamos upgrade.")
    else: dicas["Trabalho Médio (Multitarefas, Sistemas Web)"].append(f"✅ PERFEITO: {ram_gb}GB de RAM é o cenário ideal corporativo para operar múltiplos sistemas simultaneamente sem gargalos.")

    if ram_gb < 13: dicas["Trabalho Pesado (Programação, VMs, Dados)"].append(f"⚠️ CRÍTICO: Programação pesada e VMs devoram memória. {ram_gb}GB causará travamentos. Ideal: 32GB.")
    elif ram_gb < 29: dicas["Trabalho Pesado (Programação, VMs, Dados)"].append(f"💡 SUGESTÃO: Com {ram_gb}GB, para rodar múltiplas Máquinas Virtuais sem gargalo, o padrão do mercado de T.I. é o upgrade para 32GB.")
    if not tem_dedicada: dicas["Trabalho Pesado (Programação, VMs, Dados)"].append("⚠️ AVISO: Sem uma Placa Gráfica Dedicada, compilações pesadas demorarão muito mais tempo.")

    if not tem_dedicada:
        dicas["Jogos"].append("⚠️ CRÍTICO: Nenhuma Placa de Vídeo Dedicada detectada! Jogos pesados terão engasgos graves e baixo FPS. Este setup serve apenas para jogos leves.")
        dicas["Jogos"].append("💡 SUGESTÃO: A Bytebros sugere o investimento em uma placa gráfica dedicada ou consultoria para montagem de setup gamer.")
    else: dicas["Jogos"].append("✅ PERFEITO: Hardware de vídeo dedicado ativo. Mantenha as manutenções preventivas em dia para máximo de FPS.")

    if not tem_dedicada: dicas["Gravação de Vídeos (Streaming)"].append("⚠️ CRÍTICO: Fazer transmissões ao vivo sem GPU dedicada é inviável em alta qualidade.")
    if ram_gb < 13: dicas["Gravação de Vídeos (Streaming)"].append(f"⚠️ CRÍTICO: Streaming exige muito do sistema. Com apenas {ram_gb}GB, o seu PC sofrerá travamentos catastróficos.")

    if not tem_dedicada: dicas["Design e Edição"].append("⚠️ CRÍTICO: Softwares como Premiere, Photoshop e AutoCAD dependem de aceleração gráfica por hardware (GPU Dedicada).")
    if ram_gb < 13: dicas["Design e Edição"].append(f"⚠️ CRÍTICO: Edição de vídeo consome muita RAM. Com {ram_gb}GB, edições profissionais serão difíceis.")
    elif ram_gb < 29: dicas["Design e Edição"].append(f"💡 SUGESTÃO: Para fluxos de trabalho 4K e 3D sem lentidão, a Bytebros recomenda fortemente o upgrade para 32GB de RAM.")

    # REGRA: UPTIME
    if "day" in tempo_ligado or "days" in tempo_ligado:
        try:
            dias = int(tempo_ligado.split(" ")[0])
            if dias >= 5:
                aviso_tempo = f"⚠️ CRÍTICO: Esta máquina não é desligada corretamente há {dias} dias! Reinicie o sistema imediatamente para limpar a memória RAM."
                for perfil in dicas:
                    dicas[perfil].insert(0, aviso_tempo)
        except: pass

    return dicas

def gerar_resumo(relatorio):
    ram_gb = relatorio.get("ram", {}).get("total_gb", 0)
    gpus = relatorio.get("video", {}).get("placas", [])
    cpu_nome = relatorio.get("cpu", {}).get("nome", "Processador Desconhecido")
    tempo_ligado = relatorio.get("sistema", {}).get("tempo_ligado", "")
    tem_dedicada = any(g.get("tipo") == "Dedicada" for g in gpus)
    
    alerta_uptime = ""
    if "day" in tempo_ligado or "days" in tempo_ligado:
        try:
            dias = int(tempo_ligado.split(" ")[0])
            if dias >= 5: alerta_uptime = f" ATENÇÃO: Constatou-se uma grave falha de uso, com a máquina ligada ininterruptamente há {dias} dias. Reinicie o sistema imediatamente."
        except: pass

    if ram_gb >= 13 and tem_dedicada: perfil_pc, limitacao = "de alta performance", "O sistema está capacitado para cargas exigentes."
    elif ram_gb >= 13 and not tem_dedicada: perfil_pc, limitacao = "com excelente capacidade multitarefa", "A ausência de placa gráfica dedicada limita o uso para renderização 3D."
    elif ram_gb < 13 and tem_dedicada: perfil_pc, limitacao = "com bom potencial de processamento gráfico", f"Um upgrade de memória RAM é crucial para liberar a performance total da placa de vídeo."
    else: perfil_pc, limitacao = "focada em eficiência básica e tarefas leves", "O upgrade de memória RAM é uma intervenção técnica indispensável para evitar lentidão."

    return f"O equipamento opera com um {cpu_nome} e {ram_gb}GB de RAM. Trata-se de uma estação {perfil_pc}. {limitacao}{alerta_uptime}"