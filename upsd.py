import re
import os
import sys
import time

from utils import run, logger
from vm import list_vm, resume_vm, suspend_vm, ACTIVE_VM
from ct import list_ct, resume_ct, suspend_ct, ACTIVE_CT

REG_UPS_CHARGE = re.compile(r'battery\.charge\:\s+(\d+)')
REG_UPS_CHARGE_LOW = re.compile(r'battery\.charge\.low\:\s+(\d+)')
REG_UPS_CHARGE_WARNING = re.compile(r'battery\.charge\.warning\:\s+(\d+)')
REG_UPS_MFR = re.compile(r'device\.mfr\:\s+(\w+)')
REG_UPS_MODEL = re.compile(r'device\.model\:\s+([\w\- \d]+)')	#NOTICE: Space in [ ]

ARG = sys.argv[-1]
UPS_NAME = ''
UPS_LOW = None
UPS_WARNING = None
UPS_SUSPEND = None
ONBATT_TIMEOUT = 3 * 180        # 如果3分钟UPS还是100%，则认为是FAKE SIGNAL

def get_ups_charge():
    global UPS_NAME, UPS_LOW, UPS_WARNING

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
    
    if UPS_LOW is None:
        match = REG_UPS_CHARGE_LOW.findall(ups_status)
        UPS_LOW = int(match[0])
        
        match = REG_UPS_CHARGE_WARNING.findall(ups_status)
        UPS_WARNING = int(match[0])
        
        UPS_SUSPEND = (UPS_WARNING - UPS_LOW) * 0.6 + UPS_LOW
    return ups_charge


ups_charge = get_ups_charge()
header = ('' if ARG == '--pause' else '\x1b[5;30;47[(DRY MODE)m]\x1b[0m ') + f'\x1b[5;30;43m[{UPS_NAME}]\x1b[0m'
logger.info(f'{header} monitor starts: arg - {ARG}')
logger.warning(f'**(To suspend VM & CT, use --pause)**')
logger.info('{} battery charge - {} (low - {}, warning - {})'.format(header, ups_charge, UPS_LOW, UPS_WARNING))

detect_on_battery = 0
while detect_on_battery < ONBATT_TIMEOUT:
    ups_charge = get_ups_charge()
    if ups_charge < 100:
        break
    time.sleep(3)
    detect_on_battery += 3
    #print(detect_on_battery, ONBATT_TIMEOUT, detect_on_battery < ONBATT_TIMEOUT)
    print('=', end='', flush=True)
    
if detect_on_battery >= ONBATT_TIMEOUT:
    logger.info('{} not on battery within {} seconds, now exiting.'.format(header, ONBATT_TIMEOUT))
    sys.exit(0)
    

list_vm()
#print(ACTIVE_VM)

list_ct()
#print(ACTIVE_CT)

logger.info('{} is on battery, charge - {} (low - {}, warning - {})'.format(header, ups_charge, UPS_LOW, UPS_WARNING))

def suspend_vm_ct():
    for vm_id in ACTIVE_VM:
        suspend_vm(vm_id)
        time.sleep(1)

    for ct_id in ACTIVE_CT:
        suspend_ct(ct_id)
        time.sleep(1)


def resume_vm_ct():
    for vm_id in ACTIVE_VM:
        resume_vm(vm_id)
        time.sleep(1)

    for ct_id in ACTIVE_CT:
        resume_ct(ct_id)
        time.sleep(1)

vm_suspended = False
old_ups_charge = 0
while ups_charge < 100:
    ups_charge = get_ups_charge()
    if ups_charge > old_ups_charge:
        logger.info(f'[{header}] - battery is charging: {ups_charge} (low: {UPS_LOW}, warning: {UPS_WARNING})')
    elif ups_charge < old_ups_charge:
        logger.info(f'[{header}] - battery is discharging: {ups_charge} (low: {UPS_LOW}, warning: {UPS_WARNING})')
        if ups_charge < UPS_WARNING:
            logger.warning(f'[{header}] - battery is under warning, charge: {ups_charge} (low: {UPS_LOW}, warning: {UPS_WARNING})')
            logger.warning(f'[{header}] -     pve will be suspended at {UPS_SUSPEND}')
            if ups_charge < UPS_SUSPEND:
                logger.warning(f'[{header}] - battery is under {UPS_SUSPEND}, now suspending...')
                if ARG == '--pause':
                    suspend_vm_ct()
                logger.info(f'[{header}] - All VM has been suspended.')
                vm_suspended = True
                break
    time.sleep(3)
    old_ups_charge = ups_charge

if vm_suspended:
    old_ups_charge = 0
    while ups_charge < 100:
        ups_charge = get_ups_charge()
        if ups_charge > old_ups_charge:
            logger.info(f'[{header}] - battery is charging, charge: {ups_charge} (low: {UPS_LOW}, warning: {UPS_WARNING})')
        elif ups_charge < old_ups_charge:
            logger.info(f'[{header}] - battery is on battery again, now turn over to another instance.')
            sys.exit(0)
        time.sleep(3)
        old_ups_charge = ups_charge

    logger.info(f'[{header}] - battery is full, now resuming...')
    if ARG == '--pause':
        resume_vm_ct()
    logger.info(f'[{header}] - UPS recoverd & all VM has been resumed.')
else:
    logger.info(f'[{header}] - UPS recoverd and full.')