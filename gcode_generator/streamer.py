import requests


def post_gcode(gcode: str, url: str, max_load_kB: float = 1):
    payload = b""
    payload_size = 0
    try:
        for l in gcode.splitlines(keepends=True):
            new_line = l.encode()
            if (payload_size + len(new_line)) < max_load_kB * 1e3:
                payload += new_line
                payload_size += len(new_line)
            else:
                print("POST\n{}".format(payload.decode()))
                r = requests.post(url, payload, timeout=30)
                payload = new_line
                payload_size = len(new_line)
    finally:
        rst_msg = ";Pen Up\nM300 S135\nG4 P120\nG1 X0.0 Y0.0 F775.0"
        payload = rst_msg.encode()
        print("POST\n{}".format(payload.decode()))
        r = requests.post(url, payload, timeout=5)