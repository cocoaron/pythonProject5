from pydantic import BaseModel, Field

class keyword(BaseModel):
    Keyword: str
    Username: str

class processedInfo(BaseModel):
    RawInfo_Keyword_Username: str
    Real_Followers: int
    Real_Like_Rate: float
    Real_Comment_Rate: float
    Real_Influence: float

class rawInfo(BaseModel):
    Keyword_Username: str
    Followers: int
    Avg_Likes: float

class attention(BaseModel):
    # target table name inside the accessed db
    influencer_id: str
    followers: int
    real_influnce: int

class Settings(BaseModel):
    authjwt_secret_key:str='b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'
