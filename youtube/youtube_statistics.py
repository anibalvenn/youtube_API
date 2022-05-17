from requests import get
from json import loads, dump
from tqdm import tqdm

class YTstats:
  def __init__(self,api_key,channel_id):
    self.api_key = api_key
    self.channel_id = channel_id
    self.channel_statistics = None
    self.video_data = None 


  def get_channel_statistics(self):
    """
    Pega as estatísticas do canal e preenche
    videoCount, subscriberCount, viewCount, etc.    
    returns:
      dict: data, contendo as estatísticas do canal, organizadas por videoId
    """
    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
    print(url)
    json_url = get(url)
    data = loads(json_url.text)
    print(data)
    try:
      data = data["items"][0]["statistics"]
    except:
      data = None
    
    self.channel_statistics = data
    return data  

  def get_channel_video_data(self):
    # get videos IDs
    channel_videos = self._get_channel_videos(limit=5)
    # get videos statistics
    parts = ["snippet", "statistics", "contentDetails"]
    for video_id in tqdm(channel_videos):
      for part in parts:
        data = self._get_single_video_data(video_id,part)
        channel_videos[video_id].update(data)

    self.video_data = channel_videos
    return channel_videos

  def _get_single_video_data(self, video_id, part):
    """
    agrega os dados de um unico video, retirados a API do youtube
    returns:
      dict: data - os dados de um unico video, chaveados pelo id
    """
    url = f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}'
    json_url = get(url)
    data= loads(json_url.text)
    try:
      data = data['items'][0][part]
    except:
      print('Error')
      data = dict()

    return data

  def _get_channel_videos(self, limit=None):  
    """
    produz um dicionário com todos os videos do canal, caso não seja estabelecido um limite
    params:
      int: limit - o limite de videos do canal a serem acrescido no dicionario que sera retornado
    returns:
      dict: vid
    """
    url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date"

    print(url)

    if limit is not None and isinstance(limit, int):
      url +="&maxResults=" + str(limit)
    
    vid, npt = self._get_channel_videos_per_page(url)
    idx = 0
    while(npt is not None and idx < 5):
      nextUrl = url + "&pageToken=" + npt
      next_vid, npt = self._get_channel_videos_per_page(nextUrl)
      vid.update(next_vid)
      idx += 1

    return vid

  def _get_channel_videos_per_page(self, url):
    """
    pega todos os videos de uma mesma pagina na APi do youtube
    returns:
      str: nextPageToken
      dict: channel_videos
    """
    json_url = get(url)
    data = loads(json_url.text)
    channel_videos = dict()
    if 'items' not in data:
      return channel_videos, None

    item_data = data['items']
    nextPageToken = data.get("nextPageToken", None)
    for item in item_data:
      try:
        kind = item['id']['kind']
        if kind == 'youtube#video':
          video_id = item['id']['videoId']
          channel_videos[video_id] = dict()
      except KeyError:
        print("error")

    return channel_videos, nextPageToken

  def dump(self):
    """
    cria o arquivo .json com as estatísticas do canal do youtube de onde os dados foram retirados,
    no mesmo diretório onde este arquivo estiver situado
    """
    if self.channel_statistics is None or  self.video_data is None:
      print("data is None")
      return

    fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics, "video_data": self.video_data}}


    channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
    channel_title = channel_title.replace(" ", "_").lower()
    file_name = channel_title + ".json"
    with open(file_name, 'w') as f:
      dump(fused_data, f, indent=4)
    print("file dumped")