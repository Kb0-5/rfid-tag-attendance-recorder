import mysql.connector as sql
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import serial
root = Tk()
root.title('Admin page')
root.resizable(False,False)
root.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')
no,f,l,gd,cno,opwd,npwd,op,np='','','','','','','','',''
hds1,ast,rst,rdbs=None,None,None,None
run=True
rcl=[]
def irf():
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute('select dbpwd from datchng where timeofaccess=(select max(timeofaccess) from datchng where dbpwd is not null);')
    r=cur.fetchall()
    cn.close()
    return(r[0][0])

def cr():
    arduino= serial.Serial('COM4',115300,timeout=.1)
    n=''
    while True:
        rawdata=arduino.readline()
        data=str(rawdata.decode('utf-8'))
        if data.startswith("S") and data[2:]!=n and data[2] in '1234567890':
            n=(data[2:]).strip()
            return(n)
#=============================================Student===================================================
def student():
    global pwd
    st=Toplevel()
    st.resizable(False,False)
    st.title('Student List/Add Student/Remove Student')
    st.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')

    sframe=Frame(st,bd=10,relief=SUNKEN)
    sframe.place(x=0,y=0)
    
    ssl=Button(st, text='Show Student List', command=slist,padx=46,pady=10)
    ssl.grid(row=0,column=0)
    ast=Button(st, text='Add Student',command=adds,padx=42,pady=10)
    ast.grid(row=0,column=1)
    rst=Button(st, text='Remove Student',command=rms,padx=50,pady=10)
    rst.grid(row=1,column=0)
    rst=Button(st, text='Student attendance',command=sattd,padx=23,pady=10)
    rst.grid(row=1,column=1)
    close=Button(st, text='Exit',command=st.destroy,padx=10,pady=5)
    close.grid(row=2,column=2)
    st.mainloop()
    
def slist():
    global pwd
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    
    cur.execute("select rcno,concat(fname,' ',lname),gen,pno from stdb")
    r=cur.fetchall()
    shows(r)
    cn.close()

def shows(d):
    stdbs=Toplevel()
    stdbs.attributes("-fullscreen",True)
    stdbs.title('Student List')
    stdbs.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')
    
    dframe=Frame(stdbs,bd=10,relief=SUNKEN)
    dframe.pack(fill=BOTH,expand=1)
    
    hds=ttk.Treeview(dframe,column=('rcn','name','gen','pno'))
    s_y=ttk.Scrollbar(dframe,orient=VERTICAL,command=hds.yview)    
    s_y.pack(side=RIGHT,fill=Y)
    hds.configure(yscrollcommand=s_y.set)

    hds.heading('rcn',text='RFID Card Number')
    hds.heading('name',text='Name of Student')
    hds.heading('gen',text='Gender')
    hds.heading('pno',text='Contact Number')

    hds['show']="headings"

    hds.column('gen',width=150)
    hds.pack(fill=Y,expand=1)

    if len(d)!=0:
        for i in d:
            hds.insert('',END,values=i)

def adds():
    global no,f,l,gd,cno,ast
    ast=Toplevel()
    ast.resizable(False,False)
    ast.title('Add Student')
    ast.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')
    messagebox.showinfo('Place Card','Place RFID Card on sensor to register')
    
    rc=Label(ast,text='RFID Card Number',bd=3,padx=3,pady=5)
    rc.grid(row=4,column=0)
    no=cr()
    rcno=Label(ast,text=no)
    rcno.grid(row=4,column=1)
    fn=Label(ast,text='First Name of Student',bd=3,padx=3,pady=5)
    fn.grid(row=0,column=0)
    f=Entry(ast,width=30)
    f.grid(row=0,column=1)
    ln=Label(ast,text='Last Name of Student',bd=3,padx=3,pady=5)
    ln.grid(row=1,column=0)
    l=Entry(ast,width=30)
    l.grid(row=1,column=1)
    g=Label(ast,text='Gender',bd=3,padx=3,pady=5)
    g.grid(row=2,column=0)
    gd=StringVar()
    gd.set('------')
    dm=OptionMenu(ast,gd, 'M','F','O')
    dm.grid(row=2,column=1)
    cn=Label(ast,text='Contact Number',bd=3,padx=3,pady=5)
    cn.grid(row=3,column=0)
    cno=Entry(ast,width=30)
    cno.grid(row=3,column=1)
    submit=Button(ast, text='Submit',command=uploadscheck,padx=10,pady=5)
    submit.grid(row=4,column=2)
    
    ast.mainloop()

