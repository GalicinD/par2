#a0 proxy.py 

from db_soc2 import set_proxy, process_sleep

my_proxy = "157.230.250.147:8080"
link_to_proxylist = 'https://hidemyna.me/ru/proxy-list/?maxtime=1000&type=s&anon=34#list'

driver = set_proxy(my_proxy)
driver.get(link_to_proxylist)

process_sleep(20)

data1 = driver.find_elements_by_css_selector(
    '#content-section > section.proxy > div > table > tbody > tr')
data_list = []

for r in range(len(data1)):
    data_list.append((driver.find_element_by_xpath('//*[@id="content-section"]/section[1]/div/table/tbody/tr[%s]/td[1]' % str(r+1)).text,
                      driver.find_element_by_xpath('//*[@id="content-section"]/section[1]/div/table/tbody/tr[%s]/td[2]' % str(r+1)).text))
if data_list:
    with open('proxies.txt', 'w') as f:
        for pr in data_list:
            f.write(':'.join(pr))
            f.write('\n')
            print(':'.join(pr))

print('В списке ', len(data_list), 'прокси. Файл сохранён.')
driver.close()
driver.quit()

