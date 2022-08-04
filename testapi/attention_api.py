from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status

from testconn.feat_db_conn import engine_user_db_conn, engine_feat_db_conn
from testconn.models import attentionTable, keywordTable, rawInfoTable, processedInfoTable

router = APIRouter(
    prefix="/attention",
    tags=['attention']
)

feat_engine = engine_feat_db_conn()
feat_session = feat_engine.sessionmaker()

user_engine = engine_user_db_conn()
user_session = user_engine.sessionmaker()


@router.get("/")
async def read_attention_list():

    attention_list = user_session.query(attentionTable).limit(100).all()

    return jsonable_encoder(attention_list)


@router.post("/{influencer_id}", status_code=status.HTTP_201_CREATED)
async def add_to_attention_list(influencer_id: str):

    influencer = feat_session.query(
        keywordTable.Username,
        rawInfoTable.Followers,
        processedInfoTable.Real_Influence
    ).outerjoin(
        rawInfoTable,
        keywordTable.Username == rawInfoTable.Keyword_Username
    ).outerjoin(
        processedInfoTable,
        keywordTable.Username == processedInfoTable.RawInfo_Keyword_Username
    ).filter(keywordTable.Username == influencer_id).first()

    add_influencer = attentionTable(
        influencer_id=influencer.Username,
        followers=influencer.Followers,
        real_influence=influencer.Real_Influence
    )

    check_influencer = user_session.get(attentionTable, add_influencer.influencer_id)

    if check_influencer:
        raise HTTPException(status_code=404, detail="Already added.")

    user_session.add(add_influencer)

    try:
        user_session.commit()
    except:
        user_session.rollback()

    response = {
        "influencer_id": add_influencer.influencer_id,
        "followers": add_influencer.followers,
        "real_influence": add_influencer.real_influence
    }

    return jsonable_encoder(response)


@router.delete("/delete/{influencer_id}")
async def delete_user(id: str):

    influencer_to_delete = user_session.get(attentionTable, id)

    if not influencer_to_delete:
        raise HTTPException(status_code=404, detail="Influencer not found")

    user_session.delete(influencer_to_delete)

    try:
        user_session.commit()
    except:
        user_session.rollback()

    return {"ok": True}
'''
    influencer_to_delete = user_session.query(attentionTable)\
        .filter(attentionTable.influencer_id == id).first()



    user_session.delete(influencer_to_delete)

    try:
        user_session.commit()
    except:
        user_session.rollback()
        raise HTTPException(status_code=404, detail="Username not found.")

    return influencer_to_delete
'''