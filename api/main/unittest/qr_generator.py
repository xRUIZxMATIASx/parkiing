import qrcode

img = qrcode.make("hhttp://localhost:8080/?id=340")
f = open("output.png", "wb")
img.save(f)
f.close()
