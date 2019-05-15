def solve_unit(param):
    device_para_with_unit = str(param)                                     #change unit to num >
    device_para_unit = device_para_with_unit[-1]
    if device_para_unit == 'k':#change unit to nums
        unit = 1000
        device_para = device_para_with_unit.rstrip('k')
    elif device_para_unit == 'g':
        if device_para_with_unit[-2] == 'e':
            unit = 1000000
            device_para = device_para_with_unit.rstrip('meg')
        else:
            unit = 1000000000
            device_para = device_para_with_unit.rstrip('g')
    elif device_para_unit == 'm':
        unit = 0.001
        device_para = device_para_with_unit.rstrip('m')
    elif device_para_unit == 'u':
        unit = 0.000001
        device_para = device_para_with_unit.rstrip('u')
    elif device_para_unit == 'n':
        unit = 0.000000001
        device_para = device_para_with_unit.rstrip('n')
    elif device_para_unit == 'p':
        unit = 0.000000000001
        device_para = device_para_with_unit.rstrip('p')
    elif device_para_unit == 'f':
        unit = 0.000000000000001
        device_para = device_para_with_unit.rstrip('f')
    else:
        unit = 1
        device_para = device_para_with_unit
    device_para_num = float(device_para) * unit
    return device_para_num
