# from concurrent.futures import ThreadPoolExecutor,as_completed
# import time

# def is_positive(n):
#     time.sleep(1)
#     if n > 0:
#         return n
#     else:
#         return None


# numbers = [-1,2,-3,4,-5,6,-6,-10,8,-4]
# filtered_arr = []


# Multi-threadway
# curr_time = time.time()
# with ThreadPoolExecutor(max_workers=len(numbers)) as executor:
#     futures = [executor.submit(is_positive,n) for n in numbers]
#     for future in as_completed(futures):
#         if future.result():
#             filtered_arr.append(future.result())
# end_time = time.time()
            

# print(filtered_arr,f"took {end_time - curr_time}s")



#Single Thread way
# curr_time = time.time()
# for i in numbers:
#     if is_positive(i):
#         filtered_arr.append(i)

# end_time = time.time()
# print(filtered_arr,f"took {end_time-curr_time}s")