from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker as F
from colorama import Fore as FR, init
import requests as r
import os
import time
import random

init(autoreset=True)
green = FR.GREEN
red = FR.RED
yellow = FR.YELLOW

config =  {
    "chatgpt" : {
        "csrf" : "c3d51fe2f5d98da8a1ae68f90b3e85a81d657f3b3a4f074efb80d903d7b6eef9",
        "host_auth_csrf" : "c3d51fe2f5d98da8a1ae68f90b3e85a81d657f3b3a4f074efb80d903d7b6eef9%7C50d66d7090d9f10d58c0124d53cf15c73b9e82cd6f25c770d005c85317f754aa"
    },
    "settings" : {
        "password" : "@Sangkara12345", # setting password account
        "domain" : "mzastore.com" # domain active from page generator.email
    }
}

class GeneratorEmail:
    def __init__ (self):
        self.session = r.Session()
    
    def validate(self, domain, user):
        data = f"usr={user}&dmn={domain}"
        headers = {
            "Cookie":f"surl={domain}/{user}",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
        }
        while True:
            try:
                return self.session.post("https://generator.email/check_adres_validation3.php", data=data, headers=headers).json()
            except Exception as e:
                print(str(e))
                continue

    def check_email(self, domain, user):
        headers = {
            "Cookie": f"surl={domain}/{user}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        while True:
            try:
                return self.session.get(f"https://generator.email/{domain}/{user}", headers=headers)
            except Exception as e:
                continue

class ChatGPT:
    def __init__(self) -> None:
        self.session = r.Session()
        self.base_page = "https://chatgpt.com/api/auth/signin/login-web"
        self.utils = GeneratorEmail()
        self.option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.option)
        self.option.add_argument("--disable-gpu")
        self.option.add_argument("--window-size=400,400")
        self.option.add_argument("--ignore-certificate-errors")
        self.option.add_argument("--allow-insecure-localhost")
        # self.options.add_extension("proxies.zip") # not god man 403 cf
        
    def generate_page_signup(self) -> None:
        try:
            return r.post(
                self.base_page,
                params={
                    'prompt': 'login',
                    'screen_hint': 'signup',
                    'ext-oai-did': 'cc447a76-ba3c-4351-aef6-18a98d644910',
                    'flow': 'control',
                    'country_code': 'ID',
                },
                cookies={'__Host-next-auth.csrf-token': config['chatgpt']['host_auth_csrf']},
                headers={
                    'content-type': 'application/x-www-form-urlencoded',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                },
                data={
                    'callbackUrl': '/',
                    'csrfToken': config['chatgpt']['csrf'],
                    'json': 'true',
                }
            ).json()['url']
        except Exception as e:
            exit("Check your csrf token mistmacth or invalid")
    
    def exception_inner_html(self) ->None:
        inner_text = self.driver.execute_script("return document.body.innerHTML")
        if "Terlalu banyak pendaftaran dari IP yang sama" in inner_text:
            exit(f"{red}IP Address Limit. Reset your IP or Wait a Minute.")
        elif "challenge-form" in inner_text:
            exit(f"{red}Cloudflare detected. Reset your IP Wait a Minute.")
        
        # handle any response error, add or up to u
    
    def create_account_chatgpt(self) -> bool:
        user = F().first_name().lower() + F().last_name().lower() + str(random.randint(111,999))
        if self.utils.validate(config['settings']['domain'], user)['status'] == 'good':
            email = user + "@" + config['settings']['domain']
            print(f"Proccessing create : {yellow}{email}")
        else: exit(f"{red}Check again your domain valid or nah")
        
        self.driver.get(self.generate_page_signup())
        
        try:
            while True:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(email)
                    self.driver.find_element(By.XPATH, "//button[text()='Lanjutkan']").click()
                    break
                except Exception as e:
                    continue
                
            self.exception_inner_html()
            
            while True:
                try:
                    self.driver.find_element(By.ID, "password").send_keys(config['settings']['password'])
                    self.driver.find_element(By.XPATH, "//button[text()='Lanjut']").click()
                    break
                except Exception as e:
                    continue
            
            self.exception_inner_html()
            
            while True:
                check_url_verify = self.utils.check_email(config['settings']['domain'], user)
                if "ChatGPT" in check_url_verify.text:
                    url_verify = check_url_verify.text.split('<a href="')[4].split('" style="display')[0]
                    with open("account.txt","a") as f:
                        f.write(f"{email}|{config['settings']['password']}|{url_verify}\n")
                    
                    return True
        
        finally:
            self.driver.quit()



os.system('cls' if os.name == "nt" else 'clear')
time.sleep(5)

print(f'''
         ####                 ###                        ###   
  #####   ###       ####    #######    #####   #####   ####### 
 ### ##   #####        ##     ###     ### ##   ### ##    ###      {red}https://t.me/+caTVU9If4ONmYmQ9{FR.RESET}
 ###      ### ##    #####     ###     ### ##   ### ##    ###   
 ### ##   ### ##   ### ##     ###      #####   #####     ###   
  ####    ### ##    #####      ####  ##   ##   ###        #### 
                        ##            #####   ####             
''')

account_created = 0
while True:
    if ChatGPT().create_account_chatgpt():
        account_created += 1
        print(f"{green}Account created : {account_created}")


# Auto create account CHATGPT ( but not auto verify ) 
# Account saved in file aacount.txt format EMAIL|PASSWORD|LINK_URL_VERIFYCATION
# Support : https://t.me/+caTVU9If4ONmYmQ9
