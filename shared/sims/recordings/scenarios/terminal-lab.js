// Terminal Lab: ipconfig and ping in the office, then the café, then the hotel.
await wait(800); TL.run("ipconfig"); await wait(1500); TL.run("ping play.example.net"); await wait(1800);
TL.place("Café (far from the Wi-Fi)"); await wait(700); TL.run("ping 192.168.8.1"); await wait(1900);
TL.place("Hotel (name problem)"); await wait(700); TL.run("nslookup play.example.net"); await wait(1300); TL.run("ping 198.51.100.7"); await wait(1900);
