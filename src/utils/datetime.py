""" Funciones para trabajar con fechas y tiempo """

from datetime import datetime, timedelta

def get_actual_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def add_days_actual_date(days):
    now = datetime.now()
    days = timedelta(days = days)
    final_date = now + days
    return final_date.strftime("%Y-%m-%d %H:%M:%S")

def get_day_of_week_number():
    # Comienza en 0 con lunes
    return datetime.today().weekday()

def holiday():
    from datetime import date
    import datetime
    import json
    import pycurl
    from io import BytesIO
    now = str((datetime.datetime.now() + datetime.timedelta(days=1))).split(" ")[0]
    yearr=str(date.today().year)
    url = "https://apis.digital.gob.cl/fl/feriados/"+str(yearr)
    payload={}
    headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
    salida = True
    try:
        b_obj = BytesIO()
        crl = pycurl.Curl()
        crl.setopt(crl.URL,url)
        crl.setopt(crl.WRITEDATA, b_obj)
        crl.perform()
        crl.close()
        get_body = b_obj.getvalue()
        if now in get_body.decode('utf8'):
            json_load = json.loads(get_body.decode('utf8'))
            for data in json_load:
                if(data["fecha"] == now):
                    salida = False
                    break
    except:
        print("fallo conexion api "+url)
    return salida
