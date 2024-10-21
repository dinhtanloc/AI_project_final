# utils.py
from vnstock3 import Vnstock

def get_vnstock_VCI(symbol):
    """Trả về một đối tượng Vnstock cho mã cổ phiếu."""
    return Vnstock().stock(symbol=symbol, source='VCI')

def get_vnstock_TCBS(symbol):
    """Trả về một đối tượng Vnstock cho mã cổ phiếu."""
    return Vnstock().stock(symbol=symbol, source='TCBS')
