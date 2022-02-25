import numpy as np
import pandas as pd
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.figure import Figure
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import webbrowser
df = pd.read_csv("data.zip",low_memory=False,dtype={'averageRating':np.float_,'numVotes':np.int_,})

db4 = df[df["numVotes"]>=1000000]
db5 = db4[db4["averageRating"]>=8]
cols = list(df.columns)
listgenres = df['genres'].tolist()
res = []
for i in listgenres:
    if i not in res:
        res.append(i)
res.remove("0")



main = ttk.Window(themename="cosmo")
main.iconbitmap("icon.ico")


w = 1900
h = 900
ws = main.winfo_screenwidth()
hs = main.winfo_screenheight()

x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

main.geometry("%dx%d+%d+%d" % (w, h, x, y))
main.title("IMDB Title Finder")

def graphic():

    figure = Figure(figsize=(7.6, 7.6), dpi=100)
    figure.text(0.5, 0.04, 'Average Rating', ha='center')
    figure.text(0.04, 0.5, "Year", ha='center', rotation='vertical')
    ax = figure.add_subplot(111)
    x = db5["averageRating"]


    annotations = list(db5["primaryTitle"])

    y = db5["startYear"]
    ax.scatter(x,y,s=6)
    for idx, row in db5.iterrows():
           ax.annotate(row['primaryTitle'], (row['averageRating'], row['startYear']),size=6)

    canvas = FigureCanvasTkAgg(figure, frame)
    canvas.draw()

    canvas.get_tk_widget().place(x=150,y=-80)

