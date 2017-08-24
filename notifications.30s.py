#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>GitHub Notifications</bitbar.title>
# <bitbar.version>v3.0.0</bitbar.version>
# <bitbar.author>Keith Cirkel, John Flesch</bitbar.author>
# <bitbar.author.github>flesch</bitbar.author.github>
# <bitbar.desc>GitHub (and GitHub:Enterprise) notifications in your menu bar!</bitbar.desc>
# <bitbar.image>https://i.imgur.com/hW7dw9E.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>

import json
import urllib2
import os
import sys
import re
from itertools import groupby

# GitHub.com
github_api_key = '0ca09a86b67f449946ab1b1a4cb1ecb050a9fdad'

# GitHub:Enterprise (optional)
enterprise_api_key = os.getenv( 'GITHUB_ENTERPRISE_TOKEN', 'Enter your GitHub:Enterprise Personal Access Token here...' )
enterprise_api_url = os.getenv( 'GITHUB_ENTERPRISE_API', 'https://github.example.com/api/v3' )

active = '#0469d6'
inactive = '#7d7d7d'

octocat_base64_eclipse = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAASABIAAD/4QCqRXhpZgAATU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgExAAIAAAAeAAAAWodpAAQAAAABAAAAeAAAAAAAAABIAAAAAQAAAEgAAAABQWRvYmUgUGhvdG9zaG9wIENTNSBNYWNpbnRvc2gAAAOgAQADAAAAAQABAACgAgAEAAAAAQAAABCgAwAEAAAAAQAAABAAAAAA/+ELQGh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8APD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo1QkNFMkMyMDczNTMxMUUwOEEzMkRCNEYwMDM5MTQ3QyIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo1QkNFMkMxRjczNTMxMUUwOEEzMkRCNEYwMDM5MTQ3QyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOkZCN0YxMTc0MDcyMDY4MTE4QTZEQjg3ODU3MkVFMEExIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCBDUzUgTWFjaW50b3NoIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MDg4MDExNzQwNzIwNjgxMThBNkREMDk5QzEyREYzOTYiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RkI3RjExNzQwNzIwNjgxMThBNkRCODc4NTcyRUUwQTEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPD94cGFja2V0IGVuZD0idyI/PgD/7QA4UGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAAA4QklNBCUAAAAAABDUHYzZjwCyBOmACZjs+EJ+/8AAEQgAEAAQAwERAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/bAEMAAwICAgICAwICAwUDAwMFBQQDAwQFBgUFBQUFBggGBwcHBwYICAkKCgoJCAwMDAwMDA4ODg4OEBAQEBAQEBAQEP/bAEMBAwQEBgYGDAgIDBIODA4SFBAQEBAUERAQEBAQEREQEBAQEBAREBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEP/dAAQAAv/aAAwDAQACEQMRAD8A8FvdF8CeJPh1pWl+A/CGq+K/FUcEt7rkekqZEgtzL5dsxAjdUDbW+8cnB25wRXXOpTpxu2l/Wv8AX3kRpVJytHVHy78StJ13w9qo0vW9AvvDzsvnR2mpArKwPU8ogwDxx+NcyrxnsW6MqfxH/9D4A8C/FX4o/DxZ4/B2qPbx3QiEoUsFbyg2wnBH3Q7AZyOema6J4P2iM6eN9m7JnO+NPFHifx3qD6x4uvmnu1DCJnLNuY7QRkk4yB9OOmTmueGG9mbTxHO7s//Z'

