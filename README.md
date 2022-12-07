## Main idea:

Implementation of a service that uses 2+ server architecture to provide interaction between telegram bot users and deep
learning models

**Server 1** (S1): hosts telegram bot and kafka on 24/7 basis.
It collects requests from users to queue.

**Server 2+** (S2): hosts DL models, reads kafka topics, returns results to telegram bot user. Comes online at no
schedule.

S1 message structure: 
```json
{
  "user": "user id",
  "request": {
    "text": "Text from user",
    "media": {
      # Fields inside `media` are optional
      "image": ...,  # encoded np.ndarray
      "audio": ...,  # ?
      "video": ...   # ?
    }
  }
}
```

