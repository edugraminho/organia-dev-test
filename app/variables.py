from datetime import datetime

# ====================== DIRETÓRIOS LOCAIS e DATAS ======================
DATE_FORMAT = "%Y/%m/%d"
FULL_DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
DATE_NOW: str = datetime.now().strftime(FULL_DATE_FORMAT)
