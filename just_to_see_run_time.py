import time


if __name__ == '__main__':
    start = time.time()

    for i in range(20):
        for j in range(20):
            for k in range(20):
                print(i)


end = time.time()
print("The time of execution of above program is :", end-start)