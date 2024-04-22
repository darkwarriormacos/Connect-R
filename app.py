from flask import Flask, render_template, request, redirect, url_for
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_wol', methods=['POST'])
def send_wol():
    mac_address = request.form['mac_address']
    send_magic_packet(mac_address)
    return redirect('https://getscreen.me/dashboard/agents')

def send_magic_packet(mac_address):
    mac_bytes = bytearray.fromhex(mac_address.replace(':', ''))
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, ('192.168.1.70', 9))

if __name__ == '__main__':
    app.run(debug=True)