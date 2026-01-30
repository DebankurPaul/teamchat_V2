import React, { useState, useEffect } from 'react';
import { X, ChevronLeft, ChevronRight, Eye } from 'lucide-react';

const StatusViewer = ({ statusGroup, onClose, currentUser }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const stories = statusGroup.stories;
    const currentStory = stories[currentIndex];
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    useEffect(() => {
        // Auto-advance logic could go here (e.g. 5 seconds)
        const timer = setTimeout(() => {
            handleNext();
        }, 5000);

        // Mark as viewed
        if (currentUser && currentStory) {
            fetch(`${API_URL}/status/${currentStory.id}/view`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: currentUser.id })
            });
        }

        return () => clearTimeout(timer);
    }, [currentIndex]);

    const handleNext = () => {
        if (currentIndex < stories.length - 1) {
            setCurrentIndex(currentIndex + 1);
        } else {
            onClose(); // Close if last story
        }
    };

    const handlePrev = () => {
        if (currentIndex > 0) {
            setCurrentIndex(currentIndex - 1);
        }
    };

    return (
        <div className="fixed inset-0 bg-black z-50 flex flex-col items-center justify-center">
            {/* Progress Bar */}
            <div className="absolute top-2 left-0 right-0 flex space-x-1 px-2 z-10">
                {stories.map((_, idx) => (
                    <div key={idx} className="h-1 flex-1 bg-gray-600 rounded overflow-hidden">
                        <div
                            className={`h-full bg-white transition-all duration-[5000ms] ease-linear ${idx === currentIndex ? 'w-full' : (idx < currentIndex ? 'w-full' : 'w-0')}`}
                        />
                    </div>
                ))}
            </div>

            {/* Header */}
            <div className="absolute top-6 left-0 right-0 p-4 flex items-center justify-between text-white z-10">
                <div className="flex items-center space-x-2">
                    <img src={statusGroup.avatar} className="w-10 h-10 rounded-full border border-white" alt="User" />
                    <div className="flex flex-col">
                        <span className="font-semibold text-sm">{statusGroup.name}</span>
                        <span className="text-xs text-gray-300">{new Date(currentStory.timestamp).toLocaleTimeString()}</span>
                    </div>
                </div>
                <button onClick={onClose}><X size={24} /></button>
            </div>

            {/* Content */}
            <div className="w-full h-full flex items-center justify-center relative">
                {/* Nav Buttons (Hit areas) */}
                <div className="absolute left-0 top-0 bottom-0 w-1/3 z-20" onClick={handlePrev}></div>
                <div className="absolute right-0 top-0 bottom-0 w-1/3 z-20" onClick={handleNext}></div>

                {currentStory.type === 'image' ? (
                    <div className="relative w-full h-full flex items-center justify-center bg-black">
                        <img
                            src={currentStory.content.startsWith('http') ? currentStory.content : `${API_URL}${currentStory.content}`}
                            alt="Story"
                            className="max-h-full max-w-full object-contain"
                        />
                        {currentStory.caption && (
                            <div className="absolute bottom-20 left-0 right-0 text-center text-white bg-black bg-opacity-50 p-2">
                                {currentStory.caption}
                            </div>
                        )}
                    </div>
                ) : (
                    <div
                        className="w-full h-full flex items-center justify-center p-8 text-center text-white text-2xl font-bold"
                        style={{ backgroundColor: '#26a69a' }} // Default teal, could be dynamic
                    >
                        {currentStory.content}
                    </div>
                )}
            </div>

            {/* Footer / Views (Only for me) */}
            {String(statusGroup.user_id) === String(currentUser?.id) && (
                <div className="absolute bottom-4 left-0 right-0 text-center text-white flex justify-center items-center space-x-2">
                    <Eye size={16} />
                    <span>{currentStory.viewers ? currentStory.viewers.length : 0} views</span>
                </div>
            )}
        </div>
    );
};

export default StatusViewer;
