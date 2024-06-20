from urllib.request import urlopen
import time
from numpy import mean
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

urls = ['https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/01.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/02.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/03.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/04.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/05.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/06.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/07.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/08.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/09.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/10.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/11.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/12.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/13.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/14.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/15.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/16.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/17.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/18.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/19.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/20.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/21.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/22.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/23.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/24.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/25.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/26.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/27.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/28.png',
        'https://raw.githubusercontent.com/SebastianMerino/Threading/main/images/29.png',
]

def leer_urls(url):
    with urlopen(url) as page:
        image_data = page.read() # data como objeto binario
    return image_data

tiempo_secuencial = []
for _ in range(5):
    inicio = time.perf_counter()
    for url in urls:
        leer_urls(url)
    final = time.perf_counter()
    tiempo_secuencial.append(final - inicio)
tiempo_promedio_secuencial = mean(tiempo_secuencial)    
print(f'El tiempo promedio secuencial es {tiempo_promedio_secuencial}')
    
tiempo_multithread = []
for _ in range(5):    
    inicio = time.perf_counter()
    for url in urls:
        thread = Thread(target=leer_urls, args=(url,))
        thread.start()    
        thread.join()
    final = time.perf_counter()    
    tiempo_multithread.append(final - inicio)
tiempo_promedio_thread = mean(tiempo_multithread)  
print(f'El tiempo promedio multithread es {tiempo_promedio_thread}')

tiempo_multiprocessing = []
for _ in range(5):    
    inicio = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as executor:
        for url in urls:
            executor.submit(leer_urls, url) 
    final = time.perf_counter()    
    tiempo_multiprocessing.append(final - inicio)
tiempo_promedio_multiprocessing = mean(tiempo_multiprocessing)  
print(f'El tiempo promedio multiprocessing es {tiempo_promedio_multiprocessing}')


