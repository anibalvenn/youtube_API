from json import load
from matplotlib.pyplot import title
import pandas as pd
from get_comment_dict import Comment_Dataframe


"""
pega um arquivo .json local (nesse caso, 'o_primo_rico.json'), passa por todos os vídeos elencados
nesse arquivo, e gera um dataframe com as informações 'videoId','title', 'views', 'likes', 'commentCount' de cada vídeo
params:
  arquivo .json local, que contém os dados de um canal específico no youtube
returns: 
  um dataframe com as informações 'videoId','title', 'views', 'likes', 'commentCount' de cada vídeo
"""
API_KEY = 'AIzaSyD8EloR5vSuzGeN8E9AqxVfyfShYMgNsGY'
file = 'C:\\Users\\Dell\\Documents\\Python Scripts\\venv\\05\\youtube_API\\youtube\\o_primo_rico.json'
data = None
with open(file, 'r') as f:
  data = load(f)

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
  commentCount = vid[1]['commentCount']
  comment_stats = Comment_Dataframe(API_KEY, video_id)
  df_comments = comment_stats.video_comments()#cada video gera um DF de comments
  stats.append([video_id, title, views, likes, commentCount])

# cada linha do df_videos esta relacionada a um df_comments
df_videos = pd.DataFrame(stats, columns=['videoId','title', 'views', 'likes', 'commentCount'])
print(df_videos.head(10))