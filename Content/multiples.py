def size_converter(size):
    base = 1024
    kilo = base
    mega = base ** 2
    giga = base ** 3
    terra = base ** 4

    if size < kilo:
        size = size
        texto = 'B'
    elif size < mega:
        size /= kilo
        texto = 'Kb'
    elif size < giga:
        size /= mega
        texto = 'Mb'
    elif size < terra:
        size /= giga
        texto = 'Gb'
    size = round(size, 2)
    return f'{size}{texto}'.replace('.', ',')
