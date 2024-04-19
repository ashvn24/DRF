from channels.middleware import BaseMiddleware
import jwt
from rest_framework.exceptions import AuthenticationFailed
from django.db import  close_old_connections
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from channels.db import database_sync_to_async
from testapp.models import  CustomUser
import hmac
import hashlib
import base64

class JWTwebsocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        
        query_string = scope.get("query_string",b"").decode("utf-8")
        
        query_parameters = dict(qp.split("=") for qp in query_string.split("&"))
        token = query_parameters.get("token" , None)
        
        if token is None:
            await send({
                "type":"websocket.close",
                "code":4000
            })
            
        authentication = JwtAuthentication()
        try:
            user = await authentication.authenticate_websocket(scope, token)
            print(user)
            if user is not None:
                scope['user'] = user
                
            else:
                await send({
                    "type":"websocket.close",
                    "code": 4000
                        })
            
            return await super().__call__(scope,receive,send)
        
        except AuthenticationFailed:
            await send({
                "type":"websocket.close",
                "code":4002
            })
            
class JwtAuthentication(BaseAuthentication):
    
    @database_sync_to_async
    def authenticate_websocket(self,scope,token):
        try:
        # Decode base64
            decoded_token = base64.b64decode(token)
            # Extract the payload
            payload = decoded_token.split(b':')[0]
            # Compute HMAC
            computed_hmac = hmac.new(settings.SECRET_KEY.encode(), payload, hashlib.sha256).digest()
            # Compare computed HMAC with the provided HMAC
            if hmac.compare_digest(decoded_token[len(payload) + 1:], computed_hmac):
                return payload.decode()
            else:
                return None
        except:
            return None
