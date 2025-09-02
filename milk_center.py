
from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from datetime import datetime
#database------------------------------->
class milkdatabase:
    def __init__(self,db):
        self.con=sqlite3.connect(db)
        self.c=self.con.cursor()
        self.c.execute("""
             CREATE TABLE IF NOT EXISTS mdata(
                pid INTEGER PRIMARY KEY,
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                village TEXT NOT NULL 
                 
             )          
                       
                       """)
        
        self.c.execute("""
                CREATE TABLE IF NOT EXISTS rdata(
                    p INTEGER PRIMARY KEY,
                    id INTEGER NOT NULL,
                    milktype TEXT NOT NULL,
                    fatmin  REAL NOT NULL,
                    fatmax REAL NOT NULL,
                    rate INTEGER NOT NULL   
                      
                                )        
                       
                        """)
        self.con.commit()
        self.con.commit()
        
        self.c.execute("""
                  CREATE TABLE IF NOT EXISTS collnew(

                   id INTEGER PRIMARY KEY,
                   date INTEGER NOT NULL,
                   farmer TEXT NOT NULL,
                   milktype TEXT NOT NULL,
                   liter REAL NOT NULL,
                   snf REAL NOT NULL,
                   fat REAL NOT NULL,
                   rate REAL NOT NULL,
                   amount REAL NOT NULL     
                      
                  )         
                           
                           """)
        
        
    def insert(self,id,name,phone,village):
        sql="""
        INSERT INTO mdata VALUES(NULL,?,?,?,?)
        """
        self.c.execute(sql,(id,name,phone,village))
        self.con.commit() 
    def fetch(self):
        return self.c.execute("SELECT * FROM mdata")
    def update(self,id,name,phone,village,pid):
        sql="""
        UPDATE mdata SET  id=?, name=?,phone=?,village=? WHERE Pid=?
        """
        self.c.execute(sql,(id,name,phone,village,pid))
        self.con.commit()
        
    def delete(self,pid):
        sql="""
        DELETE FROM mdata WHERE pid=?
        """
        self.c.execute(sql,(pid,))
        self.con.commit()
    def search(self,keyword):
        sql="""
        SELECT * FROM mdata WHERE name LIKE ? OR phone LIKE ? OR village LIKE ?
        """ 
        param=('%'+ keyword +'%','%'+ keyword +'%','%'+ keyword +'%')
        self.c.execute(sql,(param))
        return self.c.fetchall()
    
    def inserted(self,id,milktype,fatmin,fatmax,rate):
        sql="""
        INSERT INTO rdata VALUES(NULL,?,?,?,?,?) 
        """
        self.c.execute(sql,(id,milktype,fatmin,fatmax,rate))
        self.con.commit()
    def fetch_rate(self):
        self.c.execute("SELECT * FROM rdata") 
        return self.c.fetchall() 
    def update1(self,id,milktype,fatmin,fatmax,rate,pid):
        sql="UPDATE rdata SET id=?, milktype=?,fatmin=?,fatmax=?,rate=? WHERE pid=?"
        self.c.execute(sql,(id,milktype,fatmin,fatmax,rate,pid))
        self.con.commit()
    def delete_db1(self,pid):
        sql="""
        DELETE FROM rdata WHERE pid=?
        """
        self.c.execute(sql,(pid,))
        self.con.commit()
    def insert2(self,data,farmer,milktype,liter,snf,fat,rate,amount):
        sql="""
        INSERT INTO  collnew VALUES(NULL,?,?,?,?,?,?,?,?)
        """
        self.c.execute(sql,(data,farmer,milktype,liter,snf,fat,rate,amount))
        self.con.commit() 
    def fetch_colletion(self):
        self.c.execute("SELECT * FROM collnew ") 
        return self.c.fetchall()
    def filter(self,keyword,fromdate,todate):
        sql = """
        SELECT * FROM collnew
        WHERE farmer LIKE ? AND date BETWEEN ? AND ?
        """
        params=('%'+ keyword + '%', fromdate, todate)
     # Correct
        self.c.execute(sql,params)

        return self.c.fetchall() 
    def day_summery(self,keyword):
        sql="""
        SELECT * FROM collnew WHERE date LIKE ? 
        """ 
        param=('%'+ keyword +'%',)
        self.c.execute(sql,(param))
        return self.c.fetchall() 
