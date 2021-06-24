#!/usr/bin/env python3

import paramiko, sys, os, io, tarfile, subprocess
from pathlib import Path

if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} USERNAME HOST PORT DIR")
    sys.exit(1)

ssh = paramiko.client.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

key_path = os.path.join(Path.home(), '.ssh/id_rsa')
key = paramiko.RSAKey.from_private_key_file(key_path)

ssh.connect(
        hostname=sys.argv[2], 
        username=sys.argv[1],
        port=sys.argv[3],
        pkey=key,
        )

find_cmd = 'find {} -type f'.format(sys.argv[4])

stdin, stdout, stderr = ssh.exec_command('sh')
stdin.write(find_cmd)

stdin.flush()
stdin.channel.shutdown_write()

paths = []

for l in stdout:
    paths.append(l.strip('\n').split(sys.argv[4] + '/')[1])
    print('[FIND STDOUT]\t{}'.format(l.strip('\n')))
    print('[FIND ALTERD]\t{}'.format(paths[-1]))

for l in stderr:
    print('[FIND STDERR]\t{}'.format(l.strip('\n')))

stdin, stdout, stderr = ssh.exec_command('tar cf - -C {} -T -'.format(sys.argv[4]))
stderr_lines = 0
stdout_lines = 0
stdout_type = None

stdin.write("\n".join(paths))

stdin.flush()
stdin.channel.shutdown_write()

untar = subprocess.Popen(
        ["tar", "xf", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        )

tar_data = io.BytesIO()
tar_file = open('/tmp/tartest', 'wb')

for l in stdout:
    l_byte = l.encode()

    untar.stdin.write(l_byte)

    tar_data.write(l_byte)
    tar_file.write(l_byte)

    stdout_lines += 1
    stdout_type = type(l)

    print('[TAR{}]\tReceived {} bytes'.format(stdout_lines, len(l_byte)))

for l in stderr:
    print("[STDERR]\t{}".format(l.strip('\n')))
    stderr_lines += 1

tar_file.close()
untar.stdin.close()

tar_data.seek(0)
tar_obj = tarfile.open(fileobj=tar_data, mode='r')

print(f"Received {stderr_lines} stderr line(s)")
print(f"Received {stdout_lines} stdout line(s)")
print(f"Type of stdout line is {stdout_type}")

for tarinfo in tar_obj:
    print(tarinfo)

tar_obj.close()
ssh.close()
