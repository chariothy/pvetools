from utils import run, date_str
from vm import list_vm, ACTIVE_VM

import time

today = date_str()
three_days_ago = date_str(-3)

list_vm()

print(ACTIVE_VM)

for vm_id in ACTIVE_VM:
    run(f'qm snapshot {vm_id} z{today} -vmstate 0 --description "routine"')
    time.sleep(1)
    run(f'qm delsnapshot {vm_id} z{three_days_ago}')