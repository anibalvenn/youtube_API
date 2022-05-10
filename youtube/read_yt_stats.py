import json
from matplotlib.pyplot import title
import pandas as pd

file = 'o_primo_rico.json'
data = None
with open(file, 'r') as f:
  data = json.load(f)

channel_id, stats = data.popitem()
print(channel_id)
channel_stats = stats['channel_statistics']
video_stats = stats['video_data']

# channel statistics
print('views', channel_stats['viewCount'])
print('subscribers', channel_stats['subscriberCount'])
print('videos', channel_stats['videoCount'])

# video channel_statistics
sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1]['viewCount']), reverse=True)

stats =[]
for vid in sorted_vids:
  video_id = vid[0]
  title = vid[1]['title']
  likes = vid[1]['likeCount']
  views = vid[1]['viewCount']
  comments = vid[1]['commentCount']
  stats.append([title, views, likes, comments])

df = pd.DataFrame(stats, columns=['title', 'views', 'likes', 'comments'])
print(df.head(10))