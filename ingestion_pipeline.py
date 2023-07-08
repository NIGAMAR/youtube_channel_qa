from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from googleapiclient.discovery import build
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled, YouTubeTranscriptApi
import constants as const
import os

load_dotenv()


class IngetionPipeline:
    """
    A class that consumes the YouTube channel name 
    Genrerates transcript for that channel 
    Loads up the knowledge base with the channel content 
    """
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    openai_key = os.getenv("OPENAI_API_KEY")
    video_id_list = []
    not_cached_video_id_list = []
    full_transcript: str = ""
    channel_id: str

    # get the channel id for a specified channel
    # if the channel is not found or invalid raise a value error
    def _fetch_channel_id(self, channel_name: str):
        print(f"Fetching channel id for {channel_name}....")
        response = self.youtube.search().list(
            part='snippet',
            q=channel_name,
            type='channel'
        ).execute()
        items = response['items']
        if len(items) == 0:
            self.channel_id = const.invalid_channel_d
        else:
            self.channel_id = items[0]['id']['channelId']

    # get all the videos for the channel
    def _get_channel_videos(self):
        print("Getting channel videos...")
        next_page_token = None
        while True:
            response = self.youtube.search().list(
                part=['snippet', 'id'],
                channelId=self.channel_id,
                maxResults=25,  # Adjust this value as per your requirement
                pageToken=next_page_token,
                type='video'
            ).execute()

            # Extract video IDs
            for item in response['items']:
                videoId = item['id']['videoId']
                self.video_id_list.append(videoId)

            # Check if there are more pages to fetch
            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

    # get channel transcript
    def _get_video_transcript(self, video_id: str) -> str:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(
                video_id=video_id)
        except TranscriptsDisabled:
            self.not_cached_video_id_list.append(video_id)
            return " "
        try:
            en_transcript = transcript_list.find_transcript(['en'])
            transcript = en_transcript.translate('en')
            transcript_pieces = transcript.fetch()
            transcript = " ".join([t['text'].strip(" ")
                                  for t in transcript_pieces])
            return transcript
        except NoTranscriptFound:
            self.not_cached_video_id_list.append(video_id)
            return " "

    # split transcript into chunks

    def _split_transcript_into_chunks(self):
        print(f"Splitting transcript into chunks....")
        text_splitter = RecursiveCharacterTextSplitter()
        text_splitter._chunk_size = const.doc_chunk_size
        text_splitter._chunk_overlap = const.doc_chunk_overlap
        chunks = text_splitter.split_text(text=self.full_transcript)
        return chunks

    def _get_embeddings(self):
        return HuggingFaceEmbeddings(
            model_name=const.embedding_model)

    # create a knowlege base to perform similarity search

    def _create_knowledge_base(self, data, embeddings):
        kb = FAISS.from_texts(
            texts=data,
            embedding=embeddings
        )
        kb.save_local(folder_path=const.kb_folder_path,
                      index_name=self.channel_id)
        print(f"Knowledge Base created")

    # get the knowledge base from the ingestion pipeline

    def get_knowlege_base(self) -> FAISS:
        embedding = self._get_embeddings()
        return FAISS.load_local(folder_path=const.kb_folder_path, index_name=self.channel_id, embeddings=embedding)

    # run the ingestion pipeline to cache the data source
    def run(self, channel_name: str):
        # get the channel id for the channel
        self._fetch_channel_id(channel_name)
        if self.channel_id == const.invalid_channel_d:
            raise ValueError
        print(f"channel id is {self.channel_id}")
        self._get_channel_videos()
        print(f"Total videos in channel {len(self.video_id_list)}")
        print(f"Fetching transcript for all videos....")
        for video_id in self.video_id_list:
            video_transcript = self._get_video_transcript(
                video_id=video_id)
            if video_transcript != " ":
                self.full_transcript = self.full_transcript + video_transcript + "\n"
        print(
            f"Fetched video transcript for videos except {len(self.not_cached_video_id_list)}")
        chunks = self._split_transcript_into_chunks()
        print(f"Number of chunks in transcript {len(chunks)}")
        embeddings = self._get_embeddings()
        self._create_knowledge_base(
            data=chunks,
            embeddings=embeddings
        )
