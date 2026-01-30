import React, { useState, useEffect } from 'react';
import { Plus, Image as ImageIcon, Type, MoreVertical } from 'lucide-react';
import StatusViewer from './StatusViewer';

const StatusTab = ({ currentUser }) => {
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const [statuses, setStatuses] = useState([]);
    const [viewingUser, setViewingUser] = useState(null); // User whose stories we are viewing
    const [showUpload, setShowUpload] = useState(false);
    const [uploadType, setUploadType] = useState('text'); // 'text' or 'image'

    // Upload State
    const [textStatus, setTextStatus] = useState('');
    const [imageFile, setImageFile] = useState(null);
    const [caption, setCaption] = useState('');

    useEffect(() => {
        fetchStatuses();
    }, []);

    const fetchStatuses = () => {
        if (!currentUser) return;
        fetch(`${API_URL}/status?user_id=${currentUser.id}`)
            .then(res => res.json())
            .then(data => setStatuses(data))
            .catch(err => console.error("Failed to fetch statuses", err));
    };

    const handleUpload = async () => {
        let content = textStatus;
        if (uploadType === 'image' && imageFile) {
            const formData = new FormData();
            formData.append('file', imageFile);
            try {
                const uploadRes = await fetch(`${API_URL}/upload`, { method: 'POST', body: formData });
                const uploadData = await uploadRes.json();
                content = uploadData.url;
            } catch (e) {
                console.error("Upload failed", e);
                return;
            }
        }

        const newStatus = {
            user_id: currentUser.id,
            type: uploadType,
            content: content,
            caption: caption
        };

        fetch(`${API_URL}/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newStatus)
        })
            .then(() => {
                setShowUpload(false);
                setTextStatus('');
                setImageFile(null);
                setCaption('');
                fetchStatuses(); // Refresh
            });
    };

    // My Status
    const myStatusGroup = statuses.find(s => String(s.user_id) === String(currentUser?.id));
    const otherStatuses = statuses.filter(s => String(s.user_id) !== String(currentUser?.id));

    return (
        <div className="h-full bg-white flex flex-col">
            {/* Header */}
            <div className="p-4 border-b flex justify-between items-center bg-gray-50">
                <h2 className="text-xl font-bold text-gray-800">Status</h2>
                <div className="flex space-x-2">
                    <button onClick={() => { setUploadType('text'); setShowUpload(true); }} className="p-2 bg-gray-200 rounded-full hover:bg-gray-300">
                        <Type size={20} className="text-gray-700" />
                    </button>
                    <button onClick={() => { setUploadType('image'); setShowUpload(true); }} className="p-2 bg-gray-200 rounded-full hover:bg-gray-300">
                        <ImageIcon size={20} className="text-gray-700" />
                    </button>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {/* My Status */}
                <div className="flex items-center space-x-4 cursor-pointer" onClick={() => myStatusGroup && setViewingUser(myStatusGroup)}>
                    <div className="relative">
                        <img
                            src={currentUser?.avatar || "https://ui-avatars.com/api/?background=random"}
                            alt="My Status"
                            className={`w-14 h-14 rounded-full border-2 ${myStatusGroup ? 'border-teal-500 p-0.5' : 'border-gray-300'}`}
                        />
                        {!myStatusGroup && (
                            <div className="absolute bottom-0 right-0 bg-teal-500 text-white rounded-full p-1 border-2 border-white">
                                <Plus size={12} />
                            </div>
                        )}
                    </div>
                    <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">My Status</h3>
                        <p className="text-sm text-gray-500">
                            {myStatusGroup ? `Last updated ${new Date(myStatusGroup.stories[myStatusGroup.stories.length - 1].timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}` : 'Tap to add status update'}
                        </p>
                    </div>
                </div>

                <hr />

                {/* Recent Updates */}
                <div>
                    <h3 className="text-sm font-semibold text-gray-500 mb-4 uppercase">Recent updates</h3>
                    {otherStatuses.map(group => (
                        <div key={group.user_id} className="flex items-center space-x-4 mb-4 cursor-pointer" onClick={() => setViewingUser(group)}>
                            <img
                                src={group.avatar}
                                alt={group.name}
                                className="w-14 h-14 rounded-full border-2 border-teal-500 p-0.5"
                            />
                            <div>
                                <h4 className="font-semibold text-gray-900">{group.name}</h4>
                                <p className="text-sm text-gray-500">
                                    {new Date(group.stories[group.stories.length - 1].timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </p>
                            </div>
                        </div>
                    ))}
                    {otherStatuses.length === 0 && (
                        <p className="text-gray-400 text-sm italic">No recent updates from contacts.</p>
                    )}
                </div>
            </div>

            {/* Viewer Modal */}
            {viewingUser && (
                <StatusViewer
                    statusGroup={viewingUser}
                    onClose={() => setViewingUser(null)}
                    currentUser={currentUser}
                />
            )}

            {/* Upload Modal */}
            {showUpload && (
                <div className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-xl w-full max-w-md overflow-hidden relative">
                        <div className="p-4 bg-teal-600 text-white flex justify-between items-center">
                            <h3 className="font-bold">{uploadType === 'text' ? 'Type a status' : 'Upload Image'}</h3>
                            <button onClick={() => setShowUpload(false)}><Plus size={24} className="transform rotate-45" /></button>
                        </div>
                        <div className="p-6 space-y-4">
                            {uploadType === 'text' ? (
                                <textarea
                                    className="w-full h-40 bg-gray-100 p-4 rounded-lg text-xl text-center focus:outline-none resize-none"
                                    placeholder="Type a status..."
                                    value={textStatus}
                                    onChange={e => setTextStatus(e.target.value)}
                                    style={{ backgroundColor: textStatus.length > 50 ? '#ffeb3b' : '#e0f2f1' }} // Simple dynamic bg
                                />
                            ) : (
                                <div className="space-y-2">
                                    <input type="file" accept="image/*" onChange={e => setImageFile(e.target.files[0])} />
                                    {imageFile && (
                                        <img src={URL.createObjectURL(imageFile)} alt="Preview" className="w-full h-48 object-cover rounded-lg" />
                                    )}
                                    <input
                                        type="text"
                                        placeholder="Add a caption..."
                                        className="w-full border p-2 rounded"
                                        value={caption}
                                        onChange={e => setCaption(e.target.value)}
                                    />
                                </div>
                            )}
                            <button
                                onClick={handleUpload}
                                className="w-full bg-teal-600 text-white py-3 rounded-lg font-semibold hover:bg-teal-700"
                            >
                                Send
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default StatusTab;
