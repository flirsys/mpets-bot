import requests, time
import datetime
import random
from colorama import init, Fore
from colorama import Back
from colorama import Style

init(autoreset=True)

r = requests.Session()
host = "mpets.mobi"
url = "https://"+host
info = Fore.BLUE+Back.YELLOW+"INFO"+Back.BLACK+Fore.WHITE


print(Fore.BLUE+"Запуск клиента для "+Back.GREEN+host)

id=""
PHPSESSID=""
hash=""
verify=""

cookies = {"PHPSESSID": PHPSESSID, "id": id, "hash": hash, "verify": verify}
headers = {'User-Agent': 'Mozilla/5.0'}

lastime = 0
showid = 0

def getId():
    conf = r.get(url+"/settings", cookies=cookies)
    print(info+" "+Fore.GREEN+"ID: "+conf.text.partition('персонажа:')[2].partition('</div>')[0])
    print(conf.text)

def main():
    global showid
    if(showid == 0):
        #getId()
        showid = 1
    global lastime
    delta = datetime.timedelta(hours=3, minutes=0)
    t = (datetime.datetime.now(datetime.timezone.utc) + delta)
    htime = t.strftime("%H:%M")
    if(lastime != htime):
        lastime = htime
        delta = datetime.timedelta(hours=3, minutes=0)
        t = (datetime.datetime.now(datetime.timezone.utc) + delta)
        htime = Fore.CYAN+t.strftime("%H:%M")+Fore.WHITE


        home = r.get(url, cookies=cookies)

#Сбор Монет
        money = r.get(url+"/show_coin", cookies=cookies)
        if('Получить' in money.text):
            money2 = r.get(url+"/show_coin_get", cookies=cookies)
            print("["+htime+"]"+info+" "+Fore.GREEN+"Монеты собраны. "+money2.text.partition('coin.png " alt>')[2].partition('</')[0])

#Уход за петомцем 
        if('wakeup_sleep' in home.text or 'Играть ещё' in home.text):
            print("["+htime+"]: "+Fore.GREEN+"Всё сделано на /home, осталось "+home.text.partition('через:')[2].partition('<')[0])
        else:
            raz = 0
            print("["+htime+"]: Ухаживаем")
            home = r.get(url, cookies=cookies)
            if('wakeup' in home.text):
                wakeup = r.get(url+"/wakeup", cookies=cookies)
                raz = 0
            print ("["+htime+"]"+info+" кормим; играем; идем на выставку"+Back.YELLOW+"X5")
            while (raz < 6):
                rand = random.randint(0, 9999)
                homefood = r.get(url+"/?action=food&rand={rand}", cookies=cookies)
                homefood = r.get(url+"/?action=play&rand={rand}", cookies=cookies)
                homeshow = r.get(url+"/show", cookies=cookies)
                raz = raz + 1
                if('wakeup_sleep' in home.text):
                    raz = 0
    time.sleep(5)


while True:
    try:
        main()
    except Exception as exc:
        print("Нет соединения")
        time.sleep(10)