#---------------------END-----------------------------------<      
          
  
#-----------------------Add New farmer----------------------->        
       
def add_datas():
    if ename.get()!="" and ephone.get()!="" and evilage.get()!="":
        val=len(mytree.get_children())+1
        
        mytree.insert("",index="end",values=(val,ename.get(),ephone.get(),evilage.get()))
        add_database=milkdatabase("milkdatabasenew.db")
        add_database.insert(val,ename.get(),ephone.get(),evilage.get())
        ename.delete(0,END)
        ephone.delete(0,END)
        evilage.delete(0,END)
    else:
        messagebox.showerror("msg","fill all feailts")    
        

   
       
def update():
    index=mytree.focus()
    id=mytree.focus()[3]
    mytree.item(index,values=(id,ename.get(),ephone.get(),evilage.get()))
    add_database=milkdatabase("milkdatabasenew.db")
    add_database.update(id,ename.get(),ephone.get(),evilage.get(),id)


    
    
def show(event):      
    datainser=mytree.focus()
    values=mytree.item(datainser,"values")
  
    ename.insert(0,values[1])
    ephone.insert(0,values[2])
    evilage.insert(0,values[3])
def delete_db():
    delid=mytree.focus()
   
    dsid=mytree.selection()
    for i in dsid:
        pid_str = mytree.set(i, '#1')
        pid=int(pid_str)
    add_database=milkdatabase("milkdatabasenew.db")
    add_database.delete(pid)
    mytree.delete(i)   
def go():
    
    searchval=esearch.get()
    add_database=milkdatabase("milkdatabasenew.db")
    result=add_database.search(searchval)
    if searchval!="":
        for item in mytree.get_children():
            mytree.delete(item)
        for i in  result:
            pid, id, name, phone, village = i
            mytree.insert("", index="end",iid=str(pid), values=( id, name, phone, village))
    
    else:
        messagebox.showerror("msg","search box is empty")

#---------------------------END--------------------------------<

#-------------------------------RATE PAGE---------------------------->         
         
