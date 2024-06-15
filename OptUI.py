import streamlit as st
from itertools import permutations
from timeit import default_timer as timer
import time

st.title("Optimasi Jadwal Makan 🗓")
st.header("Masukan Data Makanan")
st.warning("⚠ Pastikan belum mengisi manual input jika ingin menggunakan Default Data ⚠")
st.warning("⚠ Jika ingin mengganti dari Manual -> Default dan sebaliknya harap refresh terlebih dahulu ⚠")
items = []

def bruteForce2(items, budget):
    exec_start = time.time()
    maxPoint = 0
    perm = []
    best = []
    price = 0
    status ="reject"
    for i in range(0,5):
        availableToday = []
        for item in items:
            if item[4][i] != 0:
                availableToday.append(item)
        perm.append(list(permutations(availableToday, 2)))
    for day1 in perm[0]:
        for day2 in perm[1]:
            for day3 in perm[2]:
                for day4 in perm[3]:
                    for day5 in perm[4]:
                        totalPoint = day1[0][2] + day1[1][3] + day2[0][2] + day2[1][3] + day3[0][2] + day3[1][3] + day4[0][2] + day4[1][3] + day5[0][2] + day5[1][3]
                        totalPrice = day1[0][1] + day1[1][1] + day2[0][1] + day2[1][1] + day3[0][1] + day3[1][1] + day4[0][1] + day4[1][1] + day5[0][1] + day5[1][1]
                        if totalPoint > maxPoint and totalPrice <= budget:
                            maxPoint = totalPoint
                            price = totalPrice
                            best = [day1, day2, day3, day4, day5]
                            status = "accept"
    exec_end = time.time()
    exec_time = exec_end - exec_start
    return best, maxPoint, price, exec_time, status

def greedy2(items, budget):
    exec_start = time.time()
    availableAll = []
    for i in range(0,5):
        availableToday = []
        for item in items:
            if item[4][i] != 0:
                availableToday.append(item)
        availableAll.append(availableToday)
    solution = []
    price = 0
    totalPoint = 0
    for i in range(0, 5):
        day = []
        for j in range(2, 4):
            if availableAll[i]:
                maxItem = findMaxPoint(availableAll[i], j)
                if price+maxItem[1] <= budget:
                    day.append(maxItem)
                    totalPoint += maxItem[j]
                    price += maxItem[1]
                availableAll[i].remove(maxItem)
        solution.append(tuple(day))
    exec_end = time.time()
    exec_time = exec_end - exec_start
    return solution, totalPoint, price, exec_time
    print("tes")
    print(solution[4][1])

def findMaxPoint(availableItems, time):
    if not availableItems:
        return None
    maxItem = availableItems[0]
    for item in availableItems:
        if item[time] > maxItem[time]:
            maxItem = item
    return maxItem

B = st.number_input("Berapa Budget Anda ?")
int(B)
st.info("Default Data 👇")
D = st.button("Default Data")

if D:
        items = [["nasgor", 15000, 72, 85, (1, 0, 3, 0, 5)],
        ["bakso", 20000, 41, 80, (1, 2, 0, 0, 0)],
        ["sate", 22000, 36, 91, (1, 0, 0, 0, 0)],
        ["geprek", 18000, 26, 39, (1, 2, 3, 4, 5)],
        ["bubur", 15000, 81, 51, (0, 2, 0, 4, 0)],
        ["nasduk", 10000, 75, 23, (1, 2, 0, 0, 5)],
        ["tongseng", 30000, 42, 82, (0, 2, 0, 4, 5)],
        ["miayam", 18000, 54, 70, (0, 0, 3, 0, 5)]]
        

        def convert_day(value):
            # Fungsi untuk mengubah nilai menjadi deskripsi hari
            day_mapping = {1: "day 1", 2: "day 2", 3: "day 3", 4: "day 4", 5: "day 5", 0: ""}
            return day_mapping.get(value, "unknown")
        
        # Menentukan lebar kolom berdasarkan data terpanjang
        max_lengths = [max(len(str(item[i])) for item in items) for i in range(len(items[0]))]

        # Menentukan lebar untuk tuple terakhir
        tuple_index = len(items[0]) - 1
        max_lengths[tuple_index] = max(len(", ".join([convert_day(num) for num in item[tuple_index]])) for item in items)

        # Format string untuk menampilkan data
        row_format = " | ".join(["{:<" + str(length) + "}" for length in max_lengths])

        # Menampilkan header
        headers = ["Nama", "Harga", " Point Pagi", "Point Malam", " Jadwal Buka"]
        st.subheader(row_format.format(*headers))
        st.divider()

        # Menampilkan setiap item dalam items
        for item in items:
            item_copy = item[:]
            item_copy[tuple_index] = " ".join([convert_day(num) for num in item_copy[tuple_index]])  # Konversi tuple ke deskripsi hari
            st.subheader(row_format.format(*item_copy))
            st.divider()
        
st.info("Manual Input 👇")
x = st.number_input("Berapa makanan yang ingin kamu input untuk 5 hari:")


