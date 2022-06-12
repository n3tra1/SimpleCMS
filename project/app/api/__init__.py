import os
from datetime import timedelta

from fastapi_jwt import JwtAccessBearer

# In real life you should consider an idea to use rotating JWT
# with access and refresh tokens
# https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation
# but I'm not sure, that is important for this test task

access_security = JwtAccessBearer(
    os.getenv("JWT_SECURITY_KEY"),
    access_expires_delta=timedelta(seconds=int(os.getenv("JWT_TTL_SECONDS"))),
    auto_error=True)
