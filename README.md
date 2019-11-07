# python-server
RESTful python server

Reference: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

### Next steps
- Secure REST API on Flask using token based authentication [JWT]
- Look into Flask-Restful library
- Store session tokens in a NOSQL database like Redis.

Reference: https://stackoverflow.com/questions/47892413/how-to-secure-a-rest-api-on-flask

Resource: https://www.diycode.cc/projects/toddmotto/public-apis

Google Safe Browsing API Response
```json
{
    "report": {
        "matches": [
            {
                "cacheDuration": "300s",
                "platformType": "ANY_PLATFORM",
                "threat": {
                    "url": "http://testsafebrowsing.appspot.com/s/phishing.html"
                },
                "threatEntryType": "URL",
                "threatType": "SOCIAL_ENGINEERING"
            }
        ]
    }
}
```

Safe Browsing Testing Links : http://testsafebrowsing.appspot.com/

Link Preview API: https://www.linkpreview.net/
https://codingislove.com/generate-link-preview-webapp/

https://ip-api.com/docs/api:json

https://github.com/public-apis/public-apis#fraud-prevention