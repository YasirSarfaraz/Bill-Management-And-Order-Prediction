import mysql.connector
import pandas as pd
import warnings
from Predict import ProductPredictor
from tkinter import *
from datetime import datetime
from tkinter import Toplevel, Label, Button
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", message="^pandas only supports SQLAlchemy connectable.*", category=UserWarning)



conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yasir",
    database="kaathi_house_db"
)


root=Tk()
root.geometry("1000x700")
root.title("KAATHI HOUSE")
root.resizable(False,False)
predictor = ProductPredictor()


def predict_and_display():
    # Load data
    X, y = predictor.load_data()

    # Train the model
    predictor.train_model(X, y)

    # Predict next hour
    current_datetime = pd.Timestamp.now()
    end_datetime = current_datetime + pd.Timedelta(hours=1)
    prediction_interval = pd.date_range(start=current_datetime, end=end_datetime, freq='2T')
    predictions = predictor.predict_next_hour()

    # Most common prediction
    most_common = predictor.most_common_prediction(predictions)

    # Create Window 1 to display predictions
    window1 = Toplevel(root)
    window1.title("Predictions for Next Hour")
    window1.geometry("400x300")

    # Display the predictions in Window 1
    label1 = Label(window1, text="Predicted product orders for the next 1 hour (every 2 minutes):", font=("Times", 12))
    label1.pack()

    for timestamp, prediction in zip(prediction_interval, predictions):
        label = Label(window1, text=f"{timestamp}: {prediction}", font=("Times", 12))
        label.pack()

    # Create Window 2 to display the most common prediction
    window2 = Toplevel(root)
    window2.title("Most Common Prediction")
    window2.geometry("400x300")

    # Display the most common prediction in Window 2
    label2 = Label(window2, text=f"Most common predicted product: {most_common}", font=("Times", 12))
    label2.pack()



# def open_window1():
#     window1 = Toplevel(root)
#     window1.title("Window 1")
#     window1.geometry("400x300")  # Set the size of Window 1
#     label1 = Label(window1, text="This is Window 1")
#     predictor = ProductPredictor()

#     label1.pack()

# def open_window2():
#     window2 = Toplevel(root)
#     window2.title("Window 2")
#     window2.geometry("400x300")  # Set the size of Window 2
#     label2 = Label(window2, text="This is Window 2")
#     label2.pack()


def Reset():
    entry_Kaathiroll.delete(0,END)
    entry_Paratha.delete(0,END)
    entry_CholeB.delete(0,END)
    entry_chillipotato.delete(0,END)
    entry_KHWrap.delete(0,END)
    entry_Vanila.delete(0,END)
    entry_pavbhaji.delete(0,END)
    Total_bill.set("")
    txt.delete('1.0',END)
#######################################################################
def on_closing(connection):
    connection.close()
    root.destroy()

    

##################################################################
def Total():
    try:a1=int(Kaathiroll.get())
    except:a1=0

    try:a2=int(Paratha.get())
    except:a2=0

    try:a3=int(CholeB.get())
    except:a3=0

    try:a4=int(chillipotato.get())
    except:a4=0

    try:a5=int(pavbhaji.get())
    except:a5=0

    try:a6=int(KHWrap.get())
    except:a6=0

    try:a7=int(Vanila.get())
    except:a7=0

    #define cost of each item per quantity
    c1=65*a1
    c2=55*a2
    c3=75*a3
    c4=70*a4
    c5=90*a5
    c6=100*a6
    c7=200*a7
    current_date = datetime.now().date()
    current_time = datetime.now().strftime('%H:%M:%S')

    cursor = conn.cursor()
    if a1 > 0:
        cursor.execute("INSERT INTO orders (product, quantity, price,order_date, order_time) VALUES (%s, %s, %s, %s, %s)", ("Kaathi Roll", a1, c1, current_date, current_time))
    if a2 > 0:
        cursor.execute("INSERT INTO orders (product, quantity, price, order_date, order_time) VALUES (%s, %s, %s, %s, %s)", ("Paratha", a2, c2, current_date, current_time))
    if a3 > 0:
        cursor.execute("INSERT INTO orders (product, quantity, price, order_date, order_time) VALUES (%s, %s, %s, %s, %s)", ("Chole Bhature", a3, c3, current_date, current_time))
    if a4 > 0:
        cursor.execute("INSERT INTO orders (product, quantity, price, order_date, order_time) VALUES (%s, %s, %s, %s, %s)", ("Chilli Potato", a4, c4, current_date, current_time))
    if a5 > 0:
        cursor.execute("INSERT INTO orders (product, quantity, price, order_date, order_time) VALUES (%s, %s, %s, %s, %s)", ("Pav Bhaji", a5, c5, current_date, current_time))
    if a6 > 0:
        cursor.execute("INSERT INTO orders (product, quantity, price, order_date, order_time) VALUES (%s, %s, %s, %s, %s)", ("KH Wrap", a6, c6, current_date, current_time))
    if a7 > 0:
        cursor.execute("INSERT INTO orders (product, quantity, price, order_date, order_time) VALUES (%s, %s, %s, %s, %s)", ("Vanila Cake", a7, c7, current_date, current_time))

    query = "SELECT * FROM orders"

    # Read the data into a DataFrame
    df = pd.read_sql(query, conn)
    
    df['order_date'] = df['order_date'].astype(str)
    df['order_time'] = df['order_time'].astype(str)
    df['order_time'] = df['order_time'].apply(lambda x: x.split()[-1])

    # Define the file path for the Excel file
    excel_file_path = "orders_data.xlsx"

    # Write the DataFrame to an Excel file
    df.to_excel(excel_file_path, index=False)

    print("Excel file updated successfully.")
    
    cursor.execute("SELECT * FROM (SELECT * FROM orders ORDER BY order_date DESC, order_time DESC LIMIT 15) AS latest_orders ORDER BY order_date ASC, order_time ASC")