def rates():
    top=Toplevel(krish)
    top.geometry("1366x768")
    krish.title("Milk Center")
                      

    menuframe=Frame(top,bg="Powder Blue",width=1366,height=40)
    menuframe.grid(row=0,column=0,sticky="nw")
    menuframe.grid_propagate(False)
    farmerdetails=Frame(top,bg="#caf0f8",width=1366,height=100)
    farmerdetails.grid(row=1,column=0,sticky="nw")
    farmerdetails.grid_propagate(False)
                
    def add_datas1():
        if ecom.get()!="" and efatmin.get()!="" and efatmax.get() !="" and erate.get():
                       
            val=len(mytree.get_children())+1
            mytree.insert("","end",values=(val,ecom.get(),efatmin.get(),efatmax.get(),erate.get()))
            ratedata=milkdatabase("milkdatabasenew.db") 
            ratedata.inserted(val,ecom.get(),efatmin.get(),efatmax.get(),erate.get())
        else:
            messagebox.showerror("msg","all feailts")    
        
    
       
    def show(event):
        ecom.delete(0,END)
        efatmin.delete(0,END)       
        efatmax.delete(0,END)       
        erate.delete(0,END)       
        id=mytree.focus()
        value=mytree.item(id,"values")
        ecom.insert(0,value[1])
        efatmin.insert(0,value[2])       
        efatmax.insert(0,value[3])       
        erate.insert(0,value[4])
        
    def update1():
        inval=mytree.focus()
        id=mytree.focus()[0]
            # messagebox.showinfo(id)
        mytree.item(inval,values=(id,ecom.get(),efatmin.get(),efatmax.get(),erate.get()))
        datas.update(id,ecom.get(),efatmin.get(),efatmax.get(),erate.get(),id)
           
    def delete_db2():
        datas=milkdatabase("milkdatabasenew.db")
        select=mytree.focus()
        items=mytree.item(select,"values")
        valu=items[0]
        datas.delete_db1(valu)
        mytree.delete(valu)
     

    btnfarmers=Button(menuframe,bg="#A4A9AD",text="Farmer",font=("times",15),activebackground="Powder Blue",width=10)
    btnfarmers.grid(row=0,column=0)

    btnrate=Button(menuframe,bg="#A4A9AD",text="Rate",font=("times",15),activebackground="Powder Blue",width=10,command=rates)
    btnrate.grid(row=0,column=1,)

    btncollction=Button(menuframe,bg="#A4A9AD",text="Collection",font=("times",15),activebackground="Powder Blue",width=10)
    btncollction.grid(row=0,column=2)

    btnreport=Button(menuframe,bg="#A4A9AD",text="Report",font=("times",15),activebackground="Powder Blue",width=10)
    btnreport.grid(row=0,column=3) 
        
        


    lmtype=Label(farmerdetails,text="Milk type",font=("times",15,"bold"),bg="#caf0f8")
    lmtype.grid(row=1,column=0,pady=10,padx=10)
    ecom=ttk.Combobox(farmerdetails,font=("times",15,"bold"),values=["Cow","Buffalo"])
    ecom.set("Cow")
    ecom.grid(row=1,column=1,pady=10,padx=10)
        
    lfatmin=Label(farmerdetails,text="Fat min",font=("times",15,"bold"),bg="#caf0f8")
    lfatmin.grid(row=1,column=2,pady=15,padx=10)
        
    efatmin=Entry(farmerdetails,width=10,font=("times",10,"bold"))
    efatmin.grid(row=1,column=3,pady=15,padx=10)

        
        
    lfatmax=Label(farmerdetails,text="Fat max",font=("times",15,"bold"),bg="#caf0f8")
    lfatmax.grid(row=1,column=4,pady=15,padx=10)
        
    efatmax=Entry(farmerdetails,width=10,font=("times",10,"bold"))
    efatmax.grid(row=1,column=5,pady=15,padx=10)
    lrate=Label(farmerdetails,text="Rate",font=("times",15,"bold"),bg="#caf0f8")
    lrate.grid(row=1,column=6,pady=15,padx=10)
        
    erate=Entry(farmerdetails,width=10,font=("times",10,"bold"))
    erate.grid(row=1,column=7,pady=15,padx=10)
        
            
    btnadd=Button(farmerdetails,text="Add",font=("times",15,"bold"),command=add_datas1)
    btnadd.grid(row=1,column=8,pady=15,padx=10)
    btndelete = Button(farmerdetails, text="Update", font=("times", 15, "bold"), command=update1)
    btndelete.grid(row=1, column=9,pady=15,padx=10)

    btndelete=Button(farmerdetails,text="Delete",font=("times",15,"bold"),command=delete_db2)
    btndelete.grid(row=1,column=10,pady=15,padx=10)
    treeframe=Frame(top)
    treeframe.grid(row=2,column=0,sticky="nw")


    mytree=ttk.Treeview(treeframe,height=300)
    mytree["columns"]=("ID","Milk Type","Fat Min","Fat Max","Rate")
    mytree.column("#0",width=0,stretch=NO)
    mytree.column("#1",width=200)
    mytree.column("#2",width=300)
    mytree.column("#3",width=300)
    mytree.column("#4",width=300)
    mytree.column("#5",width=300)

    mytree.heading("#0",text="")
    mytree.heading("#1",text="ID")
    mytree.heading("#2",text="Milk Type")
    mytree.heading("#3",text="Fat Min")
    mytree.heading("#4",text="Fat Max")
    mytree.heading("#5",text="Rate")
    datas=milkdatabase("milkdatabasenew.db")
    value=datas.fetch_rate()
    for i in value:
        pid,id,mtype,fatmin,fatmax,rate=i
        mytree.insert("","end",iid=str(pid),values=(id,mtype,fatmin,fatmax,rate))
        mytree.bind("<ButtonRelease-1>",show)
    mytree.pack(pady=50,fill=X)
    
