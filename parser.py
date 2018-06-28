def parse(src_data, port, origin):
    fin_data = src_data
    if origin == 'client':
        if src_data.count(ord('A')) >= 2:
            print(src_data.hex()[:4*2], len(src_data))

		# this check fails when client sends longer messages
        if src_data[1] == 0x00 and src_data[2] == 0x02:
            cnt = (len(src_data) - 4)
            barr = b'PWNED! '
            payload = ( barr * (cnt // len(barr) + (cnt % len(barr) != 0)) )[:cnt]
            fin_data = src_data[:4] + payload

    return fin_data
