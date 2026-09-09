def bytes_para_gb(bytes_val):
    try:
        gb = int(bytes_val) / (1024 ** 3)
        return round(gb, 2)
    except (ValueError, TypeError):
        return 0.0