#--------------------------------END------------------------------------------<    
        
#---------------------------------MILK COLLECTION------------------------------->
def Collection():
    top1=Toplevel(krish)
    top1.geometry("1366x768")
    krish.title("Milk Center")
    
    menuframe=Frame(top1,bg="Powder Blue",width=1366,height=40)
    menuframe.grid(row=0,column=0,sticky="nw")
    menuframe.grid_propagate(False)


    btnfarmers=Button(menuframe,bg="#A4A9AD",text="Farmer",font=("times",15),activebackground="Powder Blue",width=10)
    btnfarmers.grid(row=0,column=0)

    btnrate=Button(menuframe,bg="#A4A9AD",text="Rate",font=("times",15),activebackground="Powder Blue",width=10)
    btnrate.grid(row=0,column=1,)

    btncollction=Button(menuframe,bg="#A4A9AD",text="Collection",font=("times",15),activebackground="Powder Blue",width=10)
    btncollction.grid(row=0,column=2)

    btnreport=Button(menuframe,bg="#A4A9AD",text="Report",font=("times",15),activebackground="Powder Blue",width=10)
    btnreport.grid(row=0,column=3) 
    
        
    farmerdetails=Frame(top1,bg="#caf0f8",width=1366,height=100)
    farmerdetails.grid(row=1,column=0,sticky="nw")
    farmerdetails.grid_propagate(False)
    today=datetime.now().strftime("%d-%m-%y")

    ldate=Label(farmerdetails,text="Date",font=("times",15,"bold"),bg="#caf0f8")
    ldate.grid(row=1,column=0,pady=10,padx=10)
    ecom=Label(farmerdetails,text=today,font=("times",15,"bold"))
    ecom.grid(row=1,column=1,pady=10,padx=10)
    
    lfarmer=Label(farmerdetails,text="Farmer",font=("times",15,"bold"),bg="#caf0f8")
    lfarmer.grid(row=1,column=2,pady=15,padx=10)
    farmerfetch=milkdatabase("milkdatabasenew.db")
    value=farmerfetch.fetch() 
 
    name=list(set(i[2] for i in value))
    efatmin=ttk.Combobox(farmerdetails,width=10,font=("times",10,"bold"))
    efatmin['values']=name
    efatmin.grid(row=1,column=3,pady=15,padx=10)
      
    farmerfetch=milkdatabase("milkdatabasenew.db")
    values=farmerfetch.fetch_rate()
    values = farmerfetch.fetch_rate()

    rates_are = 0  # default rate
    i = None      # default farmer entry
    for i in values:
        
      rates_are = i[5]

    finalrate = rates_are

   
                   
    def Collections():
        if   efatmin.get() !="" and ecoms.get() !="" and  ename.get() !="" and ephone.get() !="" and evilage.get()!="" :
            val=len(mytree.get_children())+1
            farmer_name = efatmin.get()
            milk_type = ecoms.get()
            liter_val = ename.get()
            fat_val = ephone.get()
            snf_val = evilage.get()
            rate_val =  finalrate  # You might want to calculate this based on your rate table
            total_amt=int(ename.get())*finalrate 
            # messagebox.showinfo(total_amt)
            amount_val =1000  # You might want to calculate this based on liter * rate
            
            # Insert into treeview 
            mytree.insert("", "end", values=(val, today, farmer_name, milk_type, liter_val, fat_val, snf_val, rate_val,  total_amt))
            
            # Insert into database
            ratedata = milkdatabase("milkdatabasenew.db")
            ratedata.insert2( today, farmer_name, milk_type, liter_val, snf_val, fat_val, rate_val,  total_amt)
        else:
            messagebox.showerror("msg","fill all feailts")    

    
    lmtype=Label(farmerdetails,text="Milk type",font=("times",15,"bold"),bg="#caf0f8")
    lmtype.grid(row=1,column=4,pady=10,padx=10)
    ecoms=ttk.Combobox(farmerdetails,font=("times",15,"bold"),values=["Cow","Buffalo"])
    ecoms.set("Cow")
    ecoms.grid(row=1,column=5,pady=10,padx=10)
    
    
    lname=Label(farmerdetails,text="Liter",font=("times",15,"bold"),bg="#caf0f8")
    lname.grid(row=2,column=0,pady=7)
    ename=Entry(farmerdetails,font=("times",7,"bold"))
    ename.grid(row=2,column=1,pady=7)
    lphone=Label(farmerdetails,text="Fat%",font=("times",15,"bold"),bg="#caf0f8")
    lphone.grid(row=2,column=2,pady=7)
    ephone=Entry(farmerdetails,font=("times",7,"bold"))
    ephone.grid(row=2,column=3,pady=7)

    lvilage=Label(farmerdetails,text="SNF%",font=("times",15,"bold"),bg="#caf0f8")
    lvilage.grid(row=2,column=4,pady=7)
    evilage=Entry(farmerdetails,font=("times",7,"bold"))
    evilage.grid(row=2,column=5,pady=7)
    btn=Button(farmerdetails,text="Add",font=("times",10,"bold"),command=Collections,width=10)
    btn.grid(row=2,column=6,pady=7)


    treeframe=Frame(top1)
    treeframe.grid(row=2,column=0,sticky="nw")


    mytree=ttk.Treeview(treeframe,height=300)
    mytree["columns"]=("ID","Date","Farmer","Milk Type","liter","Fat","SNF","Rate","Amount")
    mytree.column("#0",width=0,stretch=NO)
    mytree.column("#1",width=50)
    mytree.column("#2",width=80)
    mytree.column("#3",width=200)
    mytree.column("#4",width=100)
    mytree.column("#5",width=200)
    mytree.column("#6",width=200)
    mytree.column("#7",width=200)
    mytree.column("#8",width=200)
    mytree.column("#9",width=200)

    mytree.heading("#0",text="")
    mytree.heading("#1",text="ID")
    mytree.heading("#2",text="Date")
    mytree.heading("#3",text="Farmer")
    mytree.heading("#4",text="Milk Type")
    mytree.heading("#5",text="lite")
    mytree.heading("#6",text="Fat")
    mytree.heading("#7",text="SNF")
    mytree.heading("#8",text="Rate")
    mytree.heading("#9",text="Amount")
    
    
    ratedata = milkdatabase("milkdatabasenew.db")
    value= ratedata .fetch_colletion()
    for i in value:
        id,date,farmer,mtype,ltr,fat,snf,rate,amt=i
        mytree.insert("","end",values=(id,date,farmer,mtype,ltr,fat,snf,rate,amt))
  
    
    mytree.bind("<ButtonRelease-1>",show)

    mytree.pack(pady=50,fill=X)
