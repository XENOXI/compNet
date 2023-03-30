from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def read_block(block)->list:
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



def login_form(browser:webdriver,login,password):
    browser.find_element(By.ID,'username').send_keys(login)
    browser.find_element(By.ID,'password').send_keys(password)
    browser.find_element(By.ID,'submitBtn').click()


def init_browser(link)->webdriver:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)
    browser.get(link)
    #browser.get('https://cab.nsu.ru/user/sign-in/auth?authclient=nsu')
    return browser

# Функйия для создания таблицы
def create_table(browser:webdriver,selected_semester:list)->pd.DataFrame:
    tables = []
    for i in selected_semester:

        atab = browser.find_elements(By.ID,f'atab-1-{i}')
        if (len(atab)==0):
            print("Wrong selected semester. Skiping...")
            continue
        atab[0].click()

        # получает датафрейм по блокам на странице
        semester_table = pd.DataFrame([read_block(block) for block in browser.find_elements(By.CLASS_NAME,'item-grade')]).dropna(axis=0)
        tables.append(semester_table)

    table= pd.concat(tables)

    table = table.rename(columns={0 :'Предмет',
                   1 : 'Дата',
                   2 : 'Преподаватель',               
                   3 : "Форма аттестации",
                   4 : "Оценка"})
    return table


def parse(link,login,password,selected_semester):
    browser = init_browser(link)
    login_form(browser, login,password)
    browser.find_element(By.XPATH, "//a[contains(.,'Зачётная книжка')]").click()
    table = create_table(browser, selected_semester)
    return table.to_csv()