def uploadscheck():
    global no,f,l,gd,cno
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute('select rcno from stdb')
    d=(cur.fetchall())
    cn.close()
    c=0
    for i in cno.get():
        if i not in '1234567890':
            c+=1
    if str(no) in d:
        messagebox.showerror('Error!','Card already registered in the database')
    elif no=='' or f.get()=='' or l.get()=='' or gd.get() not in ('M','F','O') or cno.get()=='':
        messagebox.showerror('Error!','Fields cannot be empty')
    elif c!=0:
        messagebox.showerror('Error!','Contact Number cannot be String')
    else:
        uploads()

def uploads():
    global no,f,l,gd,cno,ast
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    conno=int(cno.get())
    try:
        cur.execute('insert into stdb values(%s, %s, %s, %s, %s)',(no,f.get(),l.get(),gd.get(),conno))
        cur.execute('insert into stp(rcno) values(%s)',[no])
        f.delete(0,END)
        l.delete(0,END)
        gd.set('------')
        cno.delete(0,END)
        messagebox.showinfo('Completed!','Student added successfully')
    except sql.IntegrityError:
        messagebox.showerror('Error!','Card already Registered')
    ast.destroy()
    cn.close()
    
def rms():
    global no,rst
    rst=Toplevel()
    rst.resizable(False,False)
    rst.title('Remove Student')
    rst.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')

    messagebox.showinfo('Place Card','Place RFID Card on sensor')
    rc=Label(rst,text='RFID Card Number',bd=3,padx=3,pady=5)
    rc.grid(row=0,column=0)
    no=cr()
    rcno=Label(rst,text=no)
    rcno.grid(row=0,column=1)
    Delete=Button(rst, text='Submit',command=popups,padx=10,pady=5)
    Delete.grid(row=1,column=2)

def popups():
    r=messagebox.askokcancel('Confirmation','Are you sure you want to delete this student from database?')
    if r==1:
        deletes()

def deletes():
    global no,rst
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()    
    cur.execute('delete from statd where rcno=%s',[no])
    cur.execute('delete from stp where rcno=%s',[no])
    cur.execute('delete from stdb where rcno=%s',[no])
    cn.close()

    messagebox.showinfo('Completed!','Student deleted from database successfully')
    rst.destroy()

def sattd():
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute("select concat(fname,' ',lname) as stname,present,max(timing) from stdb,stp,statd where stdb.rcno=stp.rcno and stp.rcno=statd.rcno group by stdb.rcno order by timing") 
    d=cur.fetchall()
    sdbs=Toplevel()
    sdbs.attributes("-fullscreen",True)
    sdbs.title('Staff List')
    sdbs.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')
    
    dframe=Frame(sdbs,bd=10,relief=SUNKEN)
    dframe.pack(fill=BOTH,expand=1)
    
    hds=ttk.Treeview(dframe,column=('name','pa','t'))
    s_y=ttk.Scrollbar(dframe,orient=VERTICAL,command=hds.yview)    
    s_y.pack(side=RIGHT,fill=Y)
    hds.configure(yscrollcommand=s_y.set)

    hds.heading('name',text='Name of Student')
    hds.heading('pa',text='Present/Absent')
    hds.heading('t',text='Time of arrival/departure')

    hds['show']="headings"
    hds.pack(fill=Y,expand=1)
    if len(d)!=0:
        for i in d:
            l=[]
            l.append(i[0])
            if i[1]=='':
                l.append('Absent')
            else:
                l.append('Present')
            l.append(i[2])
            hds.insert('',END,values=l)

#============================================Staff=====================================================

