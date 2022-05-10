from youtube_statistics import YTstats

API_KEY= "" #string de chave API: cada um tem a sua
channel_id = "UCT4nDeU5pv1XIGySbSK-GgA"
# channel_id = "UChjz-RXIVICrH0SYvtVNwHA"


yt= YTstats(API_KEY, channel_id)
yt.get_channel_statistics()
yt.get_channel_video_data()
yt.dump()