from googleapiclient.discovery import build
import pandas as pd

def add_to_comments(reply, comments)-> list:
	reply_id = reply['id'] 
	text_reply = reply['snippet']['textDisplay']
	likes_reply = reply['snippet']['likeCount']
	author_id_reply = reply['snippet']['authorChannelId']['value'] 
	video_id__reply = reply['snippet']['videoId']
	try:
		parent_id__reply = reply['snippet']['parentId']
	except:
		parent_id__reply ='0'
	date_reply = reply['snippet']['publishedAt']
	
	comments.append([reply_id, text_reply,likes_reply, author_id_reply,video_id__reply, parent_id__reply,date_reply])

	return comments

class Comment_Dataframe:
	def __init__(self,api_key,video_id):
		self.api_key = api_key
		self.video_id = video_id
		self.comment_list = self.video_comments()


	
	def video_comments(self) -> pd.DataFrame:
		# empty list for storing reply
		comments = []

		# creating youtube resource object
		youtube = build('youtube', 'v3',
						developerKey=self.api_key)

		# retrieve youtube video results
		video_response=youtube.commentThreads().list(
		part='snippet,replies',
		videoId=self.video_id
		).execute()

		# iterate video response
		while video_response:
			for d in video_response['items']:
				item = d['snippet']['topLevelComment']				
				comments = add_to_comments(item, comments)

				if 'replies' in d:
					replies_list = d['replies']['comments']
					for reply in replies_list:
						comments = add_to_comments(reply, comments)

			# Again repeat
			if 'nextPageToken' in video_response:
				video_response = youtube.commentThreads().list(
						part = 'snippet,replies',
						videoId = self.video_id, 
						pageToken = video_response.get('nextPageToken')
					).execute()
			else:
				break
		df = pd.DataFrame( comments, columns =['id','content','likes','authorChannelId','videoId','parentId','publishedAt'])
		print(df)
		return df

video_id = 'O2FEEx3E5ss'
API_KEY = 'AIzaSyD8EloR5vSuzGeN8E9AqxVfyfShYMgNsGY'
	# Call function
comm = Comment_Dataframe(API_KEY, video_id)
# comm.video_comments()