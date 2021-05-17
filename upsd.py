
import re
import time

from utils import run, logger
from vm import list_vm, resume_vm, suspend_vm, ACTIVE_VM

REG_UPS_CHARGE = re.compile(r'battery\.charge\:\s+(\d+)')
REG_UPS_MFR = re.compile(r'device\.mfr\:\s+(\w+)')
REG_UPS_MODEL = re.compile(r'device\.model\:\s+([\w\- \d]+)')	#NOTICE: Space in [ ]

UPS_NAME = ''

def get_ups_charge():
    global UPS_NAME

    ups_status = run('upsc ups@10.8.9.2')
    #print(ups_status)

    global UPS_NAME
    if not UPS_NAME:
        match = REG_UPS_MFR.findall(ups_status)
        UPS_NAME += match[0]
        UPS_NAME += ' '
        match = REG_UPS_MODEL.findall(ups_status)
        UPS_NAME += match[0]

    match = REG_UPS_CHARGE.findall(ups_status)
    #print(match)
    ups_charge = int(match[0])
    #print(ups_charge)
    return ups_charge


list_vm()

print(ACTIVE_VM)
print(UPS_NAME)

for vm_id in ACTIVE_VM:
    suspend_vm(vm_id)
    time.sleep(1)
    
ups_charge = 0
while ups_charge < 100:
    ups_charge = get_ups_charge()
    logger.info(f'[{UPS_NAME}] - battery charge: {ups_charge}')
    time.sleep(3)

for vm_id in ACTIVE_VM:
    resume_vm(vm_id)
    time.sleep(1)

logger.info(f'[{UPS_NAME}] - UPS recoverd & all VM resumed.')