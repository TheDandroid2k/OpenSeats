import requests, csv
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk


def getSeats(*args):
    term = semester.get()
    crn = course.get()
    
    html = requests.get(f"https://ssbprod.atu.edu/pls/PROD/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}").text
    
    """html=
    	<table class="datadisplaytable" summary="This layout table is used to present the seating numbers." width="100%">
    		<caption class="captiontext">Registration Availability</caption>
    		<tbody>
    			<tr>
    				<td class="dddead">&nbsp;</td>
    				<th class="ddheader" scope="col"><span class="fieldlabeltext">Capacity</span></th>
    				<th class="ddheader" scope="col"><span class="fieldlabeltext">Actual</span></th>
    				<th class="ddheader" scope="col"><span class="fieldlabeltext">Remaining</span></th>
    			</tr>
    			<tr>
    				<th class="ddlabel" scope="row" style="background: none; color: rgb(0, 0, 0);"><span class="fieldlabeltext">Seats</span></th>
    				<td class="dddefault">20</td>
    				<td class="dddefault">15</td>
    				<td class="dddefault">5</td>
    			</tr>
    		</tbody>
    	</table>
    	"""
    
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", attrs={"summary":"This layout table is used to present the seating numbers."})
    if table is None:
        seatsRemaining = "Wrong term/CRN"
    else:
        td_list = table.findAll("td")
        seatsRemaining = td_list[3].text
    seats.set(seatsRemaining)

def addEmail(*args):
    mail = email.get()
    term = semester.get()
    crn = course.get()

    with open('input.csv', 'a', newline='') as file:
        write = csv.writer(file)
        write.writerow([term, crn, mail])
    confirm.set("You have been added to the list!\nYou will receive a confirmation e-mail soon.")

root = Tk()
root.title("Remaining Seats")

mainframe = ttk.Frame(root, padding="20 20")
mainframe.grid(column=0, row=0)

semester = StringVar()
course = StringVar()
seats = StringVar()
email = StringVar()
confirm = StringVar()

ttk.Label(mainframe, text="Enter Term:").grid(row=1, column=1, sticky=E)
ttk.Label(mainframe, text="Enter CRN:").grid(row=2, column=1, sticky=E)
semesterEntry = ttk.Entry(mainframe, textvariable=semester).grid(row=1, column=2)
courseEntry = ttk.Entry(mainframe, textvariable=course).grid(row=2, column=2)
ttk.Label(mainframe, text="Remaining Seats:").grid(row=3, column=1)
ttk.Label(mainframe, textvariable=seats).grid(row=3, column=2)
ttk.Button(mainframe, text="Show me the seats!", command=getSeats).grid(row=4, column=2)
ttk.Label(mainframe, text="E-mail me when seats are open:").grid(row=5, column=1, columnspan=2, sticky=W+S)
emailEntry = ttk.Entry(mainframe, textvariable=email).grid(row=6, column=1, columnspan=2, sticky=W)
ttk.Button(mainframe, text="Add e-mail", command=addEmail).grid(row=6, column=2, sticky=E)
ttk.Label(mainframe, textvariable=confirm).grid(row=7, column=1, columnspan=2, sticky=W)

root.mainloop()