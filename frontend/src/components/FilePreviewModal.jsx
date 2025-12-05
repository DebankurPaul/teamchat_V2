import React, { useState, useEffect } from 'react';
import { X, Send, FileText, Plus } from 'lucide-react';

const FilePreviewModal = ({ file, onSend, onClose, onAddFile }) => {
    const [caption, setCaption] = useState('');
    const [previewUrl, setPreviewUrl] = useState(null);

    useEffect(() => {
        if (file) {
            if (file.type.startsWith('image/')) {
                const url = URL.createObjectURL(file);
                setPreviewUrl(url);
                return () => URL.revokeObjectURL(url);
            } else {
                setPreviewUrl(null);
            }
        }
    }, [file]);

    if (!file) return null;

    const formatSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex flex-col items-center justify-center text-white">
            {/* Header */}
            <div className="absolute top-0 left-0 right-0 p-4 flex justify-between items-center bg-black bg-opacity-50">
                <button onClick={onClose} className="p-2 hover:bg-gray-800 rounded-full">
                    <X size={24} />
                </button>
                <span className="font-medium truncate max-w-md">{file.name}</span>
                <div className="w-8"></div> {/* Spacer for centering */}
            </div>

            {/* Preview Area */}
            <div className="flex-1 flex items-center justify-center w-full p-8 overflow-hidden">
                {previewUrl ? (
                    <img src={previewUrl} alt="Preview" className="max-h-full max-w-full object-contain rounded-lg shadow-lg" />
                ) : (
                    <div className="flex flex-col items-center justify-center p-12 bg-gray-800 rounded-xl">
                        <FileText size={64} className="text-gray-400 mb-4" />
                        <p className="text-xl font-medium">No preview available</p>
                        <p className="text-sm text-gray-400 mt-2">{formatSize(file.size)} - {file.name.split('.').pop().toUpperCase()}</p>
                    </div>
                )}
            </div>

            {/* Footer / Input */}
            <div className="w-full max-w-3xl p-4 mb-4">
                <div className="flex items-center space-x-2 bg-gray-800 rounded-full px-4 py-2">
                    <button onClick={onAddFile} className="p-2 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors">
                        <Plus size={20} />
                    </button>
                    <input
                        type="text"
                        placeholder="Type a message"
                        className="flex-1 bg-transparent border-none focus:ring-0 text-white placeholder-gray-400"
                        value={caption}
                        onChange={(e) => setCaption(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && onSend(file, caption)}
                    />
                    <button
                        onClick={() => onSend(file, caption)}
                        className="p-3 bg-teal-500 rounded-full hover:bg-teal-600 transition-colors shadow-lg"
                    >
                        <Send size={20} className="ml-0.5" />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FilePreviewModal;
