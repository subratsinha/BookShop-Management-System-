import os
from pickle import load, dump
import datetime
import string
MFile = "Master.dat"
File1 = "Books.dat"
File2 = "Balance.dat"
File3 = "Customer.dat"
Cdate = datetime.datetime.now() # Current date and time

# Class for date
class Cast_Date:
    def __init__(self):
        self.dd = Cdate.day
        self.mm = Cdate.month
        self.yy = Cdate.year

class Master:
    # Constructor 
    def __init__(self):
        self.Cast_Code = 0      # Book code - (Like, 1, 2, 3, etc.)
        self.Cast_Name = " "    # Title of the Book
        self.Cast_Comp = " "    # Book author
        self.Cast_Price = 0     # Price per Book        
    def Check_Code(self, C_Code):
        MList = list()
        TRec = list()
        Flag = False # To check if Cast_Code is in Master.dat or not
        if os.path.isfile(MFile):
            Mobj = open(MFile, 'rb')
            try:
                while True:
                    MRec = []   # For extracting Master.dat records
                    MRec = load(Mobj)
                    if (C_Code == MRec[0]):
                        TRec = MRec                    
                    MList.append(MRec[0])                    
            except EOFError:
                pass
            for i in range(len(MList)):
                if (C_Code == MList[i]):
                    Flag = True
                    break
            Mobj.close()
        # Flag for Master data entry and TRec for Mobile data entry
        return Flag, TRec
        
    # For Master data entry
    def Master_Entry(self):
        TRec = list() # A temporary list to store master record
        print("Add Master Book");
        ch ='Y'
        while ch=='Y':
            while True:
                self.Cast_Code = int(raw_input("Book Code (1/2/3...) # "))
                Flag, TRec = self.Check_Code(self.Cast_Code)
                if (Flag == False):
                    while True:
                        self.Cast_Name = raw_input("Book Name : ")
                        if self.Cast_Name == 0 or len(self.Cast_Name) > 25:
                            print ("Book Name should not greater than 25")
                        else:
                            break
                    while True:
                        self.Cast_Comp = raw_input("Author Name : ")
                        if (self.Cast_Comp == 0 or len(self.Cast_Comp) > 25):
                            print("Author Name should not greater than 25")
                        else:
                            break
                    while True:            
                        self.Cast_Price = float(input("Individual Book price : "))
                        if (self.Cast_Price <= 0):
                            print("Enter valid price for Book")
                        else:
                            break;
                    with open(MFile, 'ab+') as Mobj:
                        if not Mobj:
                            print (MFile, "does not created")
                        else:
                            # Appends data into a sequnce object
                            MList = list()
                            MList.append(self.Cast_Code)
                            MList.append(self.Cast_Name)
                            MList.append(self.Cast_Comp)
                            MList.append(self.Cast_Price)
                            # Write data into binary file
                            dump(MList, Mobj)
                else:
                    print ("Code", self.Cast_Code, "is already in 'Master.dat' file")
                ch = raw_input("Add new Book code? <Y/N>: ")
                ch = ch.upper()
                if ch=='Y':
                    continue
                else:
                    break                        
    def Master_Display(self):
        if not os.path.isfile(MFile):
            print (MFile, "file does not exist")
        else:
            Mobj = open(MFile, 'rb')
            print ("\n Book Master Report")
            print ("=" * 25)            
            print ("{0:<7} {1:<30} {2:<20} {3:>8}".format(" Code", "Book Name", "Author Name", "Price"))
            print ("-" * 70)
            try:
                while True:
                    MRec = []
                    MRec = load(Mobj)
                    print ("{0:<7} {1:<30} {2:<20} {3:>8.2f}"
                           .format(' '+str(MRec[0]), MRec[1], MRec[2], MRec[3]))
            except EOFError:
                pass                
            print ("-" * 70)
            Mobj.close()       

        
