import time
import sys

from constellations.key_value_client import Key_value_client

kvc1 = Key_value_client()
kvc2 = Key_value_client()
time.sleep(10)

kvc1.distributed_set(1, 5)
kvc1.distributed_set(2, 10)
kvc1.distributed_set(3, 15)
kvc1.distributed_set(4, 20)
kvc1.distributed_set(5, 25)
time.sleep(10)
print("key = " + str(1) + " value = " + str(kvc2.distributed_get(1)))
print("key = " + str(2) + " value = " + str(kvc2.distributed_get(2)))
print("key = " + str(3) + " value = " + str(kvc2.distributed_get(3)))
print("key = " + str(4) + " value = " + str(kvc2.distributed_get(4)))
print("key = " + str(5) + " value = " + str(kvc2.distributed_get(5)))

time.sleep(1)
input("Press Enter to continue...")
sys.exit()