octocat_base64_purple = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAACXBIWXMAAAsTAAALEwEAmpwYAAAEE2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgICAgICAgICAgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiCiAgICAgICAgICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOkU1MTc4QTJBOTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC94bXBNTTpJbnN0YW5jZUlEPgogICAgICAgICA8eG1wTU06RGVyaXZlZEZyb20gcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICA8c3RSZWY6aW5zdGFuY2VJRD54bXAuaWlkOkU1MTc4QTI4OTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC9zdFJlZjppbnN0YW5jZUlEPgogICAgICAgICAgICA8c3RSZWY6ZG9jdW1lbnRJRD54bXAuZGlkOkU1MTc4QTI5OTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC9zdFJlZjpkb2N1bWVudElEPgogICAgICAgICA8L3htcE1NOkRlcml2ZWRGcm9tPgogICAgICAgICA8eG1wTU06RG9jdW1lbnRJRD54bXAuZGlkOkU1MTc4QTJCOTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC94bXBNTTpEb2N1bWVudElEPgogICAgICAgICA8eG1wOkNyZWF0b3JUb29sPkFkb2JlIFBob3Rvc2hvcCBDUzYgKE1hY2ludG9zaCk8L3htcDpDcmVhdG9yVG9vbD4KICAgICAgICAgPHRpZmY6T3JpZW50YXRpb24+MTwvdGlmZjpPcmllbnRhdGlvbj4KICAgICAgPC9yZGY6RGVzY3JpcHRpb24+CiAgIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+Col7WvIAAAKmSURBVDgRVVNLaFNRED335iVpPvZjKihELG4FXagLsaVZdqFoKy3oyoq4EBf9qJS6qRspqWjxs1D8rVuliC6Kq0IXglRxIVhcJVq00I8JaZP38vLedc5rsnDIzZ3POTNzZxKFHdFy+VRnb5iukMKgVsh4BgfoEzvvGyyI/bJ/Si3SJxJwVEO51/8r1tGRfqQ0LiVjgFMFav5OUktDRyPAVgUwPl7kcivXRmb3iwWpI/JuwsRrZcynWtDluECVpwZEw4xKMrEjlhyx6dsoYtGKo+f0hCqzDbjbeLg3ha71Ahb+buGyXcUX30fFdrDME+jiY4wYYskhV88Mm262XbaDISwP3FXP87mVzibg4FoRh3mo08eYDGqZWHLItcJhDCYE4XrilItZh2fTtoLiGxuyamDUiFjEEEvOtpFhG4OMK++VodleFY/JELImYQcPRZ0+xoghlhxytUTSQcDDWtJHjrqILwQjd3DqerBmYjzBEkSuVJJE8qU1Ek4KskCyyPtfGj5ipJckOfywrTyhTVHsrhXRTf12ZiEkF5/QEFX3wSshIyttY0CS5NXrUfOkOYkrpYrMxKAsvZ8ayKpPdWYjSdDSzJA5ocOYCVtIJ6JAoYSnam7MHI1FsOQ4mHZ9tO5L4eKfDXz1XVwdmFYfmYjEkIWsPPOk/JiU7cKXn6CW9x/XvZPqs+z1QesuDEm5Z6ubGA9p5GMJ/Kx3ASuCQjSKTq5HyHZ7M7TvYfpMVi01WsSbm2ZejGNS6fx2Bb8v3FffJQFbN+/HTFvVww+p3p6MS+tbmDs7qfpYgEMM9nsuq3okwauwxoeWOL69HTd7SCZos4BwJIJ2pwZ/s4g7DTK5JHO/QZLerLpereCQtDncHEFR/IGsb6yU5P8x5No40jelbtXdAfcf8D4uxyVOr9EAAAAASUVORK5CYII='