def clearFrame():
    def excel():
        cols = ["Title", "Year", "Rating", ]  # Your column headings here
        path = 'report.csv'
        excel_name = filedialog.asksaveasfilename(title='Save location', defaultextension=[('Excel', '*.xlsx')],
                                                  filetypes=[('Excel', '*.xlsx')])
        lst = []
        with open(path, "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')
            for row_id in tree.get_children():
                row = tree.item(row_id, 'values')
                lst.append(row)
            lst = list(map(list, lst))
            lst.insert(0, cols)
            for row in lst:
                csvwriter.writerow(row)

        writer = pd.ExcelWriter(excel_name)
        df = pd.read_csv(path, encoding="iso8859_9")
        df.to_excel(writer, 'sheetname')
        writer.save()
    def OnDoubleClick(event):
        item = tree.identify('item', event.x, event.y)
        url = "https://www.google.com.tr/search?q={}".format(tree.item(item, "text"))
        webbrowser.open_new_tab(url)
    for widget in frame.winfo_children():
        widget.destroy()

    if labelname.get() != "": #Search with Title
        db6 = df[df["primaryTitle"] == labelname.get()]
        figure = Figure(figsize=(7.6, 7.6), dpi=100)
        figure.text(0.5, 0.04, 'Average Rating', ha='center')
        figure.text(0.04, 0.4, "Number of Votes", ha='center', rotation='vertical')
        ax = figure.add_subplot(111)
        x = db6["averageRating"]
        y = db6["numVotes"]



        ax.scatter(x, y, s=6)

        for idx, row in db6.iterrows():
            ax.annotate(row['primaryTitle'], (row['averageRating'], row['numVotes']), size=6)

        canvas = FigureCanvasTkAgg(figure, frame)
        canvas.draw()

        canvas.get_tk_widget().place(x=150, y=-80)

        columns = ("Title", "Year", "Rating")

        tree = ttk.Treeview(frame, show="headings", columns=columns, height=35)
        tree.column("Title", width=250, anchor="n")
        tree.column("Year", width=80, anchor="n")

        tree.column("Rating", width=80, anchor="n")

        tree.heading("Title", text="Title")
        tree.heading("Year", text="Year")

        tree.heading("Rating", text="Rating")
        for _ in range(len(db6.index.values)):
            tree.insert('', 'end', value=tuple(db6.iloc[_, [3, 5, 6]].values),text=(db6.iloc[_,[3,5]].values))
        tree.place(x=1100, y=30)
        tree.bind("<Double-1>", OnDoubleClick)
        Butonexit = ttk.Button(frame, text="Excel", padding=(103, 10), bootstyle=(SUCCESS, OUTLINE), command=excel)
        Butonexit.place(x=1200, y=800)
    else:
        if genresselect.get() != "": #Genre Search
            db0 = df[df["genres"]==genresselect.get()]
            db1 = df[df["genres 2"]==genresselect.get()]
            db2 = df[df["genres 3"]==genresselect.get()]
            frames = [db0, db1, db2]
            db312 = pd.concat(frames)
            if labelpoint.get() != "":
                alabel = float(labelpoint.get())
            else:
                alabel = 0

            if labelnumvoting.get() != "":
                avote = int(labelnumvoting.get())
            else:
                avote = 10000
            if yearentry.get() != "":
                ayear = int(yearentry.get())
            else:
                ayear = 1
            if yearentry2.get() != "":
                ayear2 = int(yearentry2.get())
            else:
                ayear2 = 5000

            db5 = db312[db312["startYear"] >= ayear]
            db3 = db5[db5["startYear"] <= ayear2]
            db4 = db3[db3["numVotes"] >= avote]
            db6 = db4[db4["averageRating"] >= alabel]

            figure = Figure(figsize=(7.6, 7.6), dpi=100)
            figure.text(0.5, 0.04, 'Average Rating', ha='center')
            figure.text(0.04, 0.4, "Number of Votes", ha='center', rotation='vertical')
            ax = figure.add_subplot(111)
            x = db6["averageRating"]
            y = db6["numVotes"]
            annotations = list(db6["primaryTitle"])
            ax.scatter(x, y, s=6)

            for idx, row in db6.iterrows():
                ax.annotate(row['primaryTitle'], (row['averageRating'], row['numVotes']), size=6)

            canvas = FigureCanvasTkAgg(figure, frame)
            canvas.draw()

            canvas.get_tk_widget().place(x=150, y=-80)

            columns = ("Title", "Year", "Rating")

            tree = ttk.Treeview(frame, show="headings", columns=columns, height=35)
            tree.column("Title", width=250, anchor="n")
            tree.column("Year", width=80, anchor="n")

            tree.column("Rating", width=80, anchor="n")

            tree.heading("Title", text="Title")
            tree.heading("Year", text="Year")

            tree.heading("Rating", text="Rating")
            for _ in range(len(db6.index.values)):
                tree.insert('', 'end', value=tuple(db6.iloc[_, [3, 5, 6]].values), text = (db6.iloc[_, [3,5]].values))
            tree.place(x=1100, y=30)
            tree.bind("<Double-1>", OnDoubleClick)

            Butonexit = ttk.Button(frame, text="Excel", padding=(103, 10), bootstyle=(SUCCESS, OUTLINE), command=excel)
            Butonexit.place(x=1200, y=800)

        else:
            if labelpoint.get() != "": #Only search with year,point,vote
                alabel = float(labelpoint.get())
            else:
                alabel = 0
            if labelnumvoting.get() != "":
                avote = int(labelnumvoting.get())
            else:
                avote = 10000
            if yearentry.get() != "":
                ayear = int(yearentry.get())
            else:
                ayear = 1
            if yearentry2.get() != "":
                ayear2 = int(yearentry2.get())
            else:
                ayear2 = 5000
            db5 = df[df["startYear"] >= ayear]
            db0 = db5[db5["startYear"] <= ayear2]
            db4 = db0[db0["numVotes"] >= avote]
            db6 = db4[db4["averageRating"] >= alabel]

        figure = Figure(figsize=(7.6, 7.6), dpi=100)
        figure.text(0.5, 0.04, 'Average Rating', ha='center')
        figure.text(0.04, 0.4, "Number of Votes", ha='center',rotation='vertical')
        ax = figure.add_subplot(111)
        x = db6["averageRating"]
        y = db6["numVotes"]
        annotations = list(db6["primaryTitle"])


        ax.scatter(x, y, s=6)

        for idx, row in db6.iterrows():
            ax.annotate(row['primaryTitle'], (row['averageRating'], row['numVotes']),size=6)

        canvas = FigureCanvasTkAgg(figure, frame)
        canvas.draw()

        canvas.get_tk_widget().place(x=150, y=-80)


        columns = ("Title", "Year", "Rating")

        tree = ttk.Treeview(frame, show="headings", columns=columns, height=35)
        tree.column("Title", width=250, anchor="n")
        tree.column("Year", width=80, anchor="n")

        tree.column("Rating", width=80, anchor="n")

        tree.heading("Title", text="Title")
        tree.heading("Year", text="Year")

        tree.heading("Rating", text="Rating")
        for _ in range(len(db6.index.values)):
            tree.insert('','end',value=tuple(db6.iloc[_,[3,5,6]].values), text = (db6.iloc[_, [3,5]].values))
        tree.place(x=1100, y=30)
        tree.bind("<Double-1>", OnDoubleClick)
        Butonexit = ttk.Button(frame, text="Save as Excel", padding=(103, 10), bootstyle=(SUCCESS, OUTLINE), command=excel)
        Butonexit.place(x=1200, y=800)




def start(): #pandas dataframe i eklemek.
    def excel():
        cols = ["Title", "Year", "Rating", ]  # Your column headings here
        path = 'report.csv'
        excel_name = filedialog.asksaveasfilename(title='Save location', defaultextension=[('Excel', '*.xlsx')],
                                                  filetypes=[('Excel', '*.xlsx')])
        lst = []
        with open(path, "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')
            for row_id in tree.get_children():
                row = tree.item(row_id, 'values')
                lst.append(row)
            lst = list(map(list, lst))
            lst.insert(0, cols)
            for row in lst:
                csvwriter.writerow(row)

        writer = pd.ExcelWriter(excel_name)
        df = pd.read_csv(path, encoding="iso8859_9")
        df.to_excel(writer, 'sheetname')
        writer.save()

    columns = ("Title","Year","Rating")

    tree = ttk.Treeview(frame,show="headings",columns=columns,height=35)
    tree.column("Title",width=250,anchor="n")
    tree.column("Year",width=80, anchor="n")

    tree.column("Rating",width=80, anchor="n")

    tree.heading("Title",text="Title")
    tree.heading("Year",text="Year")

    tree.heading("Rating",text="Rating")
    for _ in range(len(db5.index.values)):
              tree.insert('','end',value=tuple(db5.iloc[_,[3,5,6]].values),text=(db5.iloc[_,[3,5]].values))
    tree.place(x=1100, y=30)

    def OnDoubleClick(event):
        item = tree.identify('item', event.x, event.y)
        url = "https://www.google.com.tr/search?q={}".format(tree.item(item, "text"))
        webbrowser.open_new_tab(url)
    tree.bind("<Double-1>", OnDoubleClick)


    Butonexcel = ttk.Button(frame, text="Save as Excel", padding=(103, 10), bootstyle=(SUCCESS, OUTLINE), command=excel)
    Butonexcel.place(x=1200, y=800)

def reset():
    labelname.delete(0, END)
    genresselect.set('')
    labelpoint.delete(0, END)
    labelnumvoting.delete(0, END)
    yearentry.delete(0, END)
    yearentry2.delete(0,END)
    start()
    graphic()

frame = ttk.Frame(main,height=2000,width=2000)
frame.place(x=300,y=10)

labelwelcome = ttk.Label(main, text="Welcome IMDB Title Finder",font=("Helvetica", 15), background="#FFFFFF")
labelwelcome.place(x=75, y=60)

#main filters
a = 151
b = 128
c = 160
d = 33.8
labelfilter = ttk.Label(main, text="Select Filter",font=("Helvetica", 14), background="#FFFFFF")
labelfilter.place(x=c-15,y=a-35)
#Year Filter
labelyear = ttk.Label(main, text="Year",font=("Helvetica", 10), background="#FFFFFF")
labelyear.place(x=c+30, y=(a + (4*d)))
yearentry = ttk.Entry(main,width=7)
yearentry.place(x=b, y=(a+(5*d)))
yearentry2 = ttk.Entry(main,width=7)
yearentry2.place(x=b+100, y=(a+(5*d)))
labelbyear = ttk.Label(main, text="-",font=("Helvetica", 10), background="#FFFFFF")
labelbyear.place(x=b+80, y=(a+(5*d)+2.5))
#Score Filter
labelpoint = ttk.Label(main, text="  IMDB Score",font=("Helvetica", 10), background="#FFFFFF")
labelpoint.place(x=c, y=(a + (2*d)))
labelpoint = ttk.Entry(main)
labelpoint.place(x=b, y=(a + (3*d)))
#Title Filter
labelname = ttk.Label(main, text="  Title Name",font=("Helvetica", 10), background="#FFFFFF")
labelname.place (x=c, y=a)
labelname = ttk.Entry(main)
labelname.place(x=b, y=(a + d))

#Genre Filter
labelgenres = ttk.Label(main, text=" Genres",font=("Helvetica", 10), background="#FFFFFF")
labelgenres.place(x=c+20, y=(a+(6*d)))
current_var = StringVar()
genresselect = ttk.Combobox(main,textvariable=current_var)
genresselect.place(x=b, y=(a+(7*d)))
genresselect['values'] = res
genresselect['state'] = 'readonly'

#Vote Filter
labelnumvoting = ttk.Label(main, text=" Number of Voting (Default value is 10,000)",font=("Helvetica", 10), background="#FFFFFF")
labelnumvoting.place(x=c-60, y=(a+(9*d)-30))
labelnumvoting = ttk.Entry(main)
labelnumvoting.place(x=b, y=(a+(10*d)-30))

#Main Buttons
Butonexit = ttk.Button(main, text="Exit", padding=(130, 10), bootstyle=(SUCCESS, OUTLINE), command=main.destroy)
Butonexit.place(x=c-70, y=(a+(14*d)))
butondelete = ttk.Button(main, text="Start Search", padding=(103, 10), bootstyle=(SUCCESS, OUTLINE), command=clearFrame)
butondelete.place(x=c-70, y=(a+(11*d)-25))
butondelete = ttk.Button(main, text="Reset Filter", padding=(103, 10), bootstyle=(SUCCESS, OUTLINE), command=reset)
butondelete.place(x=c-70, y=(a+(12*d)))
labelhowtouse = ttk.Label(main, text="How to Use?",font=("Helvetica", 10), background="#FFFFFF")
labelhowtouse.place(x=c, y=(a+(16*d)))
labelhowtouse = ttk.Label(main, text="Start Search Button: It searches by the specified \n(Title Name, Year, Genre, Number of Votes and Score.) "
                                     "\n(You can select multiple criteria in one time)"
                                     "\nReset Filter Button: Clears all search criteria"
                                     "\nSave as Excel: It saves the created table as an excel file."
                                     "\nWarning:If you write the number of votes as zero, "
                                     "\nThis will return all the results in the database. This process will also take a very long time."
                                     "\nIf you double click on the table it will google search for you"
                                     "\n Actual Database Size is " + str(df.size) + " Titles" ,font=("Helvetica", 8), background="#FFFFFF")
labelhowtouse.place(x=c-120, y=(a+(17*d)))
start()
graphic()
mainloop()


