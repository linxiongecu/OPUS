import imaplib, email, os, glob
# gmail cannot login with username and password using  scirpt is not allowed
# using google takeout to export your emails.

# https://stackoverflow.com/questions/70188644/gmail-login-error-with-the-help-of-imaplib-in-python
e_path="C:/Users/lxiong/UMD/GPS/email"

#Input email address and password.
EMAIL  = "xxx@gmail.com"
PWD    = "xxxx"

#SMTP_SERVER = "imap.126.com"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993
#Emails that contain GPS data information
EmailContent="gods"
def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
        mail.login(EMAIL,PWD)
        mail.select('inbox')
        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        #first_email_id = int(id_list[-120])
        latest_email_id = int(id_list[-1])
        print ("First email: {}; Last email: {}".format(first_email_id ,latest_email_id ))
        count = 0
        for i in range(latest_email_id,first_email_id, -1):
            type, data = mail.fetch(str(i), '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    if EmailContent  in email_subject:
                      count=count+1
                      print ("Number of email: ", count)
                      print ('Subject : ' + email_subject + '  From : ' + email_from + '\n')
                      current_directory = os.getcwd()
                      final_directory = os.path.join(current_directory, r'Emails')
                      if not os.path.exists(final_directory):
                          os.makedirs(final_directory)
                      print ("Work directory: " + os.getcwd())
                      save_string=str("OPUSemail_%03d.txt" %(count))
                      with open(os.path.join(final_directory, save_string), 'w') as outfile:
                          outfile.write(str(msg))
                          outfile.close()
    except Exception as e:
        print (str(e))

current_directory = os.getcwd()
final_directory = e_path
os.makedirs(final_directory, exist_ok=True)
os.chdir(final_directory )
for file in glob.glob("OPUS*txt"):
     os.remove(file)
os.chdir(current_directory)
read_email_from_gmail()
os.chdir(final_directory)
print ("Name,Date, Start, End,  NAD83_X, NAD83_Y, NAD83_Z, UTM_East, UTM_North, Ortho,EL,OBS_USED, RMS")
filesave = open("GPS.txt", "w")
filesave.write("Name,Date,Start,End,NAD83_X,NAD83_Y,NAD83_Z,UTM_East,UTM_North,,Ortho,EL,OBS_USED,RMS\n")
for file in glob.glob("OPUS*txt"):
    # Read email files
    file1 = open(file, 'r')
    Lines = file1.readlines()
    for line in Lines:
        # Extract information line by line.
        if  'RINEX FILE' in line:
             Name = line.split()[2]
        if  'SOFTWARE' in line:
             Date = line.split()[6]
             Start = line.split()[7]
        if "EPHEMERIS" in line:
             End = line.split()[5]
        if "OBS USED" in line:
            OBS_USED = line.split()[9]
        if "ARP HEIGHT" in line:
             RMS = line.split()[5].replace("(m)","")
        if "X:" in line:
            NAD83_X = line.split()[1].replace("(m)", "")
        if "Y:" in line:
            NAD83_Y = line.split()[1].replace("(m)", "")
        if "Z:" in line:
            NAD83_Z = line.split()[1].replace("(m)", "")
        if "EL HGT:" in line:
            EL = line.split()[2].replace("(m)", "")
        if "ORTHO HGT:" in line:
            Ortho = line.split()[2].replace("(m)", "")
        if "Northing" in line:
            UTM_North = line.split()[3]
        if "Easting" in line:
            UTM_East = line.split()[3]
    print (Name,Date, Start, End,  NAD83_X, NAD83_Y, NAD83_Z, UTM_East, UTM_North, Ortho,EL,  OBS_USED, RMS)
    filesave.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(Name,Date, Start, End,  NAD83_X, NAD83_Y, NAD83_Z, UTM_East, UTM_North, Ortho, EL, OBS_USED, RMS))
filesave.close()