octocat_base64_muertos = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAASABIAAD/4QCqRXhpZgAATU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgExAAIAAAAeAAAAWodpAAQAAAABAAAAeAAAAAAAAABIAAAAAQAAAEgAAAABQWRvYmUgUGhvdG9zaG9wIENTNSBNYWNpbnRvc2gAAAOgAQADAAAAAQABAACgAgAEAAAAAQAAABCgAwAEAAAAAQAAABAAAAAA/+EK/Gh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8APD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo1MEIyREU3OUY5QTMxMUUwOUU1QUUwRjA0RUZCOUY1MCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo1MEIyREU3QUY5QTMxMUUwOUU1QUUwRjA0RUZCOUY1MCIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ1M1IE1hY2ludG9zaCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjUwQjJERTc3RjlBMzExRTA5RTVBRTBGMDRFRkI5RjUwIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjUwQjJERTc4RjlBMzExRTA5RTVBRTBGMDRFRkI5RjUwIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDw/eHBhY2tldCBlbmQ9InciPz4A/+0AOFBob3Rvc2hvcCAzLjAAOEJJTQQEAAAAAAAAOEJJTQQlAAAAAAAQ1B2M2Y8AsgTpgAmY7PhCfv/AABEIABAAEAMBEQACEQEDEQH/xAAfAAABBQEBAQEBAQAAAAAAAAAAAQIDBAUGBwgJCgv/xAC1EAACAQMDAgQDBQUEBAAAAX0BAgMABBEFEiExQQYTUWEHInEUMoGRoQgjQrHBFVLR8CQzYnKCCQoWFxgZGiUmJygpKjQ1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4eLj5OXm5+jp6vHy8/T19vf4+fr/xAAfAQADAQEBAQEBAQEBAAAAAAAAAQIDBAUGBwgJCgv/xAC1EQACAQIEBAMEBwUEBAABAncAAQIDEQQFITEGEkFRB2FxEyIygQgUQpGhscEJIzNS8BVictEKFiQ04SXxFxgZGiYnKCkqNTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqCg4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2dri4+Tl5ufo6ery8/T19vf4+fr/2wBDAAMCAgICAgMCAgMFAwMDBQUEAwMEBQYFBQUFBQYIBgcHBwcGCAgJCgoKCQgMDAwMDAwODg4ODhAQEBAQEBAQEBD/2wBDAQMEBAYGBgwICAwSDgwOEhQQEBAQFBEQEBAQEBEREBAQEBAQERAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBD/3QAEAAL/2gAMAwEAAhEDEQA/APa/2qvDnxWh8T6ZpGtfErWtW0rxLq1jZaTpGhaWIotPuNRmmitnuWs2Di3hEeJJHfJJBwDXlvLp1pPnqytuktPldJ+n4to+9wnE2GwdKKw+EpqpZKU53qN7XajJqKb3/DUo/sxeDfjBP431XR/DnxW1/Q9N8K6veWevaNrukx3Frqc+nS26XDWjXjF/s8yybUlDBsjcM5reGC9ilyTdnrZ6v01S/D773PNzDPYY2TlVoQ5rcqlBez9G4x0bV+va21j/0Pub436Hq95rCLpsDtPe28A0aW3g3SRXtrKzOwuCwEB8p+uRvAxhu3DW9q5OMXa8XZ9VLuephY00lUlHmUJLmjdaxfZb+rW3U6L4G6Jf6J4Ze017S/I1Vz5mparK6Sz6hKzud8jLk/KMBQW6dABXRRjOMFGb5mkk33fV26HLiJU5TcoKybbUf5VfRX66fl1P/9k='

