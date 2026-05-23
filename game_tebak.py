# Import library random buat generate angka rahasia
import random

# Generate angka rahasia antara 1-10
angka_rahasia = random.randint(1, 10)
tebakan = 0
nyawa = 3  # Batas salah 3x

print("🔥 GAME TEBAK ANGKA 1-10 🔥")
print("Kamu punya 3 nyawa. Amatilah!")

while tebakan != angka_rahasia and nyawa > 0:
    # Input user, langsung jadi integer
    tebakan = int(input("Tebak angka: "))

    if tebakan < angka_rahasia:
        print("📉 Kecil banget! Nyawa -1")
        nyawa -= 1
    elif tebakan > angka_rahasia:
        print("📈 Gede banget! Nyawa -1")
        nyawa -= 1
    else:
        print(f"🎉 BENAR! Angka rahasia: {angka_rahasia}")
        break  # Keluar dari loop kalo benar

    print(f"Nyawa tersisa: {nyawa}")

if nyawa == 0:
    print(f"💀 Game Over! Angkanya {angka_rahasia}")