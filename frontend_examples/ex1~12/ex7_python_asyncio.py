# ex7_python_asyncio.py

import asyncio, time 

async def brew_coffe(name, duration):
    print(f"{name} 커피 주문 접수, {duration} 초 소요 예정 ")
    await asyncio.sleep(duration)
    print(f"{name} 커피 완성")
    return f"{name} 커피"

async def main():
    print("-- 카페 시작 --")
    start_time = time.time()
    task1 = asyncio.create_task(brew_coffe("아이스 아메리카노", 3))
    task2 = asyncio.create_task(brew_coffe("라떼", 2))
    task3 = asyncio.create_task(brew_coffe("스무디", 1))
    results = await asyncio.gather(task1,task2,task3)

    end_time = time.time()
    print(f"총 소요 시간: {end_time - start_time}초")
    print(f"받은 음료: {results}")
    
if __name__ == "__main__":
    asyncio.run(main())
