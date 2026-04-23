- [Playwright](https://playwright.dev/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/en/latest/index.html)
- [lxml.html](https://lxml.de/lxmlhtml.html)

# Running
```
./main | ffmpeg -y -framerate 10 -f image2pipe -vcodec pam -i - -vf "scale=iw*4:ih*4:flags=neighbor" -c:v libx265 -preset medium -crf 23 -pix_fmt yuv420p10le swarm_sim.mp4
```