class Books:
    # Constructor 
    def __init__(self):
        self.Cast_Code = 0      # Book code - (Like, 1, 2, 3, etc.)
        self.Tot_Cast = 0       # Total Book purchased
        self.dd = self.mm = self.yy = 0 # Book purchase date
    # For Books entry into the Books.dat data file
    def New_Books(self):
        M = Master()
        B = Balance()
        CDt = Cast_Date()
        self.dd = CDt.dd
        self.mm = CDt.mm
        self.yy = CDt.yy
        print("Add New Stock Book");        
        ch ='Y'
        while ch=='Y':
            TRec = list() # A temporary list to store master record
            Flag = False # To check if Cast_Code is in Master.dat or not
            print("Date: %s-%s-%s" % (CDt.dd, CDt.mm, CDt.yy))
            while True:
                self.Cast_Code = int(input("Book Code (1/2/3/...) # "))
                # Function call to check Book code in Master.dat
                Flag, TRec = M.Check_Code(self.Cast_Code)
                if (Flag == True):
                    self.Cast_Name = TRec[1]    # Title of the Book
                    self.Cast_Comp = TRec[2]    # Book author
                    self.Cast_Price = TRec[3]   # Price per Book
                    print("Book Name :", self.Cast_Name)
                    print("Author Name : ", self.Cast_Comp)
                    print("Individual Book price : ",self.Cast_Price)
                    while True:
                        self.Tot_Cast = int(input("Enter new stock Book purchased (Stock): "))
                        if (self.Tot_Cast <= 0):
                            print("Enter valid Book number");
                        else:
                            break
                    ch = raw_input("Do you want to save the record <Y/N>: ")
                    if ch == 'Y':
                        CList = list()
                        with open (File1,'ab+') as Cobj:
                            if not Cobj:
                                print (File1, "does not created")
                            else:
                                # Appends data into a sequnce object                                
                                CList.append(self.Cast_Code)
                                CList.append(self.Tot_Cast)
                                CList.append(self.dd)
                                CList.append(self.mm)
                                CList.append(self.yy)
                            # Write data into binary file
                            dump(CList, Cobj)
                            #B.Add_to_File(self.Cast_Code, self.Tot_Cast, self.Cast_Price, self.dd, self.mm, self.yy)
                            B.AddUpdateBalance(CList, self.Cast_Price)
                            print("Record saved")                
                    ch = raw_input("Stock more Book record? <Y/N>: ")
                    ch = ch.upper()
                    if ch=='N':
                        break
                    else:
                        break
    # For Books entry into the Books.dat data file
    def Display_Books(self):
        M = Master()
        if not os.path.isfile(File1):
            print (File1, "file does not exist")
        else:
            Cobj = open(File1, 'rb')
            print ("\n Book entry Register")
            print ("=" * 26)
            print ("{0:>5} {1:<25} {2:<20} {3:>10} {4:>8} {5:<12}"
                   .format("Code", "Name", "Author Name", "Quantity", "Price", "Date"))
            print ("-" * 85)
            try:
                while True:
                    CRec = []
                    CRec = load(Cobj)
                    TRec = list()
                    Flag, TRec = M.Check_Code(CRec[0])
                    nDt = Set_DateFormat(CRec[2], CRec[3], CRec[4])
                    if (Flag == True):
                        print ("{0:>5} {1:<25} {2:<20} {3:>10} {4:>8.2f} {5:<12}"
                               .format(CRec[0], TRec[1], TRec[2], CRec[1], TRec[3], nDt))
            except EOFError:
                pass                
            print ("-" * 85)
            Cobj.close()

# Function to set the date as: DD-MM-YYYY            
def Set_DateFormat(d1, m1, y1):
    fDt = ''
    d11 = str(d1)
    m11 = str(m1)
    y11 = str(y1)
    if (len(d11)==1):
        d11 = '0'+d11
    if (len(m11)==1):
        m11 = '0'+m11
    fDt = d11+'-'+m11+'-'+y11
    return fDt
                
