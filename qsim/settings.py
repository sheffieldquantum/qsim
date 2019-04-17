import os


def enable_cache():
    if 'QSIM_DISABLE_CACHE' in os.environ and os.environ['QSIM_DISABLE_CACHE'].upper() == 'TRUE':
        print("QSim WARNING: Disabling Cache")
        return False
    else:
        return True
