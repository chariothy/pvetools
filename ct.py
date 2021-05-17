import re

from utils import run, logger


ACTIVE_CT = {}
REG_CT = re.compile(r'\s*(\d+)\s+(\w+)\s+(\w+)')


def list_ct(running=True):
    ct_list_str = run('pct list')
    logger.debug(ct_list_str)
    '''
    VMID       Status     Lock         Name
    103        stopped                 alpine
    112        running                 mysql
    128        running                 ng
    130        stopped                 alpine-docker
    131        stopped                 alpine-de
    138        stopped                 debian
    139        stopped                 debian-docker
    140        stopped                 debian-de
    '''
    ct_list = ct_list_str.split('\n')

    global ACTIVE_CT
    for ct in ct_list:
        match = REG_CT.findall(ct)
        if match:
            # TODO: check if Lock exists
            ct_id, ct_stat, ct_name = match[0]
            if ct_stat == 'running' or not running:
                ACTIVE_CT[ct_id] = ct_name
                
                
def resume_ct(ct_id):
    '''
pct resume <vmid>

       Resume the container.

       <vmid>: <integer> (1 - N)
           The (unique) ID of the VM.
    '''
    run(f'pct resume {ct_id}')
    logger.info(f'Resumed ct {ct_id}')


def stop_ct(ct_id):
    '''
 pct stop <vmid> [OPTIONS]

       Stop the container. This will abruptly stop all processes running in the container.

       <vmid>: <integer> (1 - N)
           The (unique) ID of the VM.

       --skiplock <boolean>
           Ignore locks - only root is allowed to use this option.

    '''
    run(f'pct stop {ct_id}')
    logger.info(f'Stopped CT {ct_id}')


def suspend_ct(ct_id):
    '''
 pct suspend <vmid>

       Suspend the container.

       <vmid>: <integer> (1 - N)
           The (unique) ID of the VM.
    '''
    run(f'pct suspend {ct_id}')
    logger.info(f'Suspended ct {ct_id}')