# [SpaceShare](https://spaceshare.me)   [![Build Status](https://travis-ci.org/DavidAwad/SpaceShare.svg?branch=master)](https://travis-ci.org/DavidAwad/SpaceShare) [![Coverage Status](https://coveralls.io/repos/DavidAwad/SpaceShare/badge.svg)](https://coveralls.io/r/DavidAwad/SpaceShare) [![Code Climate](https://d3s6mut3hikguw.cloudfront.net/github/DavidAwad/SpaceShare/badges/gpa.svg)](https://d3s6mut3hikguw.cloudfront.net/github/DavidAwad/SpaceShare/) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/DavidAwad/SpaceShare?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=body_badge)

<!--
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/DavidAwad/SpaceShare) [![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/davidawad/SpaceShare)
-->

### This is a File sharing web service meant to simplify file sharing between persons and groups of people by removing the need to login. It is not secure, it's not meant to be, it's meant to be the extreme trade off between convenience and security.


#### You go to the app, upload your file, attach a number.
#### Others can go to the site knowing that number; or go to [spaceshare.me/upload/number](spaceshare.me/upload/number) and it will give you that file.

## Requirements
- Python
- Flask
- MongoDB
- Redis
- Celery
- React
- Gulp
- bower
- npm

## Development
#### You wanna run this hotness?
```shell
git clone https://github.com/davidawad/spaceshare
cd spaceshare
cp -r app/static nginx
docker-compose up
# awesome things
```

###### fair warning, it doesn't fucking work yet.

## Contributing
Please do check out the [contributing](/CONTRIBUTING.md) guide if you're interested.

## Special Thanks :
### [Joel Pena](https://github.com/jpena29), [Devon Peticolas](https://github.com/x), and [Wisdom Omuya](https://github.com/deafgoat), and of course StackOverflow made this app Possible.
