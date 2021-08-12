## AUTHOR == Karan Nayak

import subprocess
import os
import csv
import MySQLdb
from bs4 import BeautifulSoup
import datetime
import time
from termcolor import colored
import base64
import mysql.connector
from mysql.connector import Error
import smtplib
import base64
import email.message
import email.utils
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Function to transfer Email data
def sqldb_email(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')
        
    print(colored("\n[*]  Connected to SQL DB for transferring all the emails data",'red'))

    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/emails.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split()

    values = []
    values = [line.split() for line in file_content]

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    for each_tuple in values_2[2:]:
        query = "INSERT INTO emails(email_id, domain_searched, scanned_timestamp) VALUES(%s,%s,%s)"
        cursor.execute(query, each_tuple)

    #close the connection to the database.
    db.commit()
    cursor.close()
    print(colored("[*]  Done transferring all the emails data",'blue'))


def sqldb_names(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
    port=3306,
    user='root',
    password=password,
    database='discover_dump',
    charset='utf8mb4')
    
    print(colored("\n[*]  Connected to SQL DB for transferring all the names data", 'red'))

    def end():
        db.commit()
        cursor.close()
    print(colored("[*]  Done transferring all the names data",'blue'))

    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/names.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close


    with open("report.txt") as f:
        file_content = f.read().split()
    

    values = []

    for i,string in enumerate(file_content):
        if file_content[i] == '|' and file_content[i+1] == '|' and file_content[i+2] == '|':
            values.append('|')
            values.append('nil')
        else:
            values.append(string)                 


    updated_values = [*filter(None, map(str.strip, ' '.join(values).split('|')))] 


    it = iter(updated_values[5:])
    updated_values_1 = list(zip(it, it, it))

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in updated_values_1:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    for each_tuple in values_2:
        try:
            query = "INSERT INTO names(last_name, first_name, titles, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(query,each_tuple)
        except:
            end()
    end()



def sqldb_dns_records(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')

    print(colored("\n[*]  Connected to SQL DB for transferring all the dns_records",'red'))

    def end():
        db.commit()
        cursor.close()
    print(colored("[*]  Done with tranferring all the dns_records data", 'blue'))


    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/records.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split('\n')

    values = []
    for line in file_content:
        new_list = line.split()
        values.append(tuple(new_list))

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    test_list = ['A', 'NS', 'MX']

    for each_tuple in values_2[13:-2]:
        test_list_2 = list(each_tuple)
        try:
            if test_list_2[0] in test_list:
                query = "INSERT INTO dns_records(dns_type, dns_name, IP, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
                test_list_3 = tuple(test_list_2)
                cursor.execute(query,test_list_3) 
            elif test_list_2[0] == 'SRV':
                query = "INSERT INTO dns_records(dns_type, service_protocol_name, dns_name, IP, port, priority, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                test_list_3 = tuple(test_list_2)
                cursor.execute(query,test_list_3)
            else:
                test_list_2[2:-2] = ['__'.join(test_list_2[2:-2])]
                query = "INSERT INTO dns_records(dns_type, dns_name, miscellaneous, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
                test_list_3 = tuple(test_list_2)
                cursor.execute(query,test_list_3)
        except:
            end()
    end()


def sqldb_dns_records_misc(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')

    print(colored("\n[*]  Connected to SQL DB for transferring all the dns_records",'red'))

    def end():
        db.commit()
        cursor.close()
    print(colored("[*]  Done with tranferring all the dns_records data", 'blue'))


    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/records.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split('\n')

    values = []
    for line in file_content:
        new_list = line.split()
        values.append(tuple(new_list))

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    test_list = ['A', 'NS', 'MX', 'SRV']

    for each_tuple in values_2[13:-2]:
        test_list_2 = list(each_tuple)
        try:
            if test_list_2[0] not in test_list:
                test_list_2[2:-2] = ['__'.join(test_list_2[2:-2])]
                query = "INSERT INTO dns_records_misc(dns_type, dns_name, miscellaneous, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
                test_list_3 = tuple(test_list_2)
                cursor.execute(query,test_list_3)
            else:
                pass
        except:
            end()
    end()


def sqldb_hosts(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')

    print(colored("\n[*]  Connected to SQL DB for transferring host details",'red'))

    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/hosts.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split()

    values = [line.split() for line in file_content]

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    for line in values_2[2:]:
        query = "INSERT INTO hosts(Hosts_IP, domain_searched, scanned_timestamp) VALUES(%s,%s,%s)"
        cursor.execute(query, line)

    #close the connection to the database.
    db.commit()
    cursor.close()
    print(colored("[*]  Done with transferring all the host records to SQL db",'blue'))


def sqldb_reg_domain(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))
    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')

    print(colored("\n[*]  Connected to SQL DB to transfer registered domains data",'red'))


    def hasnumbers(inputString):
        return any(char.isdigit() for char in inputString)

    #close the connection to the database.
    def end():
        db.commit()
        cursor.close()
    print(colored("[*]  Done with transferring registered domains data",'blue'))


    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/registered-domains.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split('\n')

    values = []

    for line in file_content:
        new_list = line.split('  ')
        new_list = filter(None,new_list)
        values.append(tuple(new_list))

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    for each_tuple in values_2[17:-2]:
        test_list = list(each_tuple)
        try:
            if len(test_list) == 7:
                query = "INSERT INTO reg_domain(domain, ip_address, reg_email, reg_org, registrar, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                test_list_2 = tuple(test_list)
                cursor.execute(query,test_list_2)

            elif len(test_list) == 6:
                if hasnumbers(test_list[1]) == False:
                    query = "INSERT INTO reg_domain(domain, reg_email, reg_org, registrar, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s,%s)"
                    test_list_2 = tuple(test_list)
                    cursor.execute(query,test_list_2)
                else:
                    query = "INSERT INTO reg_domain(domain, ip_address, reg_org, registrar, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s,%s)"
                    test_list_2 = tuple(test_list)
                    cursor.execute(query,test_list_2)
            elif len(test_list) == 5:
                if hasnumbers(test_list[1]) == False:
                    if "@" not in test_list[1]:
                        query = "INSERT INTO reg_domain(domain, reg_org, registrar, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
                        test_list_2 = tuple(test_list)
                        cursor.execute(query,test_list_2)
                    else:
                        query = "INSERT INTO reg_domain(domain, reg_email, reg_org, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
                        test_list_2 = tuple(test_list)
                        cursor.execute(query,test_list_2)
                else:
                    if '@' not in test_list[2]:
                        query = "INSERT INTO reg_domain(domain, ip_address, reg_org, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
                        test_list_2 = tuple(test_list)
                        cursor.execute(query,test_list_2)
                    else:
                        query = "INSERT INTO reg_domain(domain, ip_address, reg_email, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
                        test_list_2 = tuple(test_list)
                        cursor.execute(query,test_list_2)
            elif len(test_list) == 4:
                if hasnumbers(test_list[1]) == False:
                    if '@' not in test_list[1]:
                        query = "INSERT INTO reg_domain(domain, reg_org, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s)"
                        test_list_2 = tuple(test_list)
                        cursor.execute(query,test_list_2)
                    else:
                        query = "INSERT INTO reg_domain(domain, reg_email, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s)"
                        test_list_2 = tuple(test_list)
                        cursor.execute(query,test_list_2)
                else:
                    query = "INSERT INTO reg_domain(domain, ip_address, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s)"
                    test_list_2 = tuple(test_list)
                    cursor.execute(query,test_list_2)
            
            else:
                query = "INSERT INTO reg_domain(domain, domain_searched, scanned_timestamp) VALUES(%s,%s,%s)"
                test_list_2 = tuple(test_list)
                cursor.execute(query,test_list_2)


        except:
            end()
    end()

def sqldb_squat(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')

    print(colored("\n[*]  Connected to SQL DB for transferring all the Domain Name Squat records",'red'))

    #close the connection to the database.
    def end():
        db.commit()
        cursor.close()
    print(colored("[*]  Done with transferring all the Domain Name Squat records",'blue'))


    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/squatting.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split('\n')

    values = []
    for line in file_content:
        new_list = line.split('  ')
        new_list = filter(None,new_list)
        new_list = [elem for elem in new_list if elem.strip()]
        values.append(tuple(new_list))

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    for each_tuple in values_2[13:-2]:
        test_list = list(each_tuple)
        try:
            if len(test_list) == 7:
                query = "INSERT INTO squat(squat_type, domain, ip, country, mx_server_domain, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                test_list_2 = tuple(test_list)
                cursor.execute(query,test_list_2)
            elif len(test_list) == 6:
                if '.' in test_list[3]:
                    query = "INSERT INTO squat(squat_type, domain, ip, mx_server_domain, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s,%s)"
                    test_list_2 = tuple(test_list)
                    cursor.execute(query,test_list_2)
                else:
                    query = "INSERT INTO squat(squat_type, domain, ip, country, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s,%s)"
                    test_list_2 = tuple(test_list)
                    cursor.execute(query,test_list_2)
            else:
                query = "INSERT INTO squat(squat_type, domain, ip, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s,%s)"
                test_list_2 = tuple(test_list)
                cursor.execute(query,test_list_2)
        except:
            end()
    end()

def sqldb_subdomains(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')

    print(colored("\n[*]  Connected to SQL DB for transferring all the subdomains data",'red'))

    #close the connection to the database.
    def end():
        db.commit()
        cursor.close()
    print(colored("[*]  Done with transferring all the subdomains records to SQL db",'blue'))

    cursor = db.cursor()

    link = "//root/data/"+domain_name+"/data/subdomains.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split('\n')

    values = []
    for line in file_content:
        new_list = line.split()
        try:
            new_list[1]
            values.append(tuple(new_list))
        except:
            new_list.append('nil')
            values.append(tuple(new_list))

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values[13:-2]:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)


    for each_tuple in values_2:
        try:
            query = "INSERT INTO subdomains(domains, IP, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s)"
            cursor.execute(query,each_tuple)    
        except:
            end()

    end()   


def sqldb_whois_data(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')

    print(colored("\n[*]  Connected to SQL DB for transferring all the who-is domain data",'red'))

    #close the connection to the database.
    def end():
        db.commit()
        cursor.close()
    print(colored("[*]  Done with transferring all the who-is domain data to SQL db",'blue'))

    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/whois-domain.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split('\n')

    values = []
    for line in file_content:
        new_list = line.split('  ')
        new_list = filter(None,new_list)
        values.append(tuple(new_list))

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values[13:-2]:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    for each_tuple in values_2:
        test_list = list(each_tuple)
        try:
            if len(test_list) == 4:
                query = "INSERT INTO whois_data(data_questions, information, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s)"
                test_list_2 = tuple(test_list)
                cursor.execute(query,test_list_2)
            else:
                query = "INSERT INTO whois_data(data_questions, domain_searched, scanned_timestamp) VALUES(%s,%s,%s)"
                test_list_2 = tuple(test_list)
                cursor.execute(query,test_list_2)
        except:
            end()
    end()

def sqldb_whois_ip(domain_name):
    domain_name = domain_name
    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))

    db = MySQLdb.connect(host='10.10.10.19',
        port=3306,
        user='root',
        password=password,
        database='discover_dump')

    print(colored("\n[*]  Connected to SQL DB for transferring all the who-is ip data",'red'))


    #close the connection to the database.
    def end():
        db.commit()
        cursor.close()
    print(colored("[*]  Done with transferring all the who-is ip data to SQL db",'blue'))

    cursor = db.cursor()
    link = "//root/data/"+domain_name+"/data/whois-ip.htm"

    soup = BeautifulSoup(open(link), "html.parser")

    soup2 = soup.text

    f = open("report.txt","w")
    f.write(str(soup2))
    f.close

    with open("report.txt") as f:
        file_content = f.read().split('\n')

    values = []
    for line in file_content:
        new_list = line.split('  ')
        new_list = filter(None,new_list)
        values.append(tuple(new_list))

    values_2 = []
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for line in values[13:-2]:
        line = list(line)
        line.append(domain_name)
        line.append(current_time)
        line = tuple(line)
        values_2.append(line)

    for each_tuple in values_2:
        test_list = list(each_tuple)
        try:
            if len(test_list) == 4:
                query = "INSERT INTO whois_ip(data_questions, information, domain_searched, scanned_timestamp) VALUES(%s,%s,%s,%s)"
                test_list_2 = tuple(test_list)
                cursor.execute(query,test_list_2)
            else:
                query = "INSERT INTO whois_ip(data_questions, domain_searched, scanned_timestamp) VALUES(%s,%s,%s)"
                test_list_2 = tuple(test_list)
                cursor.execute(query,test_list_2)
        except:
            end()
    end()




#Main program starts from here
if __name__ == '__main__':
    print("\n█ ▀ ▀ █ 　█ ▀ ▀ 　░ ▀ ░ 　█ ▀ ▀ ▄ 　▀ ▀ █ ▀ ▀ 　　 　█ ▀ ▄ ▀ █ 　█ ▀ ▀ █ 　█ ▀ ▀ ▄ 　")
    print("█ ░ ░ █ 　▀ ▀ █ 　▀ █ ▀ 　█ ░ ░ █ 　░ ░ █ ░ ░ 　　 　█ ░ ▀ ░ █ 　█ ░ ░ █ 　█ ░ ░ █ ")
    print("▀ ▀ ▀ ▀ 　▀ ▀ ▀ 　▀ ▀ ▀ 　▀ ░ ░ ▀ 　░ ░ ▀ ░ ░ 　　 　▀ ░ ░ ░ ▀ 　▀ ▀ ▀ ▀ 　▀ ░ ░ ▀ ")
    print("\n:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(colored("====[v2019.12.4]","blue"))
    time.sleep(10)
    domain_file = open('/root/Documents/domain_list.txt','r')
    domains = domain_file.read().splitlines()
    domain_list = list(filter(None, domains))
    domain_file.close()

    for domain_name in domain_list:
        os.chdir('/opt/discover')
        output = subprocess.Popen(['./discover.sh'], stdin=subprocess.PIPE)
        domain = bytes(domain_name, encoding = 'utf-8')
        output.stdin.write(domain)
        output.stdin.flush()
        output.stdin.close()
        output.wait()
        subprocess.Popen('pkill -f firefox', shell=True)
        print(colored('\n========================\nDone with scanning, now will transfer all data to databases\n=======================','blue'))
        
        sqldb_email(domain_name)
        time.sleep(5)
        sqldb_names(domain_name)
        time.sleep(5)
        sqldb_dns_records(domain_name)
        time.sleep(5)
        sqldb_dns_records_misc(domain_name)
        time.sleep(5)
        sqldb_hosts(domain_name)
        time.sleep(5)
        sqldb_reg_domain(domain_name)
        time.sleep(5)
        sqldb_squat(domain_name)
        time.sleep(5)
        sqldb_subdomains(domain_name)
        time.sleep(5)
        sqldb_whois_data(domain_name)
        time.sleep(5)
        sqldb_whois_ip(domain_name)
        time.sleep(5)



    def alert_email(subject):
        smtp_server = 'mailer.ocd.com'
        port = 25

        msg = MIMEMultipart()
        msg['From'] = 'knayak@ocd-tech.com'
        msg['Subject'] = subject
    
        body = MIMEText("**********************\
                    This is an automated message. Please don't reply to this message.\
                    ***********************    \n\n Please see the attached document!! \n\n\n\nRegards,\nosint_mon")
        msg.attach(body)

        with open('test.csv') as f:
            record = MIMEText(f.read())
            record['Content-Disposition'] = 'attachment; filename="Data.csv"'
        msg.attach(record)

        server = smtplib.SMTP(smtp_server,port)
        server.sendmail(msg['From'], ['knayak@ocd-tech.com'], msg.as_string())
        server.quit()

    password = (base64.b64decode("MjViaG9wMTIz").decode("utf-8"))
    
    mySQLconnection = mysql.connector.connect(host='10.10.10.19',
                                port = 3306,
                                database='discover_dump',
                                user='root',
                                password=password)

    today_date = datetime.datetime.now().strftime('%Y-%m-%d')

    sql_select_Query = "select * from emails e \
        where e.timestamp like '"+today_date+"%' and not exists \
        (select * from emails where email_id = e.email_id and timestamp < e.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_email_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_email_records)

    if len(new_email_records) != 0:
        subject = 'Alert!!! New Email records found'
        alert_email(subject)


    sql_select_Query = "select * from names n \
        where n.timestamp like '"+today_date+"%' and not exists \
        (select * from names where last_name = n.last_name and first_name = n.first_name and timestamp < n.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_names_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_names_records)

    if len(new_names_records) != 0:
        subject = 'Alert!!! New Name records found'
        alert_email(subject)

    sql_select_Query = "select * from dns_records d \
        where d.timestamp like '"+today_date+"%' and not exists \
        (select * from dns_records where ip = d.ip and dns_name = d.dns_name \
        and domain_searched = d.domain_searched and timestamp < d.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_dns_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_dns_records)

    if len(new_dns_records) != 0:
        subject = 'Alert!!! New DNS records found'
        alert_email(subject)


    sql_select_Query = "select * from dns_records_misc d \
        where d.timestamp like '"+today_date+"%' and not exists \
        (select * from dns_records_misc where dns_name = d.dns_name and miscellaneous = d.miscellaneous \
        and domain_searched = d.domain_searched and timestamp < d.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_dns_records_misc = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_dns_records_misc)

    if len(new_dns_records_misc) != 0:
        subject = 'Alert!!! New DNS-misc records found'
        alert_email(subject)

    sql_select_Query = "select * from hosts h \
        where h.timestamp like '"+today_date+"%' \
        and not exists (select * from hosts where Hosts_IP = h.Hosts_IP \
        and domain_searched = h.domain_searched and timestamp < h.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_hosts_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_hosts_records)

    if len(new_hosts_records) != 0:
        subject = 'Alert!!! New Host records found'
        alert_email(subject)


    sql_select_Query = "select * from reg_domain r \
        where r.timestamp like '"+today_date+"%' \
        and not exists (select * from reg_domain where domain = r.domain \
        and domain_searched = r.domain_searched and timestamp < r.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_regdomain_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_regdomain_records)

    if len(new_regdomain_records) != 0:
        subject = 'Alert!!! New Domain Registrar records found'
        alert_email(subject)

    sql_select_Query = "select * from squat s \
        where s.timestamp like '"+today_date+"%' \
        and not exists (select * from squat where domain = s.domain \
        and domain_searched = s.domain_searched and timestamp < s.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_squat_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_squat_records)

    if len(new_squat_records) != 0:
        subject = 'Alert!!! New Squat records found'
        alert_email(subject)

    sql_select_Query = "select * from subdomains s \
        where s.timestamp like '"+today_date+"%' \
        and not exists (select * from subdomains where domains = s.domains \
        and IP = s.IP and domain_searched = s.domain_searched and timestamp < s.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_subdomain_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_subdomain_records)

    if len(new_subdomain_records) != 0:
        subject = 'Alert!!! New Subdomain records found'
        alert_email(subject)

    sql_select_Query = "select * from whois_data w \
        where w.timestamp like '"+today_date+"%' \
        and not exists (select * from whois_data where information = w.information \
        and domain_searched = w.domain_searched and timestamp < w.timestamp);"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_whoisdata_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_whoisdata_records)

    if len(new_whoisdata_records) != 0:
        subject = 'Alert!!! New whois records found'
        alert_email(subject)

    sql_select_Query = "select * from whois_ip w \
        where w.timestamp like '"+today_date+"%' \
        and not exists (select * from whois_ip where information = w.information \
        and domain_searched = w.domain_searched and timestamp < w.timestamp );"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_select_Query)
    new_whoisip_records = cursor.fetchall()

    with open("test.csv","w")  as f:
        writer=csv.writer(f, delimiter=",", lineterminator="\r\n") 
        writer.writerows(new_whoisip_records)

    if len(new_whoisip_records) != 0:
        subject = 'Alert!!! New whois-ip records found'
        alert_email(subject)

    cursor.close()