octocat_base64_major = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAACXBIWXMAAAsTAAALEwEAmpwYAAAEE2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgICAgICAgICAgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiCiAgICAgICAgICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgICAgICAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iPgogICAgICAgICA8eG1wTU06RG9jdW1lbnRJRD54bXAuZGlkOkU1MTc4QTJCOTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC94bXBNTTpEb2N1bWVudElEPgogICAgICAgICA8eG1wTU06RGVyaXZlZEZyb20gcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICA8c3RSZWY6aW5zdGFuY2VJRD54bXAuaWlkOkU1MTc4QTI4OTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC9zdFJlZjppbnN0YW5jZUlEPgogICAgICAgICAgICA8c3RSZWY6ZG9jdW1lbnRJRD54bXAuZGlkOkU1MTc4QTI5OTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC9zdFJlZjpkb2N1bWVudElEPgogICAgICAgICA8L3htcE1NOkRlcml2ZWRGcm9tPgogICAgICAgICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOkU1MTc4QTJBOTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC94bXBNTTpJbnN0YW5jZUlEPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICAgICA8eG1wOkNyZWF0b3JUb29sPkFkb2JlIFBob3Rvc2hvcCBDUzYgKE1hY2ludG9zaCk8L3htcDpDcmVhdG9yVG9vbD4KICAgICAgPC9yZGY6RGVzY3JpcHRpb24+CiAgIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+Ck3jLMoAAALPSURBVDgRVVHNaxNBFH8zu5smu/lOW1Kapmn1pEVoG1MKLU0v0rMHwWPFo6Bn/wDPYhXBinr34EkoQiFQPFjaSkHxA6mNCSY2zWfb3c1+zDhv0wg+mJ3f/N7v92bePgK9oGJjCBszY4uUSqvikGeMjSNHKS0KQYEx92V8r7SFnAjPQ/qAp1KB+rD0WJalW5FQHHS9A45teUVlxUdVNQztkwY4jvsiceTeIeWygV4sAHx2Vm3S+kYseXER9BY4ximcORaEfAOYhhOrC5rsAzkQBFCj0Kz+2IqxxArZ3dXxGVDnx2uxiexis/Kt0GhXb7csY89lrtHu6l9xIUYOc6hBLXrQC5Xp5FIrN8n5tXneymWeIoftnOYvJ3cAFFyIkcMcanraSY5eWVW01bAWBujqIH6ajSIolcwgIdhjLwqfq5xzAoT0NEIb0SJAzsgqtZmdd7oGdIyO6YL0BB03CKGeAQD/EUGMHOZQg1r0oJcqFFJegrm11tDPQ8SvxUgJIVxAbyFGDnOocYHXEKOXukziFmdiqFQbrES9PsWNmP8v+hxqxFOC6EEvpcCLqIxo4bgOoSXPtbwsid0bsXdG3OPAkqJ5TfbHkHfBKVJG2Kbq16Ctd858Ml0/zk7kSKHgiDw+w/sHiJErT4/OS8DWTNcGVYuCRMgmdV37GTBXKOk6YfxtIj31oZHLfETxeRGOuJYd2wrKyvvIgJrq2jZrd44hSOR1OrRX2W3onUfh4fF7qk95Xi/t35eAFEf92i9RwAtK5FZICSwAoaRjmWZi5AK1Hfuhb/tg51+f4tYN0XjWIeSmZRq/R/arX4Tbm0JrIR1jpvR9QFEG1WgS2vXym+j2wXWsjrP15hvfPlwhRHoVVdR3MS366c/cxNB5ATA7XUUVZqNrsma99KBv7nvF3iuC4GQufak2k77HMxk/njH4fCpwdDV9t3plbKrHeF/v4r/S1mLheIAr2gAAAABJRU5ErkJggg=='

octocat_base64_minor = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAACXBIWXMAAAsTAAALEwEAmpwYAAAEE2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgICAgICAgICAgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiCiAgICAgICAgICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgICAgICAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iPgogICAgICAgICA8eG1wTU06RG9jdW1lbnRJRD54bXAuZGlkOkU1MTc4QTJCOTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC94bXBNTTpEb2N1bWVudElEPgogICAgICAgICA8eG1wTU06RGVyaXZlZEZyb20gcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICA8c3RSZWY6aW5zdGFuY2VJRD54bXAuaWlkOkU1MTc4QTI4OTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC9zdFJlZjppbnN0YW5jZUlEPgogICAgICAgICAgICA8c3RSZWY6ZG9jdW1lbnRJRD54bXAuZGlkOkU1MTc4QTI5OTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC9zdFJlZjpkb2N1bWVudElEPgogICAgICAgICA8L3htcE1NOkRlcml2ZWRGcm9tPgogICAgICAgICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOkU1MTc4QTJBOTlBMDExRTI5QTE1QkMxMDQ2QTg5MDREPC94bXBNTTpJbnN0YW5jZUlEPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICAgICA8eG1wOkNyZWF0b3JUb29sPkFkb2JlIFBob3Rvc2hvcCBDUzYgKE1hY2ludG9zaCk8L3htcDpDcmVhdG9yVG9vbD4KICAgICAgPC9yZGY6RGVzY3JpcHRpb24+CiAgIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+Ck3jLMoAAAKGSURBVDgRXVLPS5RRFD3fNw7jjJZYUaJCtIq02jQjSIhuCvsDahMUQwtXMW1atHMTbYIIsTApadHGAXFR4UaKpMBscHSskKFi+iH2QybSxhnn+97tnjczEl6++96Zc8957857z0ElXJ0MoaTQY4LRuAOnz5i5g+RcN5YTyHO3/GbMOYEZchrWw8ECeXU27KdxH6H+F+7ec3En1HHI1QrTYuVYo4Za9XFD19EBKyuItOQx5bQ/6sHGN6CgWVoGwsdYBjYzQOgwEGkDGtsgX8/PrDajv7UVBVu3qxYfi5fGs60MLpXTSCkumMXoeyYxOdaoEdXabukuv0avLPWLfL/DBe6SY4vyCS0jIwgyiattgxpq6aG3ri4Si6OpByjmeRplLoDu8aLjOJsW6zAArIqM69/Vz6iGWvXUYS3u+t5cH4o/IH8mi4EShmlKJpOuiPB8bBKTYy3gY5haeqzXW4Qn2YTo/DmbvRyiSIPGnWE5aoxqqx6PtyQwv3mXDfs2hng90B13mre5qqax6hG2laPaaRrcswvorTidAKkKtqNiy0E1fU440UzW+Mi5nsE0Ip3w84N/1TK6NYcux4GndbbBRZhCrjDb1a2/huCtALtPwDiYdoM+7sEUEHCjoyp8EuycmDVpzFtxZREhLqcwUx82LwMNA+1+KWmw9hRBA3oAPx27LfmHUl7CyXIG1+RtdFK+XNBnV4lSBkdkeUDMUpRvZdNqU7hVq9tZC1N6E78kc/rUehqdSvJ87DlI7kazl8FPWb4osvZAzGJs4n8zhTb8BdyUD1eFVyQfEwdqvCwc388OdBNfO7xe43Xe9m6DUvZMh5/CFZGx+pqQz3hrHon1dzha42rmf2IFXA8MHfgaAAAAAElFTkSuQmCC'