class Balance:
    def __init__(self):
        # Instance attributes of Balance.dat data file
        self.Cast_Code = 0	        # Book code to be balance
        self.Cast_Bal = 0	        # Total number of Books in balance
        self.Cast_Price = 0             # Unit price of Books on code wise
        self.dd = self.mm = self.yy = 0 # Balance date
    def Give_Balance(self, C_Code):
        Tbalance = 0
        if not os.path.isfile(File2):
            # When file does not exit
            return False
        else:
            Brec = list()   # A list to extract record from Balance.dat
            Tbalance = 0
            Bobj = open(File2, 'rb')
            try:
                while True:
                    BRec = load(Bobj)
                    if (C_Code == BRec[0]):
                        Tbalance = BRec[1] # E.g. Cast_Bal
                        break;
            except EOFError:
                pass                    
            Bobj.close()
            return Tbalance
    def AddUpdateBalance(self, CList, CPrice):
        # To know the balance Book in 'Balance.dat'
        Cbalance = Balance.Give_Balance(self, CList[0])
        if (Cbalance == False): # If file does not exist, add the record for first time
            BRec = list()
            with open(File2, 'ab') as Bobj:
                BRec.append(CList[0])   # Cast_Code
                BRec.append(CList[1])   # Cast_Bal
                BRec.append(CPrice)   # Cast_Price
                BRec.append(CList[2])   # Day
                BRec.append(CList[3])   # Month
                BRec.append(CList[4])   # Year
                dump(BRec, Bobj)
        elif (Cbalance >= 0):
            Bobj = open(File2, 'rb')
            Tobj = open("Temp.dat", 'wb')            
            try:
                while True:
                    BRec = list()   # A list to extract record from Balance.dat
                    BRec = load(Bobj)
                    if (CList[0] != BRec[0]):
                        # Write data into Temp.dat file
                        dump(BRec, Tobj)
                    else:
                        BRec[1] = Cbalance + CList[1]
                        #self.Cast_Bal = self.Cast_Bal + Cbalance
                        dump(BRec, Tobj)
            except EOFError:
                pass                
            Tobj.close()
            Bobj.close()
            os.remove("Balance.dat")
            os.rename("Temp.dat", "Balance.dat")

    def UpdateBalance(self, CList):
        Bobj = open(File2, 'rb')
        Tobj = open("Temp.dat", 'wb')            
        try:
            while True:
                BRec = list()   # A list to extract record from Balance.dat
                BRec = load(Bobj)
                if (CList[0] != BRec[0]):
                    # Write data into Temp.dat file
                    dump(BRec, Tobj)
                else:
                    BRec[1] = BRec[1] - CList[4]
                    dump(BRec, Tobj)
        except EOFError:
            pass                
        Tobj.close()
        Bobj.close()
        os.remove("Balance.dat")
        os.rename("Temp.dat", "Balance.dat")
        print('Balance.dat updated')

    def Balance_Books(self):
        M = Master()
        if not os.path.isfile(File2):
            print (File2, "file does not exist")
        else:
            TAmount = 0
            print ("\n Balance Stock Register (Book)")
            print ("=" * 35)
            Bobj = open(File2, 'rb')
            print ("{0:>5} {1:<26} {2:<20} {3:>10} {4:>8} {5:>10}"
                   .format("Code", "Name", "Author Name", "Quantity", "Price", "Amount"))
            print ("-" * 86)
            try:
                while True:
                    BRec = []
                    BRec = load(Bobj)
                    TRec = list()
                    Flag, TRec = M.Check_Code(BRec[0])
                    if (Flag == True):
                        Amount = BRec[1] * BRec[2]
                        TAmount = TAmount + Amount
                        print ("{0:>5} {1:<26} {2:<20} {3:>10} {4:>8.2f} {5:>10.2f}"
                               .format(BRec[0], TRec[1], TRec[2], BRec[1], BRec[2], Amount))
            except EOFError:
                pass
            print ("-" * 86)
            print ("%s Total Amount: %s %.2f" % (' ' * 56, ' ' * 4, TAmount))
            Bobj.close()

