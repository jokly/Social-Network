
# Social Network

## API

1. Authorization

    Redirect to url: `/api/login?service_id=<your unique service id>&redirect_url=<url to redirect>`

    Answer redirect to url: `<url to redirect>?auth_code=<auth code>`

2. Get token `POST`

    Request: `/api/token`

    ```post
    service_id=<your unique service id>
    auth_code=<auth code from "1. Authorization">
    ```

    Response: JSON
    ```json
    {
        "status": "ok",
        "user_id": "<user id>",
        "token": "<token>"
    }
    {
        "status": "error"
    }
    ```

3. Get profile info `GET`

    Request: `/api/profile/<user_id>?service_id=<your unique service id>&token=<token>`

    Response: JSON

    ```json
    {
        "status": "ok",
        "login": "<user login>",
        "email": "<user email>"
    }
    {
        "status": "error"
    }
    ```

## How its works

1. Получаем уникальный код по `1` пункту.

2. Далее получаем токен (который в дальнейшем и будет нам давать доступ к информации из другой социальной сети).
   Чтобы его получить, необходимо отправить код, полученный выше и уникальный ID вашего сайта (ГЛАВНОЕ! уникальный,
   выбираем его сами).

3. Далее по токену и ID сайта получаем профиль пользователя.
