from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status

from crawl.user_crawl import start_user_crawl
from testconn.feat_db_conn import engine_user_db_conn, engine_feat_db_conn
from testconn.models import keywordTable, rawInfoTable, processedInfoTable

router = APIRouter()

feat_engine = engine_feat_db_conn()
feat_session = feat_engine.sessionmaker()

user_engine = engine_user_db_conn()
user_session = user_engine.sessionmaker()

@router.get("/detail/{influencer_id}", tags=["detail"])
async def get_detailed_info(influencer_id: str):

    target_influencer = feat_session.query(
        rawInfoTable.Keyword_Username,
        rawInfoTable.Followers,
        rawInfoTable.Avg_Likes,
        processedInfoTable.Real_Followers,
        processedInfoTable.Real_Like_Rate,
        processedInfoTable.Real_Comment_Rate,
        processedInfoTable.Real_Influence).outerjoin(processedInfoTable,
                                                     processedInfoTable.RawInfo_Keyword_Username
                                                     == rawInfoTable.Keyword_Username
                                                     ).filter(rawInfoTable.Keyword_Username
                                                              == influencer_id).first()
    if not target_influencer:
        raise HTTPException(status_code=202, detail="No influencer named "+influencer_id+".")

    return jsonable_encoder(target_influencer)