class Customer:
    def __init__(self):
        # Instance attributes of Customer.dat data file
        self.Cast_Code = 0  # Book code
        self.C_Name = ''    # Customer name
        self.C_Address = '' # Customer address
        self.C_MPhone = 0   # Customer mobile no.
        self.No_Of_Cast = 0      # Number of Book
        self.dd = self.mm = self.yy = 0 # Sale date
    def Book_Sale(self):
        M = Master()
        B = Balance()
        CDt = Cast_Date()
        self.dd = CDt.dd
        self.mm = CDt.mm
        self.yy = CDt.yy
        Cbalance = 0
        print("Customer sales Book");        
        ch ='Y'
        while ch=='Y':
            TRec = list() # A temporary list to store master record
            Flag = False # To check if Cast_Code is in Master.dat or not
            print("Date: %s-%s-%s" % (CDt.dd, CDt.mm, CDt.yy))
            while True:
                self.Cast_Code = int(raw_input("Book Code (1/2/3/...) # "))
                # Function call to check Book code in Master.dat
                Flag, TRec = M.Check_Code(self.Cast_Code)
                Cbalance = B.Give_Balance(self.Cast_Code)
                if (Flag == True):
                    self.Cast_Name = TRec[1]    # Title of the Book
                    self.Cast_Comp = TRec[2]    # Book author
                    self.Cast_Price = TRec[3]   # Price per Book
                    print("Book Name :", self.Cast_Name)
                    print("Author Name : ", self.Cast_Comp)
                    print("Individual Book price : ",self.Cast_Price)
                    print('\n Enter Customer details')
                    self.C_Name = raw_input("Customer name: ").upper()
                    self.C_Address = raw_input("Customer addres: ")
                    self.C_MPhone = int(raw_input("Customer mobile no.: "))
                    while True:
                        self.No_Of_Cast = int(raw_input("Enter sales Books nos.: "))
                        if (self.No_Of_Cast > Cbalance):
                            print("Out of Stock");
                        else:
                            break
                        
                    ch = raw_input("Sales confirm <Y/N>: ").upper()
                    if ch == 'Y':
                        CustList = list()
                        with open(File3, 'ab') as CustObj:
                            if not CustObj:
                                print (File3, "does not created")
                            else:
                                # Appends data into a sequnce object
                                CustList.append(self.Cast_Code)
                                CustList.append(self.C_Name)
                                CustList.append(self.C_Address)
                                CustList.append(self.C_MPhone)
                                CustList.append(self.No_Of_Cast)
                                CustList.append(self.dd)
                                CustList.append(self.mm)
                                CustList.append(self.yy)
                                B.UpdateBalance(CustList)                                
                                dump(CustList, CustObj)                                
                    ch = raw_input("More sale? <Y/N>: ")
                    ch = ch.upper()
                    if ch!='Y':
                        break
    # Function to search individual customer on mobile no.
    def Return_CustomerName(self, Mno):
        M = Master()
        CName = ''
        if not os.path.isfile(File2):
            print (File3, "file does not exist")
        else:
            CustObj = open(File3, 'rb')
            try:
                while True:
                    CustRec = []
                    CustRec = load(CustObj)
                    if Mno == CustRec[3]:
                        CName = CustRec[1]
                        break
            except EOFError:    
                pass
            CustObj.close()
        return CName               

    # Function to display Sales report for a particular month in a calender year.
    def MonthlySales_Report(self):
        M = Master()
        if not os.path.isfile(File2):
            print (File3, "file does not exist")
        else:
            monthNo = int(input('Enter month no.: '))
            yearNo = int(input('Enter year: '))
            CDt = Cast_Date()
            self.dd = CDt.dd
            self.mm = CDt.mm
            self.yy = CDt.yy
            if (monthNo <= 12 and monthNo <= self.mm and yearNo <= self.yy):
                # Function call for a character month
                MonthName = Month_Name(monthNo)
                TAmount = 0
                # Function called to set the date as DD-MM-YYYY
                nDt = Set_DateFormat(self.dd, self.mm, self.yy)
                print ("\n Customer Sales Status Report - Date:", nDt)
                print ("For the month of", MonthName, yearNo)
                print ("=" * 27)
                CustObj = open(File3, 'rb')
                print ("{0:<20} {1:<12} {2:<25} {3:^10} {4:>5} {5:>12} {6:>8}"
                       .format("Name", "Mobile No.", "Book Code & Name", "Date", "Qty", "Unit Price", "Amount"))
                print ("-" * 100)
                try:
                    while True:
                        CustRec = []
                        CustRec = load(CustObj)
                        TRec = list()
                        Flag, TRec = M.Check_Code(CustRec[0])
                        UPrice = TRec[3]
                        Amount = (UPrice + (UPrice * 0.20)) * CustRec[4] # An additional 20% of Unit price
                        nDt = Set_DateFormat(CustRec[5], CustRec[6], CustRec[7])
                        if (monthNo == CustRec[6] and yearNo == CustRec[7]):
                            Clength = str(CustRec[0])+'-'+TRec[1]
                            nName = ''
                            for i in range(len(Clength)):  # Extracts only 24 characters
                                nName = nName + Clength[i]
                                if i == 23:
                                    break                                
                            print ("{0:20} {1:<12} {2:<25} {3:>10} {4:>5.0f} {5:>12.2f} {6:>8.2f}"
                                   .format(CustRec[1], CustRec[3], nName, nDt, CustRec[4], UPrice, Amount))
                except EOFError:    
                    pass
                print ("-" * 100)
                print('Note. Amount is calculated as 20% extra on unit price.')
                #print ("%s Total Amount: %s %.2f" % (' ' * 50, ' ' * 4, TAmount))
                CustObj.close()
            else:
                print ("Month no. and year is not valid")

    # Function to display cose wise monthly sales report.
    def CodeWiseMonthlySales_Report(self):
        M = Master()
        TRec = list() # A temporary list to store master record
        Flag = False # To check if Cast_Code is in Master.dat or not
        if not os.path.isfile(File2):
            print (File3, "file does not exist")
        else:
            CCode = int(input("Book Code (1/2/3/...) # "))
            monthNo = int(input('Enter month no.: '))
            yearNo = int(input('Enter year: '))
            CDt = Cast_Date()
            self.dd = CDt.dd
            self.mm = CDt.mm
            self.yy = CDt.yy
            # Function call to check Book code in Master.dat
            Flag, TRec = M.Check_Code(CCode)                
            if (monthNo <= 12 and monthNo <= self.mm and yearNo <= self.yy and Flag == True):                
                CName = TRec[1]    # Title of the Book
                CComp = TRec[2]    # Book author
                CPrice = TRec[3]   # Price per Book
                # Function call for a character month
                MonthName = Month_Name(monthNo)
                TAmount = 0
                # Function called to set the date as DD-MM-YYYY
                nDt = Set_DateFormat(self.dd, self.mm, self.yy)
                print ("\n Code wise Sales Report - Date:", nDt)
                print ("For the month of", MonthName, yearNo)
                print ("Book Code: %d Name: %s" % (CCode, CName))
                print ("=" * 40)
                CustObj = open(File3, 'rb')
                print ("{0:<20} {1:<12} {2:^10} {3:>5} {4:>12} {5:>8}"
                       .format("Customer Name", "Mobile No.", "Date", "Qty", "Unit Price", "Amount"))
                print ("-" * 74)
                ctr = 0
                try:
                    while True:
                        CustRec = []
                        CustRec = load(CustObj)
                        TRec = list()
                        Flag, TRec = M.Check_Code(CustRec[0])
                        UPrice = TRec[3]
                        Amount = (UPrice + (UPrice * 0.20)) * CustRec[4] # An additional 20% of Unit price
                        nDt = Set_DateFormat(CustRec[5], CustRec[6], CustRec[7])
                        if (monthNo == CustRec[6] and yearNo == CustRec[7] and CCode == CustRec[0]):
                            ctr += 1
                            print ("{0:20} {1:<12} {2:>10} {3:>5.0f} {4:>12.2f} {5:>8.2f}"
                                   .format(CustRec[1], CustRec[3], nDt, CustRec[4], UPrice, Amount))
                except EOFError:    
                    pass
                print ("-" * 74)
                if (ctr == 0):
                    print('No record found on such Code No., Month and Year')
                else:
                    print('Note. Amount is calculated as 20% extra on unit price.')
                #print ("%s Total Amount: %s %.2f" % (' ' * 50, ' ' * 4, TAmount))
                CustObj.close()
            else:
                print ("Either Code not found or Month no. and year is not valid")


    # Function to search individual customer on mobile no.
    def CustomerWithMobileSearch(self):
        M = Master()
        if not os.path.isfile(File2):
            print (File3, "file does not exist")
        else:
            MobileNo = int(input('\nEnter customer mobile no.: '))
            Cust_Name = self.Return_CustomerName(MobileNo)
            TAmount = 0
            CDt = Cast_Date()
            self.dd = CDt.dd
            self.mm = CDt.mm
            self.yy = CDt.yy
            # Function called to set the date as DD-MM-YYYY
            nDt = Set_DateFormat(self.dd, self.mm, self.yy)
            print ("\nDate:", nDt)
            print ("Customer name:", Cust_Name, '& Mobile No.:', MobileNo)
            print ("=" * 40)
            CustObj = open(File3, 'rb')
            print ("{0:<30} {1:^10} {2:>5} {3:>12} {4:>8}"
                   .format("Book", "Date", "Qty", "Unit Price", "Amount"))
            print ("-" * 70)
            ctr = 0        
            try:
                while True:
                    CustRec = []
                    CustRec = load(CustObj)
                    TRec = list()
                    Flag, TRec = M.Check_Code(CustRec[0])
                    UPrice = TRec[3]
                    Amount = (UPrice + (UPrice * 0.20)) * CustRec[4] # An additional 20% of Unit price
                    nDt = Set_DateFormat(CustRec[5], CustRec[6], CustRec[7])
                    if (MobileNo == CustRec[3]):
                        ctr += 1
                        Clength = str(CustRec[0])+'-'+TRec[1]
                        nName = ''
                        for i in range(len(Clength)):  # Extracts only 24 characters
                            nName = nName + Clength[i]
                            if i == 23:
                                break
                        print ("{0:<30} {1:>10} {2:>5.0f} {3:>12.2f} {4:>8.2f}"
                               .format(nName, nDt, CustRec[4], UPrice, Amount))
            except EOFError:    
                pass
            print ("-" * 70)
            if (ctr == 0):
                print('No record found on such mobile no.')
            else:
                print('Note. Amount is calculated as 20% extra on unit price.')
            #print ("%s Total Amount: %s %.2f" % (' ' * 50, ' ' * 4, TAmount))
            CustObj.close()
                
