# Oauth 2. Пример провайдера на фрэймворке DJANGO 

### Endpoints

```grant/``` - авторизация приложения  
```tokenauth/``` - получение токена  
```signin/``` - форма авторизации  
```about/``` - защищеный URL  

### Constants

..settings  

TOKEN_TIME_LIFE  - время жизни токена
TOKEN_ENCODE_ALGORITM - алгоритм шифрования

#### Обязательно указать модуль авторизации
>REST_FRAMEWORK = {  
>    'DEFAULT_AUTHENTICATION_CLASSES': (  
>        'oauthapp.utils.JWTAuthentication',  
>    ),
>}

