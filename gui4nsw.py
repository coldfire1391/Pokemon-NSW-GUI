import tkinter as tk
import tkinter.scrolledtext as st

# from st_team_gen
import random
import numpy as np
import pandas as pd

# number to type <array>
NTT = ["normal","fighting","flying","poison","ground","rock","bug","ghost","steel","fire","water","grass","electric","psychic","ice","dragon","dark","fairy"]

# type to number <dictionary>
TTN = {"normal":0, "fighting":1, "flying":2, "poison":3, "ground":4, "rock":5, "bug":6, "ghost":7, "steel":8, "fire":9, "water":10, "grass":11, "electric":12, "psychic":13, "ice":14, "dragon":15, "dark":16, "fairy":17}

# Shared Weakness Matrix
SWM = pd.read_csv("SWM.csv").to_numpy()

# from st_team_gen
# ccz: c-something check
# swm: shared weakness matrix, fmem: final members list, x: x-coord, y: y-coord
def ccz(swm, fmem, x, y):
	if x == 1:
		return swm[fmem[x]][fmem[0]]
	elif y == -1:
		return ccz(swm, fmem, x-1, x-2)
	else:
		return (swm[fmem[x]][fmem[y]] | ccz(swm, fmem, x, y-1))

# from st_team_gen
# swm: shared weakness matrix, pmem: potential members, lenm: length of matrix, ts: team size, fmemlist(output): final members list 
def powerset(swm, pmem, lenm, ts, fmemlist):
	x = len(pmem)
	for i in range(1 << x):
		Fmem = [pmem[j] for j in range(x) if (i & (1 << j))]
		if len(Fmem) == (int(ts)-int(lenm)) and not ccz(swm,Fmem,len(Fmem)-1,len(Fmem)-2):
				fmemlist.append(Fmem)
	return

# get a list of types whose check buttons were ticked
# l: list, ntt: number to type
def getCzButtons(l,ntt):
	a = len(l)
	return [ntt[x] for x in range(a) if l[x].get() == 1]

# transforms items in a list to text
# l: list
def list_to_text(l):
	text = ""
	for x in l:
		text+=(x + "\n")
	return text

# disable all check buttons if currently unchecked
# cbl: check button list, tcl: Types_chosen list
def disable_all(cbl,tcl):
	for x in range(18):
		if tcl[x].get() == 0:
			cbl[x].config(state="disabled")
	return

# active all check buttons
# cbl: check button list
def active_all(cbl):
	for x in range(18):
		cbl[x].config(state="normal")
	return

# checks if the number of ticked check boxes has reaches/gone over (the desires team size - 2). Disables them if so, activates them if not
# n: spinbox number, cbl: check button list, tcl: Types_chosen list
def check_limit(n,cbl,tcl,ntt):
	# Types_chosen list length
	tcl_len = len(getCzButtons(tcl,ntt))
	if tcl_len >= int(n)-2:
		disable_all(cbl,tcl)
	else:
		active_all(cbl)
	return

# Display text window with all generated teams
# stw: scrolled text object, n: spinbox number, cbl: check button list, ntt: number to text, ttn: text to number, swm: shared weakness matrix
def Team_Gen(stw,n,cbl,ntt,ttn,swm):
	# clear ScrolledText text (widget must be NORMAL to delete anything)
	stw.config(state="normal")
	stw.delete(1.0, tk.END)

	# obtain list of mandatory types (represented by numbers)
	Mtypes = sorted([ttn[t] for t in cbl])

	# obtain length of Mtypes
	len_m = len(cbl)

	# extend length of Mtypes to 6
	while len(Mtypes) < 6:
		Mtypes.append(Mtypes[0])

	# potential members <array>
	Pmem = [p for p in range(0,18) if (swm[Mtypes[0]][p] | swm[Mtypes[1]][p] | swm[Mtypes[2]][p] | swm[Mtypes[3]][p] | swm[Mtypes[4]][p] | swm[Mtypes[5]][p] == 0)] # or p == mtype

	# Final members list
	FmemList = []

	# develops output to FmemList
	powerset(swm, Pmem, len_m, n, FmemList)

	# turns each list from powerset into a newline string elements, 
	final_output = [str([ntt[z] for z in w])+"\n" for w in FmemList]

	final_text = list_to_text(final_output)

	# inserts final_text to ScrolledText widget
	stw.insert(tk.INSERT,final_text)

	# to make the scrolltext readonly
	stw.configure(state='disabled')

def main():
	# parent window
	pw = tk.Tk()

	# Spinbox vars
	spinbox1 = tk.IntVar()

	# CheckButton vars
	Types_chosen = [None]*18
	for i in range(18):
		Types_chosen[i] = tk.IntVar()

	# CheckButtons list
	Cbl = []

	pw.title('Team Parameters')
	# pw.geometry("600x300")
	# pw['bg'] = "#d1f4ff"

	# Labels
	tk.Label(pw, text="Team Size").grid(row=0)
	tk.Label(pw, text="Initial Types").grid(row=1, columnspan=2)

	# SpinBox
	spinbox1 = tk.Spinbox(pw, from_=0, to=6, command=lambda: check_limit(spinbox1.get(),Cbl,Types_chosen,NTT))
	spinbox1.grid(row=0, column=1)

	# CheckButtons
	# places a 9x2 matrix of pokemon types on the grid
	for x in range(18):
		Cbl.append(tk.Checkbutton(pw, text=NTT[x], variable=Types_chosen[x], state="disabled", command=lambda: check_limit(spinbox1.get(),Cbl,Types_chosen,NTT)))
		Cbl[-1].grid(row=((x % 9)+2), column=int(x/9), sticky="W")
	# , bg="#d1f4ff", activebackground="#d1f4ff"

	# ScrolledText
	scrolltxt1 = st.ScrolledText(pw, bg='white', font='TkFixedFont', state="disabled")
	scrolltxt1.grid(row=0, column=2, rowspan=12)

	# buttons
	button1 = tk.Button(pw, text="Generate Teams", width=25, command=lambda: Team_Gen(scrolltxt1,spinbox1.get(),getCzButtons(Types_chosen,NTT),NTT,TTN,SWM)).grid(row=11, columnspan=2)

	pw.mainloop()

main()