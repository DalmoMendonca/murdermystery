# iPhone image saving

`/iphone/` preloads all thirty public character JPEGs and the invitation JPEG, then offers a native file share on a direct user tap. The payload contains only 31 `File` objects with `image/jpeg` MIME types. No URL or text accompanies the files, preserving the image-only share actions. The user chooses Save Images in Safari's native share sheet; the page cannot perform that device permission step itself.

`scripts/export_phone_images.py` produces the flat 31-image ZIP, public invite JPEG and exact manifest. The normal build invokes it after poster exports, keeping the phone page current.

QA: mobile 390 × 844 and desktop 1280 × 800 renders inspected; no horizontal overflow or script errors. Browser automation verified the preloaded 31-file JPEG handoff using a mocked native share receiver and verified the unsupported-browser individual-image fallback. Native iPhone Photos saving requires device verification; no claim that the files are already in the user's photo library. Individual images remain available for Safari's touch-and-hold saving if bulk file sharing is unavailable.
