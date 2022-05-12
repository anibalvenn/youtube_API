from googleapiclient.discovery import build

class Comment_List:
	def __init__(self,api_key,video_id):
		self.api_key = api_key
		self.video_id = video_id
		self.comment_list = self.video_comments()




	def video_comments(self) -> list[str]:
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
				comment = item['snippet']['topLevelComment']['snippet']['textDisplay']    
				comments.append(comment)


			# Again repeat
			if 'nextPageToken' in video_response:
				video_response = youtube.commentThreads().list(
						part = 'snippet,replies',
						videoId = self.video_id, 
						pageToken = video_response.get('nextPageToken')
					).execute()
			else:
				break
		return comments


	# Call function
	# video_comments(video_id)