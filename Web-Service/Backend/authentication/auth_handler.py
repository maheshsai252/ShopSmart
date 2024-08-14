from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from snowflake.sqlalchemy import URL
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from models.pydantic_models import UserSignup,UserLogin
# Snowflake configuration
SNOWFLAKE_ACCOUNT=os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
JWT_SECRET = os.getenv("JWT_SECRET")
print(SNOWFLAKE_ACCOUNT)
print(SNOWFLAKE_USER)
print(SNOWFLAKE_PASSWORD)
print(SNOWFLAKE_DATABASE)

print(SNOWFLAKE_ROLE)
print(SNOWFLAKE_WAREHOUSE)
# Set up SQLAlchemy engine with Snowflake
snowflake_url = URL(
    account=SNOWFLAKE_ACCOUNT,
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    role=SNOWFLAKE_ROLE,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
)
engine = create_engine(snowflake_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)

    data.update({"exp": expire})
    
    token = jwt.encode(data, JWT_SECRET, algorithm=ALGORITHM)
    return token


# Signup endpoint
def signup_handler(user: UserSignup):
    try:
        with SessionLocal() as session:
            existing_user = session.execute(
                text("SELECT * FROM MARKETPLACE.PUBLIC.USERS WHERE USERNAME = :username"),
                {"username": user.username},
            ).fetchone()

            if existing_user:
                raise HTTPException(status_code=400, detail="Username already exists")

            # Insert the new user with hashed password
            session.execute(
                text("INSERT INTO MARKETPLACE.PUBLIC.USERS (USERNAME, PASSWORD, GENDER) VALUES (:username, :password, :gender)"),
                {
                    "username": user.username,
                    "password": pwd_context.hash(user.password),
                    "gender": user.gender,
                },
            )

            user_id = session.execute(
                text("SELECT ID FROM MARKETPLACE.PUBLIC.USERS WHERE USERNAME = :username"),
                {"username": user.username},
            ).fetchone()[0]

            # Insert selected activities into USERSACTIVITIES
            for activity in user.activities:
                session.execute(
                    text("INSERT INTO MARKETPLACE.PUBLIC.USERSACTIVITIES (USER_ID, ACTIVITY) VALUES (:user_id, :activity)"),
                    {
                        "user_id": user_id,
                        "activity": activity,
                    },
                )

            session.commit()
        return {"message": "Signup successful!"}

    except HTTPException as e:
        print(str(e))
        raise e  # Catch HTTP exceptions
    
    except Exception as e:
        print(str(e))
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"Signup failed due to internal server error: {str(e)}")


# Login endpoint with JWT generation
def login_handler(user: UserLogin):
    with SessionLocal() as session:
        existing_user = session.execute(
            text("SELECT * FROM MARKETPLACE.PUBLIC.USERS WHERE USERNAME = :username"),
            {"username": user.username},
        ).fetchone()

        if not existing_user:
            raise HTTPException(status_code=400, detail="Invalid username or password")
        print(existing_user)
        hashed_password = existing_user[2]
        if not pwd_context.verify(user.password, hashed_password):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        access_token = create_access_token(
            {
                "sub": user.username,
                "exp": datetime.utcnow() + timedelta(minutes=40),

            }
        )

    return {"access_token": access_token, "token_type": "Bearer", "user_id": existing_user[0]}