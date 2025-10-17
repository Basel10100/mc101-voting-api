# from api.users.UserDBModels import UserDBModel, get_user_by_email, add_user
from typing import List
from fastapi import APIRouter, status, HTTPException, Request, Depends
from sqlalchemy import func 
from utils.constants import Endpoints, ResponseMessages
from utils.security import create_access_token, decode_access_token, hash_password, verify_password, oauth2_scheme
from .UserSchemas import (CandidateSchema, UserLoginResponseSchema, 
                          UserRegisterResponseSchema, UserSchema, 
                          UserLoginSchema, UserUpdateSchema, VoteResponseSchema, VotingSchema, VoteCountResponseSchema, PasswordChangeSchema) 
from db.DBModels import CandidateDBModel, UserDBModel, VoteDBModel, NoteDBModel, TokenBlacklist
from db.DbConfig import get_db 
from utils.crypto_notes import encrypt_note, decrypt_note
from pydantic import SecretStr
from datetime import datetime, timezone
from .NoteSchemas import NoteCreateSchema, NoteUpdateSchema, NoteResponseSchema

UserRouter = APIRouter(prefix="/users", tags=["Users"])

@UserRouter.post(Endpoints.REGISTER,
                 status_code=status.HTTP_201_CREATED,
                 response_model=UserRegisterResponseSchema)