# Function to find a character month on against a month no.
def Month_Name(mNo):
    mDict = {1:'January', 2:'February', 3:'March',
             4:'April', 5:'May', 6:'June', 7:'July',
             8:'August', 9:'September', 10:'October',
             11:'November', 12:'December'}
    mName = ''
    for key, value in mDict.items():
        if (key == mNo):
            mName = value
            break
    return mName
                    
def main():
    opt = ''
    M = Master()
    CS = Books()
    BL = Balance()
    Cust = Customer()
    while True:
        print ("\n Book Gallery Main Menu")
        print ("-" * 30)
        print ("| 1 - > Master Books |")
        print ("| 2 - > Stock Books  |")
        print ("| 3 - > Customer Sales       |")
        print ("| 4 - > Exit                 |")
        print ("-" * 30)
        opt=int(raw_input("Enter your choice: "))
        if opt == 1:
            ch = ''
            while True:
                print ("\n\tMaster Book Menu")
                print ("-" * 35)
                print ("| 1 - > New Book Entry |")
                print ("| 2 - > View Books        |")
                print ("| 3 - > Exit                      |")
                print ("-" * 35)
                ch=int(raw_input("Enter your choice: "))
                if ch == 1:
                    M.Master_Entry()
                elif ch == 2:
                    M.Master_Display()                    
                elif ch == 3:
                    break
                else:
                    print ("Wrong choice")
                    continue
        elif opt == 2:
            while True:
                print ("\n\tStock Book Menu")
                print ("-" * 33)
                print ("| 1 - > Books Stock entry |")
                print ("| 2 - > Display Books     |")
                print ("| 3 - > Stock/Balance Books |")
                print ("| 4 - > Exit                    |")
                print ("-" * 33)
                ch=int(raw_input("Enter your choice: "))
                if ch == 1:
                    CS.New_Books()
                elif ch == 2:
                    CS.Display_Books()
                elif ch == 3:
                    BL.Balance_Books()
                elif ch == 4:
                    break
                else:
                    print ("Wrong Choice")
                    continue
        elif opt == 3:
            while True:
                print ("\n\tCustomer Sales Menu")
                print ("-" * 34)
                print ("| 1 - > Sales Entry              |")
                print ("| 2 - > Monthly Sales Report     |")
                print ("| 3 - > Code Wise Monthly Sales  |")
                print ("| 4 - > Customer Mobile No. Wise |")
                print ("| 5 - > Exit                     |")
                print ("-" * 34)
                ch=int(raw_input("Enter your choice: "))
                if ch == 1:
                    Cust.Book_Sale()
                elif ch == 2:
                    Cust.MonthlySales_Report()
                elif ch == 3:
                    Cust.CodeWiseMonthlySales_Report()
                elif ch == 4:
                    Cust.CustomerWithMobileSearch()
                elif ch == 5:
                    break
                else:
                    print ("Wrong Choice")
                    continue
        elif opt == 4:
            break
        else:
            print ("Wrong input")
            continue
if __name__ == "__main__":
    main()
