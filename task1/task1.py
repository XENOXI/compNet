from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


csv_file = open('eggs.csv', 'w', newline='') 
selected_semester=range(1,7)
login_file = open('login.txt','r')

def read_block(block):
    name = block.find_element(By.CLASS_NAME,'name').text 
    mark = block.find_element(By.CLASS_NAME,'icons').text

    form_of_attestation = block.find_element(By.CLASS_NAME,'isp').text
    form_of_attestation = form_of_attestation.replace('Форма аттестации:','')   

    date = block.find_elements(By.CLASS_NAME,'kurs')
    if len(date)==0:
        date=""
    else:
        date= date[0].text.replace('Дата:','')

    teacher = block.find_elements(By.CLASS_NAME,'teachers')
    if len(teacher)==0:
        teacher=""
    else:
        teacher= teacher[0].text.replace('Преподаватель:','')

    return [name,date,teacher,form_of_attestation,mark]


def login_form(browser:webdriver,login_file):
    login = login_file.readline()
    password = login_file.readline()

    browser.find_element(By.ID,'username').send_keys(login)
    browser.find_element(By.ID,'password').send_keys(password)
    browser.find_element(By.ID,'submitBtn').click()


def init_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)
    browser.get('https://cab.nsu.ru/user/sign-in/auth?authclient=nsu')
    return browser


def create_table(browser:webdriver,selected_semester:list):
    tables = []
    for i in selected_semester:

        atab = browser.find_elements(By.ID,f'atab-1-{i}')
        if (len(atab)==0):
            print("Wrong selected semester. Skiping...")
            continue
        atab[0].click()

        semesterTable = pd.DataFrame([read_block(block) for block in browser.find_elements(By.CLASS_NAME,'item-grade')]).dropna(axis=0)
        tables.append(semesterTable)

    table= pd.concat(tables)

    table = table.rename(columns={0 :'Предмет',
                   1 : 'Дата',
                   2 : 'Преподаватель',               
                   3 : "Форма аттестации",
                   4 : "Оценка"})
    return table


browser = init_browser()

login_form(browser,login_file)

browser.find_element(By.XPATH,"//a[contains(.,'Зачётная книжка')]").click()

table = create_table(browser,selected_semester)

table.to_csv(csv_file)

