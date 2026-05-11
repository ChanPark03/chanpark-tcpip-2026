# ex6_python_threading.py

import time, threading

def download_data(site_name, delay) :
    print(f"{site_name} 다운로드 시작 ...")
    time.sleep(delay)
    print(f"{site_name} 다운로드 완료: {delay} 초 소요")

if __name__ == "__main__" : 
    sites = [("Google", 2),
             ("Naver", 3),
             ("Github", 1),
             ("Youtube", 2)]
    threads = []
    print("---멀티 스레딩 시작---")
    start_time = time.time()
    for name, delay in sites: #4 번 반복
        thread = threading.Thread(target=download_data,
                                  args=(name,delay))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"총 소요 시간: {end_time - start_time}초")