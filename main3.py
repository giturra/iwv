from streamdataloader.streamdataloader import TweetStreamLoader

fn = "C:/Users/gabri/Desktop/biwv/biwv/proccess_tweets.txt"
bat_size = 256 
buff_size = 2048  # a multiple of bat_size
emp_ldr = TweetStreamLoader(fn, bat_size, buff_size, shuffle=False) 

for (b_idx, batch) in enumerate(emp_ldr):
    print(batch)
emp_ldr.fin.close()