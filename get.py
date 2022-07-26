import subprocess, sys, json, datetime; 
from datetime import date
from tabulate import tabulate

account_json = subprocess.run(["aws","organizations","list-accounts"],stdout=subprocess.PIPE, text=True)
data= json.loads(account_json.stdout)

x = input('Get accounts that created in current month?(Y/N): ')

table = []

if x == 'Y':
    compareDate = date.today().replace(day=1)
    print("Current Month:", compareDate)
else:
    year = int(input('Enter Year(YYYY): '))    
    month = int(input('Enter Month(MM): '))    
    day = int(input('Enter Day(DD): '))    
    compareDate = datetime.date(year,month,day)

for i in data['Accounts']: 
    accountDate = datetime.datetime.strptime(i['JoinedTimestamp'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
    if accountDate > compareDate:
        table.append([i['Id'],i['Name'],i['Email']])

print(tabulate(table,headers=['AccountID', 'Account Name', 'Account Email'],tablefmt='simple'))
