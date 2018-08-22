from cisco_sdk.devices.switches import CatSwitch

my_swicth = CatSwitch(host='4.71.144.98', username='admin', password='J3llyfish1')

my_swicth.sync_cpu_status()


x = my_swicth.cpu_status.is_high
print(x)
y = my_swicth.cpu_status.is_higher_than(1)
print(y)
z = my_swicth.cpu_status.cpu_5_sec

print(my_swicth.cpu_status)