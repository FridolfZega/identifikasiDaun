import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk

def cek_kesehatan_daun_histogram(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return "Gagal membaca gambar."

    # Ubah ke HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Range warna hijau (Hue 35–85 derajat)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Mask total daun (kuning sampai hijau)
    lower_leaf = np.array([15, 30, 30])
    upper_leaf = np.array([100, 255, 255])
    mask_leaf = cv2.inRange(hsv, lower_leaf, upper_leaf)

    total_pixel = np.count_nonzero(mask_leaf)
    if total_pixel == 0:
        status = "Tidak ada area daun yang terdeteksi."
        print("Hasil deteksi:", status)
        return status

    green_pixel = np.count_nonzero(mask_green)
    persentase_hijau = (green_pixel / total_pixel * 100)

    if persentase_hijau > 90:
        status = f"Sehat ({persentase_hijau:.2f}% hijau)"
    else:
        status = f"Tidak Sehat (hijau hanya {persentase_hijau:.2f}%)"

    print("Hasil deteksi:", status)

    # Tampilkan gambar asli
    cv2.imshow("Gambar Asli", img)

    # --- Plot histogram HSV ---
    plt.figure(figsize=(10,6))
    colors = ['r','g','b']
    labels = ['Hue','Saturation','Value']

    for i, col in enumerate(colors):
        bins = 180 if i == 0 else 256
        range_vals = [0,180] if i == 0 else [0,256]
        hist = cv2.calcHist([hsv], [i], mask_leaf, [bins], range_vals)
        plt.plot(hist, color=col, label=labels[i])

    plt.title("Histogram HSV Daun")
    plt.xlabel("Nilai Channel")
    plt.ylabel("Jumlah piksel")
    plt.legend()

    # Tambahkan penjelasan warna pada sumbu Hue (0–180)
    ax = plt.gca()
    hue_colors = [
        (0, 'Merah'),
        (20, 'Oranye'),
        (30, 'Kuning'),
        (60, 'Hijau'),
        (100, 'Biru'),
        (140, 'Ungu'),
        (180, 'Merah')
    ]
    for h, nama in hue_colors:
        ax.axvline(x=h, color='k', linestyle='--', alpha=0.4)
        ax.text(h, ax.get_ylim()[1]*0.9, nama, rotation=90,
                verticalalignment='top', fontsize=8)

    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return status

if __name__ == "__main__":
    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Pilih gambar daun",
        filetypes=[("Image files", "*.jpg *.png *.jpeg")]
    )
    if file_path:
        cek_kesehatan_daun_histogram(file_path)
    else:
        print("Tidak ada file yang dipilih.")

#Program ini digunakan untuk mendeteksi kesehatan daun berdasarkan warna dominan dengan metode analisis citra menggunakan OpenCV dan matplotlib.
# Daun dianggap sehat jika mayoritas areanya berwarna hijau, dan dianggap tidak sehat jika terdapat dominasi warna lain (kuning, oranye, coklat).
# Selain memberikan status, program juga menampilkan histogram HSV (Hue, Saturation, Value) untuk menunjukkan distribusi warna pada area daun.
