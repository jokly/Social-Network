
# Social Network

## API

1. Authorization
    Request: `/api/login?service_id=<your unique service id>&redirect_url=<url to redirect>`
    Response: `<url to redirect>?auth_code=<auth code>`

2. Get token
    Request: `/api/token?auth_code=<auth code>&service_id=<your unique service id>`
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

3. Get profile info
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

4. Get user posts
    Request: `/api/posts/<user_id>?token=<token>`
    Response: JSON

    ```json
    posts: [
        {
            "text": "<post text>",
            "date": "<post date>"
        }
    ]
    ```