# Fetch all rows
    rows = cursor.fetchall()

# Print column headers
    print("{:<3} | {:<20} | {:<12} | {:<12} | {:<14} | {:<10}".format("ID", "Product", "Quantity", "Price", "Order Date", "Order Time"))
    print("-" * 70)

    for row in rows:
    # Ensure row elements are correctly formatted
        id_str = str(row[0])
        product_str = str(row[1])
        quantity_str = str(row[2])
        price_str = "{:.2f}".format(row[3]) if isinstance(row[3], float) else str(row[3])
        order_date_str = str(row[4])
        order_time_str = str(row[5])

    # Print with equalized spacing
        print("{:<3} | {:<20} | {:<12} | {:<12} | {:<14} | {:<10}".format(id_str, product_str, quantity_str, price_str, order_date_str, order_time_str))


    # Commit changes to the database
    conn.commit()

    # Close cursor
    cursor.close()




    txt.delete('1.0',END)
    txt.insert(END,"       Welcome To KAATHI HOUSE\n")
    txt.insert(END, f"\nDate: {datetime.now().date()} Time: {datetime.now().time()}")
    txt.insert(END,"\n==================================")
    txt.insert(END,"\nProduct          Qty         Price")
    txt.insert(END,"\n==================================")

#######################################################################################################

        
    if Kaathiroll.get() !="":
        txt.insert(END,f"\nKaathiroll        {int(Kaathiroll.get())}          {c1}")
    if Paratha.get() != "":
        txt.insert(END,f"\nParatha           {int(Paratha.get())}          {c2}")
    if CholeB.get() != "":
        txt.insert(END,f"\nCholeB            {int(CholeB.get())}          {c3}")
    if chillipotato.get() != "":
        txt.insert(END,f"\nchillipotato      {int(chillipotato.get())}          {c4}")
    if pavbhaji.get() != "" :
        txt.insert(END,f"\npavBhaji          {int(pavbhaji.get())}          {c5}")
    if KHWrap.get() != "":
        txt.insert(END,f"\nKhWrap            {int(KHWrap.get())}          {c6}")
    if Vanila.get() != "":
        txt.insert(END,f"\nVanila            {int(Vanila.get())}          {c7}")
    txt.insert(END,"\n==================================")

 ##############################################################################

    lbl_total=Label(f2,font=("aria",10,"bold"),text="Total",width=16,fg="lightyellow",bg="black")
    lbl_total.place(x=70,y=295)

    entry_total=Entry(f2,font=("aria",20,"bold"),textvariable=Total_bill,bd=6,width=15,bg="beige")
    entry_total.place(x=20,y=320)

    totalcost=c1+c2+c3+c4+c5+c6+c7
    string_bill="Rs.",str('%.2f'%totalcost)
    Total_bill.set(string_bill)

Label(text="KAATHI HOUSE",bg="lightblue",fg="black",font=("Times",33,"bold"),width="300",height="2").pack()
#Menu Card
f=Frame(root,bg="beige",highlightbackground="black",highlightthickness=4,width=300,height=370)
f.place(x=10,y=118)
Label(f,text="Menu",font=("Times",28,"bold","underline"),fg="black",bg="beige",justify=CENTER).place(x=80,y=5)
Label(f,font=("Times",17,),text="Kathi Roll-Rs.65   ",fg="black",bg="beige",justify=CENTER).place(x=40,y=80)
Label(f,font=("Times",17),text="Paratha-Rs.55    ",fg="black",bg="beige",justify=CENTER).place(x=40,y=110)
Label(f,font=("Times",17),text="Chole Bhature-Rs.75 ",fg="black",bg="beige",justify=CENTER).place(x=40,y=140)
Label(f,font=("Times",17),text="Chilli Potato-Rs.70   ",fg="black",bg="beige",justify=CENTER).place(x=40,y=170)
Label(f,font=("Times",17),text="Pav bhaji-Rs.90    ",fg="black",bg="beige",justify=CENTER).place(x=40,y=200)
Label(f,font=("Times",17),text="KH Wrap-Rs.100",fg="black",bg="beige",justify=CENTER).place(x=40,y=230)
Label(f,font=("Times",17,),text="Vanila Cake-Rs.200",fg="black",bg="beige",justify=CENTER).place(x=40,y=260)

