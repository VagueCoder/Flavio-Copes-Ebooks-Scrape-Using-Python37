
def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'Kilo', 2: 'Mega', 3: 'Giga', 4: 'Tera'}
    while size > power:
        size /= power
        n += 1
    return f'{size:.2f} {power_labels[n]}bytes'

def main():
    print('2,147,483,648 Bytes = ', format_bytes(2147483648))

if __name__=='__main__':
    main()