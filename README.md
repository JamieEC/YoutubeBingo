# YoutubeBingo
Web app to play a random video from a playlist from a random point

Clone repo then 

``docker stop youtube-bingo; docker build -t python_web .; docker run -itd -p 5000:5000 --rm -e YOUTUBE_API_KEY="your_key_here" --name youtube-bingo python_web``