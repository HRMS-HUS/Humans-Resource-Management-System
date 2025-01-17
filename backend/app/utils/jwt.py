from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status,Depends, Request, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from ..models import users as models_user
from ..configs.database import get_db, AsyncSession
import os
from..configs.redis import redis_client

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480
ACCESS_TOKEN_EXPIRE_MINUTES_ADMIN = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Get stored refresh token from Redis
        stored_refresh_token = await redis_client.get(f"refresh_token:{user_id}")
        if not stored_refresh_token or stored_refresh_token.decode() != refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is invalid or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Create new access token
        access_token = await create_access_token({"sub": user_id})
        
        # Store new access token in Redis
        await redis_client.setex(
            user_id,
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            access_token
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )



async def get_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Decode token to get username
        user_id = await decode_access_token(token)
        # username = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Get token from Redis
        redis_token = await redis_client.get(user_id)
        
        if not redis_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return redis_token
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(get_token), db: AsyncSession = Depends(get_db)):
    try:
        # Decode the token to get the username
        user_id = await decode_access_token(token)
        # username = payload.get("sub")
        
        # Find user in database
        stmt = select(models_user.Users).where(models_user.Users.user_id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

        
async def get_active_user(db: AsyncSession = Depends(get_db), current_user: models_user.Users = Depends(get_current_user)):
    if current_user.status != models_user.StatusEnum.Active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
    return current_user

async def get_current_admin(db: AsyncSession = Depends(get_db), current_user: models_user.Users = Depends(get_active_user)):
    if current_user.role != models_user.RoleEnum.Admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

async def get_current_manager(
    current_user: dict = Depends(get_active_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != models_user.RoleEnum.Manager and current_user.role != models_user.RoleEnum.Admin: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user