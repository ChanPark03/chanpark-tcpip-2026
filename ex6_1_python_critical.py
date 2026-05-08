# ex6_1_python_critical.py
# 공유자원 = 은행잔고 

import threading
total_balance = 0 # 은행 잔고 

def deposit(amount) :
    global total_balance
    for i in range(amount): #amount 0~ amount -1 
        total_balance += 1
        
if __name__ == "__main__" :
    t1 = threading.Thread(target=deposit, args=(1000000,))
    t2 = threading.Thread(target=deposit, args=(1000000,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    print(f"최종 잔고: {total_balance}원")
    print(f"최종 잔고 기대값: {200000}원")