def Staff():
    global pwd
    st=Toplevel()
    st.resizable(False,False)
    st.title('Staff List/Add Staff/Remove Staff')
    st.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')

    sframe=Frame(st,bd=10,relief=SUNKEN)
    sframe.place(x=0,y=0)
    
    ssl=Button(st, text='Show Staff List', command=stlist,padx=47,pady=10)
    ssl.grid(row=0,column=0)
    ast=Button(st, text='Add Staff',command=addst,padx=50,pady=10)
    ast.grid(row=0,column=1)
    rst=Button(st, text='Remove Staff',command=rmst,padx=50,pady=10)
    rst.grid(row=1,column=0)
    rst=Button(st, text='Staff attendance',command=stattd,padx=32,pady=10)
    rst.grid(row=1,column=1)
    close=Button(st, text='Exit',command=st.destroy,padx=10,pady=5)
    close.grid(row=2,column=2)
    st.mainloop()
    
def stlist():
    global pwd
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute("select rcno,concat(fname,' ',lname),gen,pno from cdb")
    r=cur.fetchall()
    showst(r)    
    cn.close()

def showst(d):
    stdbs=Toplevel()
    stdbs.attributes("-fullscreen",True)
    stdbs.title('Staff List')
    stdbs.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')
    
    dframe=Frame(stdbs,bd=10,relief=SUNKEN)
    dframe.pack(fill=BOTH,expand=1)
    
    hds=ttk.Treeview(dframe,column=('rcn','name','gen','pno'))
    s_y=ttk.Scrollbar(dframe,orient=VERTICAL,command=hds.yview)    
    s_y.pack(side=RIGHT,fill=Y)
    hds.configure(yscrollcommand=s_y.set)

    hds.heading('rcn',text='RFID Card Number')
    hds.heading('name',text='Name of Student')
    hds.heading('gen',text='Gender')
    hds.heading('pno',text='Contact Number')

    hds['show']="headings"
    hds.column('gen',width=150)
    hds.pack(fill=Y,expand=1)

    if len(d)!=0:
        for i in d:
            hds.insert('',END,values=i)

def addst():
    global no,f,l,gd,cno,ast
    ast=Toplevel()
    ast.resizable(False,False)
    ast.title('Add Student')
    ast.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')

    messagebox.showinfo('Place Card','Place RFID Card on sensor to register')
    
    rc=Label(ast,text='RFID Card Number',bd=3,padx=3,pady=5)
    rc.grid(row=4,column=0)
    no=cr()
    rcno=Label(ast,text=no)
    rcno.grid(row=4,column=1)
    fn=Label(ast,text='First Name of Student',bd=3,padx=3,pady=5)
    fn.grid(row=0,column=0)
    f=Entry(ast,width=30)
    f.grid(row=0,column=1)
    ln=Label(ast,text='Last Name of Student',bd=3,padx=3,pady=5)
    ln.grid(row=1,column=0)
    l=Entry(ast,width=30)
    l.grid(row=1,column=1)
    g=Label(ast,text='Gender',bd=3,padx=3,pady=5)
    g.grid(row=2,column=0)
    gd=StringVar()
    gd.set('------')
    dm=OptionMenu(ast,gd, 'M','F','O')
    dm.grid(row=2,column=1)
    cn=Label(ast,text='Contact Number',bd=3,padx=3,pady=5)
    cn.grid(row=3,column=0)
    cno=Entry(ast,width=30)
    cno.grid(row=3,column=1)
    submit=Button(ast, text='Submit',command=uploadstcheck,padx=10,pady=5)
    submit.grid(row=4,column=2)
    
    ast.mainloop()

def uploadstcheck():
    global no,f,l,gd,cno
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute('select rcno from cdb')
    d=(cur.fetchall())
    cn.close()
    c=0
    for i in cno.get():
        if i not in '1234567890':
            c+=1
    if str(no) in d:
        messagebox.showerror('Error!','Card already registered in the database')
    elif no=='' or f.get()=='' or l.get()=='' or gd.get() not in ('M','F','O') or cno.get()=='':
        messagebox.showerror('Error!','Fields cannot be empty')
    elif c!=0:
        messagebox.showerror('Error!','Contact Number cannot be String')
    else:
        uploadst()