#-----------------------------------------END---------------------------------------<

#-----------------------------------REPORT PAGE-------------------------------->    
    
def report():
    top1=Toplevel(krish)
    top1.geometry("1366x768")
    krish.title("Milk Center")
  

    menuframe=Frame(top1,bg="Powder Blue",width=1366,height=40)
    menuframe.grid(row=0,column=0,sticky="nw")
    menuframe.grid_propagate(False)
    
    def fiterbtn():
    
        searchval= efatmin.get()
        fromdate=ename.get()
        todate=  ename.get()
        add_database=milkdatabase("milkdatabasenew.db")
        result=add_database.filter(searchval,fromdate,todate)
        if not searchval=="": 
            for item in mytree.get_children():
                mytree.delete(item)
            for i in  result:
                id,date,farmer,mtype,ltr,fat,snf,rate,amt = i
                mytree.insert("", index="end", values=(id,date,farmer,mtype,ltr,fat,snf,rate,amt))
        
        else:
            messagebox.showinfo("msg","search box is empty") 
    def TodaySumery():
        today=datetime.now().strftime("%d-%m-%y")
    
        searchval=today

        add_database=milkdatabase("milkdatabasenew.db")
        result=add_database.day_summery(searchval)
        if not searchval=="":
            for item in mytree.get_children():
                mytree.delete(item)
            for i in  result:
                id,date,farmer,mtype,ltr,fat,snf,rate,amt = i
                mytree.insert("", index="end", values=(id,date,farmer,mtype,ltr,fat,snf,rate,amt))
        
        else:
            messagebox.showinfo("msg","search box is empty") 

    btnfarmers=Button(menuframe,bg="#A4A9AD",text="Farmer",font=("times",15),activebackground="Powder Blue",width=10)
    btnfarmers.grid(row=0,column=0)

    btnrate=Button(menuframe,bg="#A4A9AD",text="Rate",font=("times",15),activebackground="Powder Blue",width=10)
    btnrate.grid(row=0,column=1,)

    btncollction=Button(menuframe,bg="#A4A9AD",text="Collection",font=("times",15),activebackground="Powder Blue",width=10)
    btncollction.grid(row=0,column=2)

    btnreport=Button(menuframe,bg="#A4A9AD",text="Report",font=("times",15),activebackground="Powder Blue",width=10)
    btnreport.grid(row=0,column=3) 
    
        
    farmerdetails=Frame(top1,bg="#caf0f8",width=1366,height=100)
    farmerdetails.grid(row=1,column=0,sticky="nw")
    farmerdetails.grid_propagate(False)

    
    
    lname=Label(farmerdetails,text="From",font=("times",15,"bold"),bg="#caf0f8")
    lname.grid(row=2,column=0,pady=7)
    ename=Entry(farmerdetails,font=("times",15,"bold"))
    ename.grid(row=2,column=1,pady=7)
    lphone=Label(farmerdetails,text="To",font=("times",15,"bold"),bg="#caf0f8")
    lphone.grid(row=2,column=2,pady=7)
    ename=Entry(farmerdetails,font=("times",15,"bold"))
    ename.grid(row=2,column=3,pady=7)
    lrate=Label(farmerdetails,text="Farmer",font=("times",15,"bold"),bg="#caf0f8")
    lrate.grid(row=2,column=4,pady=15,padx=10)
    
    farmerfetch=milkdatabase("milkdatabasenew.db")
    value=farmerfetch.fetch()
    
    
    name=list(set(i[2] for i in value))
    efatmin=ttk.Combobox(farmerdetails,width=10,font=("times",10,"bold"))
    efatmin['values']=name
    efatmin.grid(row=2,column=5,pady=15,padx=10)
    

        
    btnadd=Button(farmerdetails,text="Filter",font=("times",15,"bold"),command=fiterbtn)
    btnadd.grid(row=2,column=6,pady=7,padx=10)
    btndelete = Button(farmerdetails, text="TodaySumery", font=("times", 15, "bold"),command=TodaySumery)
    btndelete.grid(row=2, column=7,pady=7,padx=10)



    treeframe=Frame(top1)
    treeframe.grid(row=2,column=0,sticky="nw")


    mytree=ttk.Treeview(treeframe,height=300)
    mytree["columns"]=("ID","Date","Farmer","Milk Type","liter","Fat","SNF","Rate","Amount")
    mytree.column("#0",width=0,stretch=NO)
    mytree.column("#1",width=50)
    mytree.column("#2",width=80)
    mytree.column("#3",width=200)
    mytree.column("#4",width=100)
    mytree.column("#5",width=200)
    mytree.column("#6",width=200)
    mytree.column("#7",width=200)
    mytree.column("#8",width=200)
    mytree.column("#9",width=200)

    mytree.heading("#0",text="")
    mytree.heading("#1",text="ID")
    mytree.heading("#2",text="Date")
    mytree.heading("#3",text="Farmer")
    mytree.heading("#4",text="Milk Type")
    mytree.heading("#5",text="lite")
    mytree.heading("#6",text="Fat")
    mytree.heading("#7",text="SNF")
    mytree.heading("#8",text="Rate")
    mytree.heading("#9",text="Amount")
    mytree.pack(pady=50,fill=X)
    ratedata = milkdatabase("milkdatabasenew.db")
    value= ratedata .fetch_colletion()
    for i in value:
        id,date,farmer,mtype,ltr,fat,snf,rate,amt=i
        mytree.insert("","end",values=(id,date,farmer,mtype,ltr,fat,snf,rate,amt))