#BILL
f2=Frame(root,bg="white",highlightbackground="black",highlightthickness=1)
f2.place(x=690,y=118,width=300,height=370)

Bill=Label(f2,text="Bill Area",font=("Times",20,"bold"),bd=7,relief=GROOVE)
Bill.pack(fill=X)
scroll_y=Scrollbar(f2,orient=VERTICAL)
txt=Text(f2,yscrollcommand=scroll_y.set) 
scroll_y.pack(side=RIGHT,fill=Y)
scroll_y.config(command=txt.yview)
txt.pack(fill=BOTH,expand=1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       


#Entry Work
f1=Frame(root,bd=5,height=370,width=300,relief=RAISED)
f1.pack()

Kaathiroll=StringVar()
Paratha=StringVar()
CholeB=StringVar()
chillipotato=StringVar()
pavbhaji=StringVar()
KHWrap=StringVar()
Vanila=StringVar()
Total_bill=StringVar()

#Label

lbl_Kaathiroll=Label(f1,font=("Times", 20, 'bold'), text="Kathi Roll", justify=CENTER, width=12,fg="Black")
lbl_Paratha=Label(f1,font=("Times", 20, 'bold'), text="Paratha", width=12,fg="black")
lbl_CholeB=Label(f1,font=("Times", 20, 'bold'), text="Chole Bhature", width=12,fg="black")
lbl_chillipotato=Label(f1,font=("Times", 20, 'bold'), text="Chilli Potato", width=12,fg="black")
lbl_pavbhaji=Label(f1,font=("Times", 20, 'bold'), text="Pav bhaji", width=12,fg="black")
lbl_KHWrap=Label(f1,font=("Times", 20, 'bold'), text="KH Wrap", width=12,fg="black")
lbl_Vanila=Label(f1,font=("Times", 20, 'bold'), text="Vanila Cake", width=12,fg="black")

lbl_Kaathiroll.grid(row=1, column=0)
lbl_Paratha.grid(row=2, column=0)
lbl_CholeB.grid(row=3, column=0)
lbl_chillipotato.grid(row=4, column=0)
lbl_pavbhaji.grid(row=5, column=0)
lbl_KHWrap.grid(row=6, column=0)
lbl_Vanila.grid(row=7, column=0)
#Entry
entry_Kaathiroll=Entry (f1, font=("Times", 20, 'bold'),justify=CENTER, textvariable=Kaathiroll,bd=6, width=8, bg="Grey")
entry_Paratha=Entry (f1, font=("Times", 20, 'bold'), justify=CENTER, textvariable=Paratha,bd=6, width=8, bg="beige")
entry_CholeB=Entry (f1, font=("Times", 20, 'bold'), justify=CENTER, textvariable=CholeB,bd=6, width=8, bg="Grey")
entry_chillipotato=Entry (f1, font=("Times", 20, 'bold'), justify=CENTER, textvariable=chillipotato,bd=6, width=8, bg="beige")
entry_pavbhaji=Entry (f1, font=("Times", 20, 'bold'), justify=CENTER,textvariable=pavbhaji,bd=6, width=8, bg="grey")
entry_KHWrap=Entry (f1, font=("Times", 20, 'bold'),justify=CENTER, textvariable=KHWrap,bd=6, width=8, bg="beige")
entry_Vanila=Entry (f1, font=("Times", 20, 'bold'),justify=CENTER, textvariable=Vanila,bd=6, width=8, bg="grey")

entry_Kaathiroll.grid(row=1, column=1)
entry_Paratha.grid(row=2, column=1)
entry_CholeB.grid(row=3, column=1)
entry_chillipotato.grid(row=4, column=1)
entry_pavbhaji.grid(row=5, column=1)
entry_KHWrap.grid(row=6, column=1)
entry_Vanila.grid(row=7, column=1)

#buttons
btn_reset=Button(f1,bd=5,fg="black",bg="lightblue",font=("Times",16,'bold'),width=10,text='Reset',command=Reset)
btn_reset.grid(row=8,column=0)

#Total buttons
btn_total=Button(f1,bd=5,fg="black",bg="lightblue",font=("Times",16,'bold'),width=9,text="Total",command=Total)
btn_total.grid(row=8,column=1)

btn_predict = Button(f1, bd=5, fg="black", bg="lightblue", font=("Times", 16, 'bold'), width=12, text="Predict", command=predict_and_display)
btn_predict.grid(row=9, column=0)

# btn_open_window2 = Button(f1, bd=5, fg="black", bg="lightblue", font=("Times", 16, 'bold'), width=12, text="Pred Demand", command=open_window2)
# btn_open_window2.grid(row=9, column=1)


#eventloop
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(conn))

root.mainloop()

