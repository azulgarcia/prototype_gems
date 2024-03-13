import csv

def eliminar_lineas_duplicadas(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r', newline='') as archivo_entrada, \
            open(archivo_salida, 'w', newline='') as archivo_salida:
        lector_csv = csv.reader(archivo_entrada)
        escritor_csv = csv.writer(archivo_salida)
        lineas_unicas = set()

        for linea in lector_csv:
            tupla_linea = tuple(linea)  # Convertir la lista en una tupla para que sea hasheable
            if tupla_linea not in lineas_unicas:
                escritor_csv.writerow(linea)
                lineas_unicas.add(tupla_linea)


if __name__ == "__main__":
    archivo_entrada = 'top_30_performances_39_3.csv'
    archivo_salida = 'top_30_performances_final.csv'
    eliminar_lineas_duplicadas(archivo_entrada, archivo_salida)

'''
import requests
from urllib.parse import urlencode

user = 'garcia.azul.maria@gmail.com'
password = '18130424'

url_login = 'https://cryptobirds.com/api/auth/login'

login_data = {
    'email': user,
    'password': password
}

response_login = requests.post(url_login, data=urlencode(login_data),
                               headers={'Content-Type': 'application/x-www-form-urlencoded'})

if response_login.status_code == 200:
    limit_gems = 15
    year_url = 2024
    week_url = 5
    url = f"https://cryptobirds.com/api/top-gems-{limit_gems}?withTotal=false&perPage=50&year={year_url}&week={week_url}"

    response = requests.get(url, cookies=response_login.cookies)

    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        print(data)
'''