#------------------------------------------REPORT PAGE END--------------------------<

#==========================================FIRST PAGE================================>        

krish=Tk()
krish.geometry("1366x768")
krish.title("Milk Center")

menuframe=Frame(krish,bg="Powder Blue",width=1366,height=40)
menuframe.grid(row=0,column=0,sticky="nw")
menuframe.grid_propagate(False)


btnfarmers=Button(menuframe,bg="#A4A9AD",text="Farmer",font=("times",15),activebackground="Powder Blue",width=10)
btnfarmers.grid(row=0,column=0)

btnrate=Button(menuframe,bg="#A4A9AD",text="Rate",font=("times",15),activebackground="Powder Blue",width=10,command=rates)
btnrate.grid(row=0,column=1,)

btncollction=Button(menuframe,bg="#A4A9AD",text="Collection",font=("times",15),activebackground="Powder Blue",width=10,command=Collection)
btncollction.grid(row=0,column=2)

btnreport=Button(menuframe,bg="#A4A9AD",text="Report",font=("times",15),activebackground="Powder Blue",width=10,command=report)
btnreport.grid(row=0,column=3)


farmerdetails=Frame(krish,bg="#caf0f8",width=1366,height=100)
farmerdetails.grid(row=1,column=0,sticky="nw")
farmerdetails.grid_propagate(False)

