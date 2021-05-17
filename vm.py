import re
import time

from utils import run, logger


ACTIVE_VM = {}
REG_VM = re.compile(r'\s+(\d+)\s+(\w+)\s+(\w+)')

def stop_vm(vm_id):
    '''
qm stop <vmid> [OPTIONS]

       Stop virtual machine. The qemu process will exit immediately. Thisis akin to pulling the power plug of a running computer and may damage the VM data

       <vmid>: <integer> (1 - N)
           The (unique) ID of the VM.

       --keepActive <boolean> (default = 0)
           Do not deactivate storage volumes.

       --migratedfrom <string>
           The cluster node name.

       --skiplock <boolean>
           Ignore locks - only root is allowed to use this option.

       --timeout <integer> (0 - N)
           Wait maximal timeout seconds.
    '''
    run(f'qm stop {vm_id}')
    logger.info(f'Stopped VM {vm_id} ({ACTIVE_VM[vm_id]})')


def resume_vm(vm_id):
    '''
qm resume <vmid> [OPTIONS]

       Resume virtual machine.

       <vmid>: <integer> (1 - N)
           The (unique) ID of the VM.

       --nocheck <boolean>
           no description available

       --skiplock <boolean>
           Ignore locks - only root is allowed to use this option.
    '''
    run(f'qm resume {vm_id}')
    logger.info(f'Resumed VM {vm_id} ({ACTIVE_VM[vm_id]})')


def suspend_vm(vm_id):
    '''
 qm suspend <vmid> [OPTIONS]

       Suspend virtual machine.

       <vmid>: <integer> (1 - N)
           The (unique) ID of the VM.

       --skiplock <boolean>
           Ignore locks - only root is allowed to use this option.

       --statestorage <string>
           The storage for the VM state

               Note
               Requires option(s): todisk

       --todisk <boolean> (default = 0)
           If set, suspends the VM to disk. Will be resumed on next VM start.
    '''
    run(f'qm suspend {vm_id}')
    logger.info(f'Suspended VM {vm_id} ({ACTIVE_VM[vm_id]})')


def list_vm():
    vm_list_str = run('qm list')
    logger.debug(vm_list_str)
    '''
    VMID NAME                 STATUS     MEM(MB)    BOOTDISK(GB) PID
        100 web                  running    10240             80.00 4070
        101 opv0adm              running    1024               0.00 2442
        104 debian               stopped    10240             80.00 0
        106 debian-docker        stopped    10240             80.00 0
        108 dsm3617              running    4096               0.05 25142
        109 win10                stopped    4096             100.00 0
        110 print                running    2048              80.00 3000
        111 opvlan               stopped    1024               0.00 0
        113 opv6net              running    1024               0.00 1919
        114 debian-ui            stopped    4096              32.00 0
        115 opv7dev              running    1024               0.00 3496
        116 opv8apg              running    1024               0.00 12656
        117 gitea                running    1024              80.00 27202
        118 builder              running    8192              80.00 9708
        119 sit                  running    4096              80.00 21506
        120 website-efi          stopped    8192              32.00 0
    '''
    vm_list = vm_list_str.split('\n')

    global ACTIVE_VM
    for vm in vm_list:
        match = REG_VM.findall(vm)
        if match:
            vm_id, vm_name, vm_stat = match[0]
            if vm_stat == 'running':
                ACTIVE_VM[vm_id] = vm_name