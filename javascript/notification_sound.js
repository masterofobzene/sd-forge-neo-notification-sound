onAfterUiUpdate(function () {
    if (!navigator.userAgent.includes("Windows")) return;

    const audio = gradioApp()
        .querySelector("#audio_notification #waveform > div")
        ?.shadowRoot?.querySelector("audio");

    if (audio && !audio._pythonNotifPatched) {
        audio._pythonNotifPatched = true;
        audio.play = () => Promise.resolve();
    }
});