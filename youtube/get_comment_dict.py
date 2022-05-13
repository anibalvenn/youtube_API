from googleapiclient.discovery import build
import pandas as pd

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

			
			# extracting required info
			# from each result object
			for item in video_response['items']:
				
				# Extracting comments
				comment_id = item['snippet']['topLevelComment']['id'] 
				text_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
				likes_comment = item['snippet']['topLevelComment']['snippet']['likeCount']
				author_id_comment = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'] 
				video_id__comment = item['snippet']['topLevelComment']['snippet']['videoId']
				parent_id__comment = '0'
				date_comment = item['snippet']['topLevelComment']['snippet']['publishedAt']

				comments.append([comment_id, text_comment,likes_comment, author_id_comment,video_id__comment,parent_id__comment,date_comment])

				if 'replies' in item:
					replies_list = item['replies']['comments']
					for reply in replies_list:
						reply_id = reply['id'] 
						text_reply = reply['snippet']['textDisplay']
						likes_reply = reply['snippet']['likeCount']
						author_id_reply = reply['snippet']['authorChannelId']['value'] 
						video_id__reply = reply['snippet']['videoId']
						parent_id__reply = reply['snippet']['parentId']
						date_reply = reply['snippet']['publishedAt']
						
						comments.append([reply_id, text_reply,likes_reply, author_id_reply,video_id__reply, parent_id__reply,date_reply])


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