# Utility Functions

def plural( word, n ):
    return str(n) + ' ' + (word + 's' if n > 1 else word)

def get_dict_subset( thedict, *keys ):
    return dict([ (key, thedict[key]) for key in keys if key in thedict ])

def print_bitbar_line( title, **kwargs ):
    print title + ' | ' + ( ' '.join( [ '{}={}'.format( k, v ) for k, v in kwargs.items() ] ) )

def make_github_request( url, method='GET', data=None, enterprise = False ):
    try:
        api_key = enterprise_api_key if enterprise else github_api_key
        headers = {
            'Authorization': 'token ' + api_key,
            'Accept': 'application/json',
        }
        if data is not None:
            data = json.dumps(data)
            headers['Content-Type'] = 'application/json'
            headers['Content-Length'] = len(data)
        request = urllib2.Request( url, headers=headers )
        request.get_method = lambda: method
        response = urllib2.urlopen( request, data )
        return json.load( response ) if response.headers.get('content-length', 0) > 0 else {}
    except Exception:
        return None

def get_notifications( enterprise ):
    url = '%s/notifications' % (enterprise_api_url if enterprise else 'https://api.github.com')
    return make_github_request( url, enterprise=enterprise ) or []

def get_status():
    url = 'https://status.github.com/api/status.json'
    return make_github_request( url ) or {}

def print_notifications( notifications, enterprise=False ):
    notifications = sorted( notifications, key=lambda notification: notification['repository']['full_name'] )
    for repo, repo_notifications in groupby( notifications, key=lambda notification: notification['repository']['full_name'] ):
        if repo:
            repo_notifications = list( repo_notifications )
            print_bitbar_line( title=repo )
            print_bitbar_line(
                title='{title} - Mark {count} As Read'.format( title=repo, count=len( repo_notifications ) ),
                alternate='true',
                refresh='true',
                bash=__file__,
                terminal='false',
                param1='readrepo',
                param2=repo,
                param3='--enterprise' if enterprise else None
            )
            for notification in repo_notifications:
                formatted_notification = format_notification( notification )
                print_bitbar_line( refresh='true', **get_dict_subset( formatted_notification, 'title', 'href', 'image', 'templateImage' ) )
                print_bitbar_line(
                    refresh='true',
                    title='%s - Mark As Read' % formatted_notification['title'],
                    alternate='true',
                    bash=__file__,
                    terminal='false',
                    param1='readthread',
                    param2=formatted_notification['thread'],
                    param3='--enterprise' if enterprise else None,
                    **get_dict_subset( formatted_notification, 'image', 'templateImage' )
                )

