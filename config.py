
import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler



ip = '10.10.10.2'


device_type = 'arista_eos'


username = 'admin'
password = 'python'


command = 'show running'



session = ConnectHandler(device_type = device_type, ip = ip, username = username, password = password, global_delay_factor = 3)

enable = session.enable()


output = session.send_command(command)


device_cfg_old = 'cfgfiles/' + ip + '_' + (datetime.date.today() - datetime.timedelta(days = 1)).isoformat()


with open('cfgfiles/' + ip + '_' + datetime.date.today().isoformat(), 'w') as device_cfg_new:
    device_cfg_new.write(output + '\n')



with open(device_cfg_old, 'r') as old_file, open('cfgfiles/' + ip + '_' + datetime.date.today().isoformat(), 'r') as new_file:
    difference = difflib.HtmlDiff().make_file(fromlines = old_file.readlines(), tolines = new_file.readlines(), fromdesc = 'Yesterday', todesc = 'Today')

    

fromaddr = 'networkcatproject3@gmail.com'
toaddr = 'networkcatproject3@gmail.com'


msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Daily Configuration Management Report'
msg.attach(MIMEText(difference, 'html'))


server = smtplib.SMTP('smtp.gmail.com', 587)


server.starttls()


server.login('networkcatproject3@gmail.com', 'python3.7')
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()


