import React, { useEffect, useRef, useState } from 'react';
import { PhoneOff } from 'lucide-react';

const VideoCall = ({ roomName, userName, onClose, isVoiceOnly = false }) => {
    const jitsiContainerRef = useRef(null);
    const [api, setApi] = useState(null);

    useEffect(() => {
        const domain = 'meet.jit.si';
        const options = {
            roomName: roomName,
            width: '100%',
            height: '100%',
            parentNode: jitsiContainerRef.current,
            userInfo: {
                displayName: userName
            },
            configOverwrite: {
                startWithAudioMuted: true,
                startWithVideoMuted: isVoiceOnly,
                prejoinPageEnabled: false // Skip prejoin for seamless entry
            },
            interfaceConfigOverwrite: {
                TOOLBAR_BUTTONS: [
                    'microphone', 'closedcaptions', 'desktop', 'fullscreen',
                    'fodeviceselection', 'hangup', 'profile', 'chat', 'recording',
                    'livestreaming', 'etherpad', 'sharedvideo', 'settings', 'raisehand',
                    'videoquality', 'filmstrip', 'invite', 'feedback', 'stats', 'shortcuts',
                    'tileview', 'videobackgroundblur', 'download', 'help', 'mute-everyone',
                    'security'
                ].concat(isVoiceOnly ? [] : ['camera']), // Only add camera if not voice-only
            },
        };

        // Load Jitsi script dynamically if not present
        if (!window.JitsiMeetExternalAPI) {
            const script = document.createElement('script');
            script.src = 'https://meet.jit.si/external_api.js';
            script.async = true;
            script.onload = () => {
                const newApi = new window.JitsiMeetExternalAPI(domain, options);
                setApi(newApi);
                newApi.addEventListeners({
                    videoConferenceLeft: () => onClose(),
                });
            };
            document.body.appendChild(script);
        } else {
            const newApi = new window.JitsiMeetExternalAPI(domain, options);
            setApi(newApi);
            newApi.addEventListeners({
                videoConferenceLeft: () => onClose(),
            });
        }

        return () => {
            if (api) {
                api.dispose();
            }
        };
    }, []);

    return (
        <div className="fixed inset-0 bg-black z-50 flex flex-col">
            <div ref={jitsiContainerRef} className="flex-1 w-full h-full" />
            <button
                onClick={onClose}
                className="absolute top-4 right-4 bg-red-600 hover:bg-red-700 text-white p-2 rounded-full shadow-lg z-50"
                title="Close Call Window"
            >
                <PhoneOff size={24} />
            </button>
        </div>
    );
};

export default VideoCall;