def format_notification( notification ):
    type = notification['subject']['type']
    formatted = {
        'thread': notification['url'],
        'title': notification['subject']['title'].encode('utf-8'),
        'href': notification['subject']['url'],
        'image': 'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAQCAYAAAAmlE46AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAA',
    }
    if len(formatted['title']) > 80:
        formatted['title'] = formatted['title'][:69] + '…'
    latest_comment_url = notification.get( 'subject', {} ).get( 'latest_comment_url', None )
    typejson = make_github_request( formatted['href'] )
    if typejson and typejson.get( 'user', {} ).get( 'login', None ):
        formatted['title'] = '@{}: '.format(typejson['user']['login']) + formatted['title']
    formatted['title'] =  '{} / '.format(notification['reason']) + formatted['title']
    if latest_comment_url:
        formatted['href'] = ( make_github_request( latest_comment_url ) or {} ).get( 'html_url', formatted['href'] )
    # Try to hack a web-viewable URL if the last check failed
    if formatted['href']:
        formatted['href'] = re.sub( 'api\.|api/v3/|repos/', '', re.sub( '(pull|commit)s', ur'\1', formatted['href'] ) )
    if (type == 'PullRequest'):
        if typejson and typejson['merged']:
            formatted['image'] += 'SpJREFUKJG9kkFOwmAQhb+ZQiVx5xm4hIlncEF7jLZuWSjSeAJsvQUY4xkMHsCtcU9MXBmwJsy4EWgFEt34VpP55mX+eflhj9KoGO5jAK00LmOwoZiaYIPRbXaXRsVQRC6BvWZJ4uLJRI6DcKlUMsVl/G0CwIw3UR8V4+QKxFd9BbfDqiP6buo1sB5QjgTJ07i8aPTFgvNFa/7i7fYzaL+YpEN3zwGux4mY2QmAm6db783i0rO4bGyrh7OL66a0Bigm6d5gGkYz3brvV8a/SjeF/dPGJLrpmTMDXs/i4vTnQNYrInNm5szqvIVYbiJdCV1Z6ANwXze6em4i3SBcqi+CNVeAIFxq9dkR0+07HfHVz6rzlsLAK5keUCEu/R0hDD7C+SME6A7+Z30BqF2G+GPLjSUAAAAASUVORK5CYII='
        elif typejson and typejson['state'] == 'closed':
            formatted['image'] += 'Q9JREFUKJG9kjFOw0AQRd9sbAiiQOIMqWJfAInOPULANehTQIjFCbgHFS1eKhR6cDpEbyHRmljyDpWVTWJbSsOvRvvm72i+BjpkI2ZdDIBszNVzTG7HvGcx543JxmifT7KIj4FyUlaYcMjcKI8Id17Pj8JDknMvrD4zoriwRg4OMaKtU44FUhtz6z8aFW7KkC9X82mESbJghpICJDkiyimAwvV2EDG6uZMfThs3TeFYB8miP1XjFb0pdhp31cro/muijbjAUTjDtx1zttnwEnGJo8BR+DxQSAcwWv5i9vd4BZ58Yy2kgTIqq3VuAMoKEx4htCQrijaX5fMAYRoOmbMEJ0y2lhGmZcgbNdDGd9Uf3M1iNlKZZGMAAAAASUVORK5CYII='
        else:
            formatted['image'] += 'TJJREFUKJG9krFOAlEQRe/MLpqHnd/ATyBWsLWF+hcLPYXibvwCE/gLC2MNVrD7AbbGnpjYboBlro2QXWATabzVy5x338ydPKBC4awTVTEA8Huz9i1FI5gZBINh6+0lnHUiEXkAUGmWMGm/c7Fues4pLU9IPv+aAABm9i2qT6Pm+BECbuoqpnZWW4lmmRLG3ZdV9VyAOEyD+1JdVO4yqX+ua7UPofRHrUlEMgaA4cVYALkEACF6e/N2k4DdJCh1Ky7nENftyVACo9akcjElox3I9yfjsdoaVfFPHbtpcG2GOUy/wjS42r0QTjs3ZpibYV7kPmkxVuuGOKfIl1MAr0WjqMRcrBqec8oCVwDwnNOFnwugezkJ4+ZnFbkPeANanpwsAQr7+2m8Qab1FKcAeYgfqR/3P4pMOYR15QAAAABJRU5ErkJggg=='
    elif (type == 'RepositoryInvitation'):
        formatted['image'] = 'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAKCAYAAACE2W/HAAAAAXNSR0IArs4c6QAAAM1JREFUKBWVkD0OQUEUhcdv/ASJn55SyxLoVBJq8tZjBRQsgkZiAQoqOiQ2oFc935nMvLxEXsRJPufOufe+kTHGmBeEf3Jg3i4t8IwOP6QZzeoi+3PFt1BRkKAq+Q4uEKbdUA+/wxm6LoubshPcoO8b9lp3GOMPGPomPoInqOcV/VUfyKfwhsChegJxfS3O6R5hALpFqFY2A69osUyygT3UQOpAWwVSpt4aShAt6lWXkIUk5WiswL5qiqIODdBz6+ZirM67cwFvulwfaH0AC7M1lHL62U4AAAAASUVORK5CYII=';
        formatted['templateImage'] = formatted.pop('image');
    elif (type == 'Issue'):
        if typejson and typejson['state'] == 'closed':
            formatted['image'] += 'YpJREFUKJGdkj9I23EQxT93SZrJQYNQ6Bo65BtQcHRpSeyUuQqNWx2ti7qJRpqhUxGX0lGhlXQ0uJhfU7cOLm3+QKCzoIjoJpp8z0HT/BpJBd90HO/dvTsePBLS36iM8Uw6vANyQNJ7RJU/wG7nmo1XLY7uCStp8uL5BJwgbJtRU8E8jImR98qoGHPZBjsSFhlsCRQjCQovD2iHhx5OEDu/ZF2E5Y4wLn/tXdMy5WO2zkqXHKQxgEy95+y7Y1KMXwogbeaBk0iCwqBn7DteAJym+NmBnSiAF3IK2/32wiIVqoGjYE1GRMlGARSSZtQGbZtq8CNwFBBWDUxgJjqI3I9Mg7XAgRoXmSYlACqOWuAG39ePimNB7+oyxuzhBLEwIUhj3c92sZckLsaSAvg2m14ZPb98eGs8ThFlqBcAx4wJX8T4cGasvm5yFRaUUjwZUd4bLKow/W/kbsWfgTMxvorxmwhtjHEPbxSGEd5many7F/JqiqdemceT88rzu3ZLoWywma1z/NA5/8UNNkSJCdaYQF4AAAAASUVORK5CYII='
        else:
            formatted['image'] += 'ZxJREFUKJGdkjFoU2EUhb97k9jNRzEFoWvJVHXoZCqIaQaH7JaUbtpi2zc4ORWJYKGTYJLBroFaiGPo0hBwyAOhU51Cd8EOOid53uugL4SnkOK3/dx7OPccfvhPZPqxHZUWc0gIUjFs6c/CJdDBtN580P36lzCM1jZ+mr9HuFKkJfgXABO9i/mmqOTd7VlztXcyEYbR2oabtFx5kx+Oa7VHn+LpS7bOV3K5UfBaTF+6WLW52juR7ai0mDEGovq2WezuJ8t7UdkBGsXu5KqdfvlQhOeeGRc0h4QIV/nhuDarkIVgft+xHxJnQwWpKNJKn/cvasvtkcCxuFTUsKWkiOsgrhcoBb2uIE1W4NKRO8DH6cF0KSnLewYDBTqGb26dr+Sm53tR2ZNmE8LTx3O4V9XpKKZ1FV24MZyf2aoH8YE5garXBWC3X1oX12NXO8zfvPWqttwepZ08iA9wXqDypFE8a09y7PZL64geCXx37IO4XiSZcK/+dso8bRTP2pD65DufH96WOBuKSwWlAGD4QJ2Oqtff3e99mxVnJr8AXSGi02ni0+YAAAAASUVORK5CYII='
    elif (type == 'Commit'):
        formatted['image'] += 'HhJREFUKJHl0LEKwkAQBNCH3yIaf05S+VUqmh8ykFoUYn8WbnEc8a7XgYVlmNkdhv/EDgNmvHDFtmXq8ETCiFvsD2xqxksI9xnXB3cqxamYceHgVOpWC6JUi/QNQxj7jDsEd6wZ83KmLOId69bXzqekOeas0eiv4g3q4SY7NY1R2gAAAABJRU5ErkJggg=='
        formatted['templateImage'] = formatted.pop('image')
    elif (type == 'Release'):
        formatted['image'] += 'JdJREFUKJGl0DsKwkAUBdDTRgvFHbgmNyLY+QWzKxM/kK2kSKc70MIIQ0ziqBceA/dxinn8mSkKVMGUmH+CBWaNboQjdn2wqt97Pa8kNd5+C0O86YNdSZC34RLjCJxhHZYLXDCIxKuwTHGOwBNcm2WKUw9OcMCybZl6XjHpQOs30cB5gKNQiDPPP0WjV/a4aVwxNsNfUGce7P8k4XgVPSYAAAAASUVORK5CYII='
        formatted['templateImage'] = formatted.pop('image')
    return formatted