for i in range(0,int(x)):
    st.subheader(f"Data Makanan {i+1}")
    makanan = st.text_input("Nama Makanan", key=str(i)+"makan")
    harga = st.number_input("Harga Makanan:",key=str(i)+"harga")
    int(harga)
    PoinSiang = st.slider("Poin Kepuasan pagi:",key=str(i)+"siang")
    PoinMalam = st.slider("Poin Kepuasan malam:",key=str(i)+"malam")
    st.write("Jadwal Makanan yang Tersedia pada 5 hari:")
    hari1 = st.checkbox("Hari ke 1",key=str(i)+"day1")
    if hari1 == 1:
        day1 = 1
    else:
        day1 = 0

    hari2 = st.checkbox("Hari ke 2",key=str(i)+"day2")
    if hari2 == 1:
        day2 = 2
    else:
        day2 = 0
    hari3 = st.checkbox("Hari ke 3",key=str(i)+"day3")
    if hari3 == 1:
        day3 = 3
    else:
        day3 = 0
    hari4 = st.checkbox("Hari ke 4",key=str(i)+"day4")
    if hari4 == 1:
        day4 = 4
    else:
        day4 = 0
    hari5 = st.checkbox("Hari ke 5",key=str(i)+"day5")  
    if hari5 == 1:
        day5 = 5
    else:
        day5 = 0
    day = (day1, day2, day3, day4, day5)
    menu = [makanan, int(harga), PoinSiang, PoinMalam, day]
    items.append(menu)
    st.divider()

submit = st.button("Submit")
if submit:
    st.success("Data Tersimpan")
    st.divider()
    st.header("Hasil Perhitungan 🧮")
    solBF, pointBF, priceBF, execBF, stats = bruteForce2(items, B)
    solGR, pointGR, priceGR, execGR = greedy2(items, B)
    execBF_ms = execBF * 1000
    execGR_ms = execGR * 1000
    colBF, colGR = st.columns(2)
    with colBF:
        st.header("Brute Force")
        if stats == "accept":
            for i in range (0,5):
                st.subheader(f"Day {i+1}")
                st.write("Pagi Hari")
                st.write(f"Makanan: {solBF[i][0][0]}")
                st.write("Malam Hari")
                st.write(f"Makanan: {solBF[i][1][0]}")
                st.divider()
            colPBF, colPriBF = st.columns(2)
            colPBF.metric("Harga Total (Rp)", priceBF)
            colPriBF.metric("Point Kepuasan Total", pointBF)
            st.info(f"Execution time: {execBF_ms} ms")
        else:
            st.error("Tidak ditemukan solusi faktual 😔")
        

    with colGR:
        st.header("Greedy")
        for i in range (0,5):
            st.subheader(f"Day {i+1}")
            if 0 < len(solGR[i]) -1:
                st.write("Pagi Hari")
                st.write(f"Makanan: {solGR[i][0][0]}")
                st.write("Malam Hari")
                st.write(f"Makanan: {solGR[i][1][0]}")       
                st.divider()
            elif 0 <= len(solGR[i]) - 1:
                st.write("Pagi Hari")
                st.write(f"Makanan: {solGR[i][0][0]}")
                st.write("Malam Hari")
                st.write("Tidak Makan 😔")       
                st.divider()
            else:
                st.write("Tidak Makan 😔")
                st.divider()

        colPGR, colPriGR= st.columns(2)
        colPGR.metric("Harga Total (Rp)", priceGR)
        colPriGR.metric("Point Kepuasan Total", pointGR)
        st.info(f"Execution time: {execGR_ms} ms")


if D:
    st.divider()
    st.header("Hasil Perhitungan 🧮")
    solBF, pointBF, priceBF, execBF, stats = bruteForce2(items, B)
    solGR, pointGR, priceGR, execGR = greedy2(items, B)
    execBF_ms = execBF * 1000
    execGR_ms = execGR * 1000
    colBF, colGR = st.columns(2)
    with colBF:
        st.header("Brute Force")
        if stats == "accept":
            for i in range (0,5):
                st.subheader(f"Day {i+1}")
                st.write("Pagi Hari")
                st.write(f"Makanan: {solBF[i][0][0]}")
                st.write("Malam Hari")
                st.write(f"Makanan: {solBF[i][1][0]}")
                st.divider()
            colPBF, colPriBF = st.columns(2)
            colPBF.metric("Harga Total (Rp)", priceBF)
            colPriBF.metric("Point Kepuasan Total", pointBF)
            st.info(f"Execution time: {execBF_ms} ms")
        else:
            st.subheader("Tidak ditemukan solusi faktual 😔")
            st.error("Over Budget")
            colPBF, colPriBF = st.columns(2)
            colPBF.metric("Harga Total (Rp)", priceBF)
            colPriBF.metric("Point Kepuasan Total", pointBF)
            st.info(f"Execution time: {execBF_ms} ms")
        

    with colGR:
        st.header("Greedy")
        for i in range (0,5):
            st.subheader(f"Day {i+1}")
            if 0 < len(solGR[i]) -1:
                st.write("Pagi Hari")
                st.write(f"Makanan: {solGR[i][0][0]}")
                st.write("Malam Hari")
                st.write(f"Makanan: {solGR[i][1][0]}")       
                st.divider()
            elif 0 <= len(solGR[i]) - 1:
                st.write("Pagi Hari")
                st.write(f"Makanan: {solGR[i][0][0]}")
                st.write("Malam Hari")
                st.write("Tidak Makan 😔")       
                st.divider()
            else:
                st.write("Tidak Makan 😔")
                st.divider()

        colPGR, colPriGR= st.columns(2)
        colPGR.metric("Harga Total (Rp)", priceGR)
        colPriGR.metric("Point Kepuasan Total", pointGR)
        st.info(f"Execution time: {execGR_ms} ms")


    

