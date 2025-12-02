from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.db.mongo import users_col
from app.models.user_model import RegisterDTO, LoginDTO, UserResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ------------------------------------------
# REGISTER
# ------------------------------------------
@router.post("/register", response_model=UserResponse)
async def register_user(body: RegisterDTO):

    # check existing
    existing = await users_col.find_one({"email": body.email})
    if existing:
        raise HTTPException(400, "Email already registered")

    hashed = hash_password(body.password)
    
    doc = {
        "email": body.email,
        "password_hash": hashed,
    }

    res = await users_col.insert_one(doc)

    token = create_access_token({
        "user_id": str(res.inserted_id),
        "email": body.email
    })

    return UserResponse(access_token=token, user_id=str(res.inserted_id))


# ------------------------------------------
# LOGIN
# ------------------------------------------
@router.post("/login", response_model=UserResponse)
async def login_user(body: LoginDTO):

    user = await users_col.find_one({"email": body.email})
    if not user:
        raise HTTPException(404, "User not found")

    if not verify_password(body.password, user["password_hash"]):
        raise HTTPException(401, "Incorrect credentials")

    token = create_access_token({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })

    return UserResponse(access_token=token, user_id=str(user["_id"]))