if len(sys.argv) > 1:
    command = sys.argv[1]
    args = sys.argv[2:]
    enterprise=False
    if ('--enterprise' in args):
        enterprise=True
        args.remove( '--enterprise' )
    if command == 'readrepo':
        url = '%s/repos/%s/notifications' % (enterprise_api_url if enterprise else 'https://api.github.com', args[0])
        print 'Marking %s as read' % url
        make_github_request( url=url, method='PUT', data={}, enterprise=enterprise )
    elif command == 'readthread':
        url = args[0]
        print 'Marking %s as read' % url
        make_github_request( url=url, method='PATCH', data={}, enterprise=enterprise )
    elif command == 'readall':
        url = '%s/notifications' % (enterprise_api_url if enterprise else 'https://api.github.com')
        print 'Marking all as read'
        make_github_request( url=url, method='PUT', data={}, enterprise=enterprise)

else:
    is_github_defined = len( github_api_key ) == 40
    is_github_enterprise_defined = len( enterprise_api_key ) == 40
    github_notifications = get_notifications( enterprise=False ) if is_github_defined else []
    enterprise_notifications = get_notifications( enterprise=True ) if is_github_enterprise_defined else []
    has_notifications = len( github_notifications ) + len( enterprise_notifications )
    color = active if has_notifications else inactive
    github_status = get_status()
    octocat_status = octocat_base64_purple
    if github_status['status'] == 'major':
        octocat_status = octocat_base64_major
    elif github_status['status'] == 'minor':
        octocat_status = octocat_base64_minor

    if (has_notifications):
        print_bitbar_line(
            title=( u'%s' % len( github_notifications ) ).encode('utf-8') ,
            color=color ,
            image=octocat_status
        )
        print '---'
    else:
        # print '-'
        print_bitbar_line(
            title=''.encode('utf-8') ,
            image=octocat_status
        )
        exit(0)


    if is_github_defined:
        if len( github_notifications ):
            # print_bitbar_line(
            #     title=( u'GitHub \u2014 %s' % plural( 'notification', len( github_notifications ) ) ).encode( 'utf-8' ),
            #     color=active,
            #     href='https://github.com/notifications',
            # )
            print_notifications( github_notifications )
            if (len( github_notifications ) > 0):
                print_bitbar_line(
                    title=u''.encode( 'utf-8' ),
                )
                print_bitbar_line(
                    title=( u'Mark all %s notifications as read' % len( github_notifications ) ).encode( 'utf-8' ),
                    refresh='true',
                    bash=__file__,
                    terminal='false',
                    param1='readall',
                )
        else:
            print_bitbar_line(
                title=u'GitHub \u2014 No new notifications'.encode( 'utf-8' ),
                color=inactive,
                href='https://github.com',
            )

    # print_bitbar_line( title='---' )

    # print_bitbar_line( title='Refresh', refresh='true' )

    if is_github_enterprise_defined:
        if len( enterprise_notifications ):
            if is_github_defined:
                print '---'
            print_bitbar_line(
                title=( u'GitHub:Enterprise \u2014 %s' % plural( 'notification', len( enterprise_notifications ) ) ).encode( 'utf-8' ),
                color=active,
                href='%s/notifications' % re.sub( '/api/v3', '',  enterprise_api_url ),
            )
            print_notifications( enterprise_notifications, enterprise=True )
        else:
            print '---'
            print_bitbar_line(
                title=u'GitHub:Enterprise \u2014 No new notifications',
                color=inactive,
            )