def create_user(user: UserSchema, db=Depends(get_db)):
    # check the user exists
    existing_user = db.query(UserDBModel).filter(UserDBModel.email == user.email).first()
    if existing_user:
        raise HTTPException(detail=ResponseMessages.USER_ALREADY_EXISTS,
                            status_code=status.HTTP_400_BAD_REQUEST) 
    new_user = UserDBModel(**user.model_dump(exclude={"password"}),
                           hashed_password=hash_password(user.password))
    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(detail="The candidate already exists!", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    db.refresh(new_user)  # Refresh the instance to get the updated data from the DB
    # We have set the response_model to UserRegisterResponseSchema, so FastAPI will automatically
    # filter out the hashed_password field from the response and return only the fields defined in the schema.
    # Pydantic and sqlalchemy integration handles this seamlessly.
    # The difference between returning a dict and a pydantic model is that the pydantic model provides
    # validation, serialization, and documentation benefits.
    return new_user


# Login endpoint
@UserRouter.post(Endpoints.LOGIN,
                 status_code=status.HTTP_200_OK,
                 response_model=UserLoginResponseSchema)
def login_user(user: UserLoginSchema, db=Depends(get_db)):
    # Check user exists
    existing_user = db.query(UserDBModel).filter(UserDBModel.email == user.email).first()
    if not existing_user:
        raise HTTPException(detail=ResponseMessages.USER_NOT_FOUND,
                            status_code=status.HTTP_404_NOT_FOUND)
    # Verify password
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(detail=ResponseMessages.INVALID_PASSWORD,
                            status_code=status.HTTP_401_UNAUTHORIZED)
    # Generate JWT token
    payload = {
        "user_id": str(existing_user.id),
        "email": existing_user.email
    }
    token = create_access_token(data=payload)
    # Return the token in the response with the authentication type using the pydantic schema
    # The difference between returning a dict and a pydantic model is that the pydantic model provides
    # validation, serialization, and documentation benefits.
    return UserLoginResponseSchema(authentication_type="Bearer", token=token)


@UserRouter.post(Endpoints.LOGOUT, status_code=status.HTTP_200_OK)
def logout_user(token: str = Depends(oauth2_scheme), payload = Depends(decode_access_token), db=Depends(get_db)):
    """Invalidate current JWT by storing its JTI in blacklist until exp."""
    from jose import jwt
    from config import Settings
    settings = Settings()
    decoded = jwt.get_unverified_claims(token)
    jti = decoded.get("jti")
    exp = decoded.get("exp")
    if not jti or not exp:
        raise HTTPException(status_code=400, detail="Invalid token")
    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
    try:
        db.add(TokenBlacklist(jti=jti, expires_at=expires_at))
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to logout")
    return {"message": "Logged out"}


@UserRouter.post(Endpoints.CHANGE_PASSWORD, status_code=status.HTTP_200_OK)
def change_password(body: PasswordChangeSchema, payload = Depends(decode_access_token), db=Depends(get_db)):
    user = db.query(UserDBModel).filter(UserDBModel.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail=ResponseMessages.USER_NOT_FOUND)
    if not verify_password(body.current_password, user.hashed_password):
        raise HTTPException(status_code=401, detail=ResponseMessages.INVALID_PASSWORD)
    user.hashed_password = hash_password(body.new_password)
    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to change password")
    return {"message": "Password changed"}


@UserRouter.get(Endpoints.USER_INFO)
def get_user_info(payload = Depends(decode_access_token)): 
    return payload


@UserRouter.delete(Endpoints.ROOT, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(payload = Depends(decode_access_token), db=Depends(get_db)):
    user = db.query(UserDBModel).filter(UserDBModel.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(detail=ResponseMessages.USER_NOT_FOUND,
                            status_code=status.HTTP_404_NOT_FOUND)
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(detail="Failed to delete user", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@UserRouter.patch(Endpoints.ROOT, status_code=status.HTTP_200_OK,
                   response_model=UserRegisterResponseSchema)
def update_user(updated_user: UserUpdateSchema, payload = Depends(decode_access_token), db=Depends(get_db)):
    """
    This endpoint updates the user's name and email.
    Check UserUpdateSchema in UserSchemas.py for the fields that can be updated.
    """

    # First get the user from the database
    user = db.query(UserDBModel).filter(UserDBModel.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(detail=ResponseMessages.USER_NOT_FOUND,
                            status_code=status.HTTP_404_NOT_FOUND)
    # Update the user fields only if provided
    if updated_user.name is not None:
        user.name = updated_user.name
    if updated_user.email is not None:
        user.email = updated_user.email 
    try:
        # After modifying the user object, if we do the commit it will update the record in the database
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(detail="Failed to update user", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # update the user object with the latest data from the database
    db.refresh(user)
    return user


@UserRouter.post(Endpoints.VOTING, 
                 status_code=status.HTTP_201_CREATED,
                 response_model=VoteResponseSchema)
def vote_candidate(candidate: VotingSchema, user = Depends(decode_access_token), db=Depends(get_db)):
    # Check there is a candidate
    existing_candidate = db.query(CandidateDBModel).filter(CandidateDBModel.id == candidate.candidate_id).first()
    if not existing_candidate:
        raise HTTPException(detail="Candidate not found", status_code=status.HTTP_404_NOT_FOUND)
    # Check the user has not already voted
    existing_vote = db.query(VoteDBModel).filter(VoteDBModel.user_id == user["user_id"],
                                                 VoteDBModel.candidate_id == candidate.candidate_id).first()
    if existing_vote:
        raise HTTPException(detail="User has already voted", status_code=status.HTTP_400_BAD_REQUEST)

    # If everything is fine, cast the vote
    new_vote = VoteDBModel(user_id=user["user_id"], candidate_id=candidate.candidate_id)
    try:
        db.add(new_vote)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(detail="Failed to cast vote", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    db.refresh(new_vote)
    # Sometimes we need to return all fields of a database model,
    # In this case, we can return the SQLAlchemy model instance directly.
    # FastAPI will handle the serialization.
    # However, we will lose the automatic documentation benefits of pydantic models.
    # For the sake of documentation, we can create a VoteResponseSchema if needed.
    return new_vote


# Notes endpoints
@UserRouter.post(Endpoints.NOTES_ROOT, status_code=status.HTTP_201_CREATED, response_model=NoteResponseSchema)
def create_note(note: NoteCreateSchema, payload = Depends(decode_access_token), db=Depends(get_db)):
    # Validate personal encryption requirements
    if note.personal_encryption and not note.password:
        raise HTTPException(status_code=400, detail="Password required for personal encryption")

    ciphertext, nonce, salt, personal = encrypt_note(note.content, note.password if note.personal_encryption else None)
    db_note = NoteDBModel(
        user_id=payload["user_id"],
        title=note.title,
        content_encrypted=ciphertext,
        personal_encryption=personal,
        kdf_salt=salt,
        nonce=nonce,
    )
    try:
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create note")

    # Decrypt for response (app-level or personal depending on flag)
    try:
        content_plain = decrypt_note(db_note.content_encrypted, db_note.nonce, db_note.kdf_salt, db_note.personal_encryption, note.password)
    except Exception:
        # If decryption fails here, still created, but respond with masked content
        content_plain = ""
    return NoteResponseSchema(
        id=db_note.id,
        title=db_note.title,
        content=content_plain,
        personal_encryption=db_note.personal_encryption,
        created_at=db_note.created_at,
        updated_at=db_note.updated_at,
    )


@UserRouter.get(Endpoints.NOTES_ITEM, status_code=status.HTTP_200_OK, response_model=NoteResponseSchema)
def get_note(note_id: int, password: str | None = None, payload = Depends(decode_access_token), db=Depends(get_db)):
    db_note = db.query(NoteDBModel).filter(NoteDBModel.id == note_id, NoteDBModel.user_id == payload["user_id"]).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    try:
        secret = None if password is None else SecretStr(password)  # type: ignore[name-defined]
    except Exception:
        secret = None
    try:
        content_plain = decrypt_note(db_note.content_encrypted, db_note.nonce, db_note.kdf_salt, db_note.personal_encryption, secret)
    except Exception:
        if db_note.personal_encryption:
            raise HTTPException(status_code=401, detail="Invalid or missing password for personal note")
        else:
            raise HTTPException(status_code=500, detail="Failed to decrypt note")
    return NoteResponseSchema(
        id=db_note.id,
        title=db_note.title,
        content=content_plain,
        personal_encryption=db_note.personal_encryption,
        created_at=db_note.created_at,
        updated_at=db_note.updated_at,
    )


@UserRouter.patch(Endpoints.NOTES_ITEM, status_code=status.HTTP_200_OK, response_model=NoteResponseSchema)
def update_note(note_id: int, updated: NoteUpdateSchema, payload = Depends(decode_access_token), db=Depends(get_db)):
    db_note = db.query(NoteDBModel).filter(NoteDBModel.id == note_id, NoteDBModel.user_id == payload["user_id"]).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Update title if provided
    if updated.title is not None:
        db_note.title = updated.title

    # If content is provided, re-encrypt it (possibly switching encryption mode)
    if updated.content is not None:
        personal_flag = db_note.personal_encryption if updated.personal_encryption is None else updated.personal_encryption
        if personal_flag and not updated.password:
            raise HTTPException(status_code=400, detail="Password required for personal encryption")
        ciphertext, nonce, salt, personal = encrypt_note(updated.content, updated.password if personal_flag else None)
        db_note.content_encrypted = ciphertext
        db_note.nonce = nonce
        db_note.kdf_salt = salt
        db_note.personal_encryption = personal

    try:
        db.commit()
        db.refresh(db_note)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update note")

    # Decrypt to return plaintext
    try:
        content_plain = decrypt_note(db_note.content_encrypted, db_note.nonce, db_note.kdf_salt, db_note.personal_encryption, updated.password)
    except Exception:
        content_plain = ""
    return NoteResponseSchema(
        id=db_note.id,
        title=db_note.title,
        content=content_plain,
        personal_encryption=db_note.personal_encryption,
        created_at=db_note.created_at,
        updated_at=db_note.updated_at,
    )




AdminRouter = APIRouter(prefix="/admin", tags=["Admin"])

# Add candidates to db
@AdminRouter.post(Endpoints.CANDIDATE, status_code=status.HTTP_201_CREATED)
def add_candidate(new_candidate: CandidateSchema, db=Depends(get_db)):
    candidate = CandidateDBModel(**new_candidate.model_dump())
    try:
        db.add(candidate)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    db.refresh(candidate)
    return candidate


@AdminRouter.get(Endpoints.VOTE_COUNTS,
                 status_code=status.HTTP_200_OK,
                 ## To return a list of pydantic models, we can use List object from typing
                 ### Normal list will fail.
                 response_model=List[VoteCountResponseSchema])
def get_vote_counts(db=Depends(get_db)):
    results = db.query(
        VoteDBModel.candidate_id, 
        CandidateDBModel.name, 
        func.count(VoteDBModel.id)
    ).join(
        CandidateDBModel, 
        VoteDBModel.candidate_id == CandidateDBModel.id
    ).group_by(
        VoteDBModel.candidate_id, CandidateDBModel.name
    ).order_by(
        VoteDBModel.candidate_id
    ).all()
    ################ IMPORTANT ################
    # Fastapi can not return a list of tuples as a response, as the result of join and group by queries
    # Thus we need to convert the result to a dictionary or a list of dictionaries
    # Or we can create a pydantic model to represent the response
    # results_dict = {}
    ########### We need to loop over results and get the candidate_id, candidate_name, vote_count ###########
    ########### Comprehension way ###########
    # # results_dict = {
    # #     candidate_id: {"candidate_name": candidate_name, "vote_count": vote_count}
    # #     for candidate_id, candidate_name, vote_count in results
    # # }
    ########### OR Loop way ###########
    # for candidate_id, candidate_name, vote_count in results:
    #     results_dict[candidate_id] = {"candidate_name": candidate_name, "vote_count": vote_count}
    #
    # ##### BUT we will use Pydantic model to represent the response ##### 
    results_ = []
    for candidate_id, candidate_name, vote_count in results:
        results_.append(VoteCountResponseSchema(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            vote_count=vote_count
        ))
    return results_ 


@AdminRouter.get(Endpoints.CANDIDATE)
def get_candidates(db=Depends(get_db)):
    candidates = db.query(CandidateDBModel).all()
    return candidates