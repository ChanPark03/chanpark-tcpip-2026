# ex5_python_multiprocessing.py

import multiprocessing, time

# 병렬적으로 실행할 무거운 작업.

def heavy_work(n):
    time.sleep(1) # 1초대기 
    result = n * n 
    print(f"숫자 {n} 계산 완료: {result}")
    return result
if __name__ == "__main__":
    numbers = [1,2,3,4,5,6,7,8]
    print("--멀티 프로세싱 시작---")
    start_time = time.time()
    with multiprocessing.Pool(processes=1) as pool: 
        results = pool.map(heavy_work, numbers)
    end_time = time.time()
    print(f"최종 결과: {results}")
    print(f"총 소요 시간: {end_time-start_time}")