def uploadst():
    global no,f,l,gd,cno,ast   
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    conno=int(cno.get())
    try:
        cur.execute('insert into cdb values(%s, %s, %s, %s, %s)',(no,f.get(),l.get(),gd.get(),conno))
        cur.execute('insert into cp(rcno) values(%s)',[no])
        f.delete(0,END)
        l.delete(0,END)
        gd.set('------')
        cno.delete(0,END)
        messagebox.showinfo('Completed!','Staff added successfully')
    except sql.IntegrityError:
        messagebox.showerror('Error!','Card already Registered')
    ast.destroy()
    cn.close()
    
def rmst():
    global no,rst
    rst=Toplevel()
    rst.resizable(False,False)
    rst.title('Remove Student')
    rst.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')

    messagebox.showinfo('Place Card','Place RFID Card on sensor')
    rc=Label(rst,text='RFID Card Number',bd=3,padx=3,pady=5)
    rc.grid(row=0,column=0)
    no=cr()
    rcno=Label(rst,text=no)
    rcno.grid(row=0,column=1)
    Delete=Button(rst, text='Submit',command=popupst,padx=10,pady=5)
    Delete.grid(row=1,column=2)

def popupst():
    r=messagebox.askokcancel('Confirmation','Are you sure you want to delete this staff from database?')
    if r==1:
        deletest()

def deletest():
    global no,rst    
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute('delete from catd where rcno=%s',[no])
    cur.execute('delete from cp where rcno=%s',[no])
    cur.execute('delete from cdb where rcno=%s',[no])    
    cn.close()
    
    messagebox.showinfo('Completed!','Staff deleted from database successfully')
    rst.destroy()

def stattd():
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute("select concat(fname,' ',lname) as stname,present,max(timing) from cdb,cp,catd where cdb.rcno=cp.rcno and cp.rcno=catd.rcno group by cdb.rcno order by timing") 
    d=cur.fetchall()
    stdbs=Toplevel()
    stdbs.attributes("-fullscreen",True)
    stdbs.title('Staff List')
    stdbs.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')
    
    dframe=Frame(stdbs,bd=10,relief=SUNKEN)
    dframe.pack(fill=BOTH,expand=1)
    
    hds=ttk.Treeview(dframe,column=('name','pa','t'))
    s_y=ttk.Scrollbar(dframe,orient=VERTICAL,command=hds.yview)    
    s_y.pack(side=RIGHT,fill=Y)
    hds.configure(yscrollcommand=s_y.set)

    hds.heading('name',text='Name of Staff')
    hds.heading('pa',text='Present/Absent')
    hds.heading('t',text='Time of arrival/departure')

    hds['show']="headings"
    hds.pack(fill=Y,expand=1)
    if len(d)!=0:
        for i in d:
            l=[]
            l.append(i[0])
            if i[1]=='':
                l.append('Absent')
            else:
                l.append('Present')
            l.append(i[2])
            hds.insert('',END,values=l)

#===========================================Change Password=============================================
def chngpwd():
    global no,cd,pwd,op,np,opwd,npwd,rst
    
    rst=Toplevel()
    rst.resizable(False,False)
    rst.title('Change Password')
    rst.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')

    messagebox.showinfo('Place Card','Place Admin RFID Card/tag on sensor')
    
    rc=Label(rst,text='RFID Card Number',bd=3,padx=3,pady=5)
    rc.grid(row=0,column=0)
    no=cr()
    rcno=Label(rst,text=no)
    rcno.grid(row=0,column=1)
    opwd=Label(rst,text='Old Password',bd=3,padx=3,pady=5)
    opwd.grid(row=1,column=0)
    op=Entry(rst,width=30)
    op.grid(row=1,column=1)
    npwd=Label(rst,text='New Password',bd=3,padx=3,pady=5)
    npwd.grid(row=2,column=0)
    np=Entry(rst,width=30)
    np.grid(row=2,column=1)
    npwd=np.get()
    opwd=op.get()
    confirm=Button(rst, text='Submit',command=epa,padx=10,pady=5)
    confirm.grid(row=3,column=3)

def epa():
    global no,pwd,cd,op,rst,np
    if pwd==op.get() and cd==no:
        popupchng()
    elif cd!=no: 
        messagebox.showerror('Error!','Wrong Card')
        rst.destroy()
    elif pwd!=op.get():
        messagebox.showerror('Error!','Your Old Password is Incorrect')
    elif pwd==op.get() and op.get()==np.get():
        print('op',op.get())
        print('pwd',pwd)
        messagebox.showerror('Error!','Old and New Password cannot be Same')

