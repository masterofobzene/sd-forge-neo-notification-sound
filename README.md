# Notification Sound for Forge Neo

Plays a sound through Python when a generation job finishes, so it works even when the
browser is minimized or in the background. Windows only.

## Install

1. Open the **Extensions** tab → **Install from URL**
2. Paste this repo's URL and click **Install**
3. __Fully restart__ the WebUI (a UI reload is not enough)

## Sound file

Uses `notification.mp3` from the extension folder if present, otherwise from the WebUI root
folder. Put your own `notification.mp3` in either place.

Respects the existing `notification_audio` and `notification_volume` settings.