lname=Label(farmerdetails,text="Name",font=("times",15,"bold"),bg="#caf0f8")
lname.grid(row=1,column=0,pady=10)
ename=Entry(farmerdetails,font=("times",15,"bold"))
ename.grid(row=1,column=1,pady=10)
lphone=Label(farmerdetails,text="Phone",font=("times",15,"bold"),bg="#caf0f8")
lphone.grid(row=1,column=2,pady=10)
ephone=Entry(farmerdetails,font=("times",15,"bold"))
ephone.grid(row=1,column=3,pady=10)

lvilage=Label(farmerdetails,text="Village",font=("times",15,"bold"),bg="#caf0f8")
lvilage.grid(row=1,column=4,pady=10)
evilage=Entry(farmerdetails,font=("times",15,"bold"))
evilage.grid(row=1,column=5,pady=10)

btnadd=Button(farmerdetails,text="Add",font=("times",15,"bold"),command=add_datas)
btnadd.grid(row=1,column=6)
btndelete = Button(farmerdetails, text="Update", font=("times", 15, "bold"), command=update)
btndelete.grid(row=1, column=7)

btndelete=Button(farmerdetails,text="Delete",font=("times",15,"bold"),command=delete_db)
btndelete.grid(row=1,column=8)

lsearch=Label(farmerdetails,text="Search",font=("times",15,"bold"),bg="#caf0f8")
lsearch.grid(row=2,column=0)

esearch=Entry(farmerdetails,font=("times",15,"bold"))
esearch.grid(row=2,column=1)

btngo=Button(farmerdetails,text="Go",font=("times",10,"bold"),command=go)
btngo.grid(row=2,column=2)

treeframe=Frame(krish)
treeframe.grid(row=2,column=0,sticky="nw")


mytree=ttk.Treeview(treeframe,height=300)
mytree["columns"]=("ID","Name","Phone","Village")
mytree.column("#0",width=0,stretch=NO)
mytree.column("#1",width=350)
mytree.column("#2",width=350)
mytree.column("#3",width=350)
mytree.column("#4",width=350)

mytree.heading("#0",text="")
mytree.heading("#1",text="ID")
mytree.heading("#2",text="Name")
mytree.heading("#3",text="Phone")
mytree.heading("#4",text="Village")
datas=milkdatabase("milkdatas.db") 
value=datas.fetch()

mytree.pack(pady=50,fill=X)
add_database=milkdatabase("milkdatabasenew.db")
values=add_database.fetch()

for i in values:
    pid,id,name,phone,village=i
    mytree.insert("",index="end",values=(id,name,phone,village))

mytree.bind("<<TreeviewSelect>>",show)
krish.mainloop()
#===============================FIRST PAGE END==========================<