def popupchng():
    r=messagebox.askokcancel('Confirmation','Are you sure you want to change the password?')
    if r==1:
        chng()

def chng():
    global np,no,rst,pwd
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute('insert into datchng values (%s,%s,now())',(np.get(),no))
    cn.close()
    messagebox.showinfo('Completed!','Password changed successfully')
    rst.destroy()
    pwd=irf()
#========================================Record Attendance==================================== 
def crl():
    global rdbs
    arduino= serial.Serial('COM4',115300,timeout=.1)
    n=''
    while True:
        rawdata=arduino.readline()
        data=str(rawdata.decode('utf-8'))
        if data.startswith("S") and data[2:]!=n and data[2] in '1234567890':
            n=(data[2:]).strip()
            return(n)
def ratd():
    global rcl,hds1,rdbs
    run=True
    rdbs=Toplevel()
    rdbs.attributes("-fullscreen",True)
    rdbs.title('Record Attendance')
    rdbs.iconbitmap('C:/Users/Admin/Downloads/atdicon.ico')
    rcl=[]
    dframe=Frame(rdbs,bd=10,relief=SUNKEN)
    dframe.pack(fill=BOTH,expand=1)
    
    hds1=ttk.Treeview(dframe,column=('rcn'))
    s_y=ttk.Scrollbar(dframe,orient=VERTICAL,command=hds1.yview)    
    s_y.pack(side=RIGHT,fill=Y)
    hds1.configure(yscrollcommand=s_y.set)
    hds1.heading('rcn',text='RFID Card Number')
    hds1['show']="headings"
    hds1.pack(fill=Y,expand=1)
    ex=Button(rdbs, text='Exit', command=rdbs.destroy,padx=10,pady=5)
    ex.pack(side=RIGHT)
    dis()
    rdbs.mainloop()

def dis():
    global rcl,hds1,no
    if hds1!=None:
        no=crl()
        if no!=None:
            rcl.append(no)
        attd()
        hds1.delete(*hds1.get_children())
        for i in rcl:
            hds1.insert('',END,values=(i,))
        hds1.after(500,dis)

def attd():
    global no
    print(no)
    cn=sql.connect(host='localhost',user='root',passwd='',database='rar')
    cur=cn.cursor()
    cur.execute("select rcno from stp")
    sp=(cur.fetchall())[0]
    cur.execute("select rcno from cp")
    cp=(cur.fetchall())[0]
    if no in sp:
        cur.execute("select present from stp where rcno=%s",[no])
        n=(cur.fetchall())[0][0]
        print(n)
        if n=='*':
            cur.execute("update stp set present='' where rcno=%s",[no])
        else:
            cur.execute("update stp set present='*' where rcno=%s",[no])
        cur.execute("insert into statd values(%s,now())",[no])
        cn.close()
    if no in cp:
        cur.execute("select present from cp where rcno=%s",[no])
        n=(cur.fetchall())[0][0]
        print(n)
        if n=='*':
            cur.execute("update cp set present='' where rcno=%s",[no])
        else:
            cur.execute("update cp set present='*' where rcno=%s",[no])
        cur.execute("insert into catd values(%s,now())",[no])
        cn.close()
#================================Main window=================================================

pwd=irf()
cd=cr()

mframe=Frame(root,bd=10,relief=SUNKEN)
mframe.place(x=0,y=0)
sl=Button(root, text='Student List/Add Student/Remove Student', command=student,padx=4,pady=10)
sl.grid(row=0,column=0)
cl=Button(root, text='Staff List/Add Staff/Remove Staff', command=Staff,padx=14,pady=10)
cl.grid(row=0,column=1)
chngpwd=Button(root, text='Change Password', command=chngpwd,padx=69,pady=10)
chngpwd.grid(row=1,column=0)
atd=Button(root, text='Record Attendance', command=ratd,padx=50,pady=10)
atd.grid(row=1,column=1)
ex=Button(root, text='Exit', command=root.destroy,padx=10,pady=5)
ex.grid(row=2,column=3)
root.mainloop()
