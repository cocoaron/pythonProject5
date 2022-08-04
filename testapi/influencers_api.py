from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from starlette import status

from crawl.user_crawl import start_user_crawl
from testconn.feat_db_conn import engine_user_db_conn, engine_feat_db_conn
from testconn.models import attentionTable, keywordTable, rawInfoTable, processedInfoTable

router = APIRouter(
    prefix="/influencers",
    tags=['influencers']
)

feat_engine = engine_feat_db_conn()
feat_session = feat_engine.sessionmaker()

user_engine = engine_user_db_conn()
user_session = user_engine.sessionmaker()

#리스트 랭킹
@router.get("/ranking")
async def get_ranking(* ,
                  keyword: Optional[str] = None,
                      category: Optional[str] = Query(default="", enum=["캠핑", "골프", "조명"]),
                  choice: str = Query(
                      default="all",
                      enum=["all", "nano", "micro", "mid", "macro", "mega"]
                  )):

    all_filters = [rawInfoTable.Followers > 0]

    if choice == "nano":
        all_filters.append(rawInfoTable.Followers < 10000)
        all_filters.append(rawInfoTable.Followers >= 1000)
    if choice == "micro":
        all_filters.append(rawInfoTable.Followers < 50000)
        all_filters.append(rawInfoTable.Followers >= 10000)
    if choice == "mid":
        all_filters.append(rawInfoTable.Followers < 100000)
        all_filters.append(rawInfoTable.Followers >= 50000)
    if choice == "macro":
        all_filters.append(rawInfoTable.Followers < 500000)
        all_filters.append(rawInfoTable.Followers >= 100000)
    if choice == "mega":
        all_filters.append(rawInfoTable.Followers >= 500000)

    if category:
        all_filters.append(keywordTable.Keyword.like('%' + category + '%'))

    if keyword:
        all_filters.append(keywordTable.Keyword.like('%' + keyword + '%'))


    influencers = feat_session.query(
        func.rank().over(order_by=processedInfoTable.Real_Influence.desc()).label('rank'),
        keywordTable.Username,
        keywordTable.Keyword,
        rawInfoTable.Followers,
        processedInfoTable.Real_Influence
    ).outerjoin(
        rawInfoTable,
        keywordTable.Username == rawInfoTable.Keyword_Username
    ).outerjoin(
        processedInfoTable,
        keywordTable.Username == processedInfoTable.RawInfo_Keyword_Username
    ).filter(*all_filters).limit(100).all()

    check_error = []

    if not influencers:
        # if keyword and category:
        #    all_filters.pop()

        #     check = feat_session.query(keywordTable).filter(
        #        all_filters.append(keywordTable.Keyword.like('%' + category + '%'))).all()

        #    if check:
        #        check_error.append("no data in this keyword. ")
        #    else:
        #        check_error.append("no data in this category. ")
        #else:
        #    check_error.append("no data in this level of influencer. ")

        raise HTTPException(status_code=202, detail="no data")

    return jsonable_encoder(influencers)

@router.get("/{influencer_id}")
async def get_influencer_rank(influencer_id: str):

    target_influencer = feat_session.query(
        rawInfoTable.Keyword_Username,
        rawInfoTable.Followers,
        processedInfoTable.Real_Influence
    ).outerjoin(
        processedInfoTable,
        rawInfoTable.Keyword_Username == processedInfoTable.RawInfo_Keyword_Username
    ).filter(rawInfoTable.Keyword_Username == influencer_id).first()

    influencer_list = feat_session.query(
        rawInfoTable.Keyword_Username,
        rawInfoTable.Followers,
        processedInfoTable.Real_Influence
    ).outerjoin(
        processedInfoTable,
        rawInfoTable.Keyword_Username == processedInfoTable.RawInfo_Keyword_Username
    ).order_by(processedInfoTable.Real_Influence.desc()).limit(100).all()

    influencer_rank = []

    # for influencer in influencer_list:
        #if():
        #    influencer_rank = influencer_list
        #    break

    return jsonable_encoder(influencer_list)
