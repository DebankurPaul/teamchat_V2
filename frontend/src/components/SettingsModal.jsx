import React, { useState, useEffect } from 'react';
import { X, User, Lock, Save, Camera } from 'lucide-react';

const SettingsModal = ({ isOpen, onClose, currentUser, onUpdateProfile }) => {
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    // Tabs: 'profile', 'privacy'
    const [activeTab, setActiveTab] = useState('profile');

    // Profile State
    const [name, setName] = useState(currentUser?.name || '');
    const [about, setAbout] = useState(currentUser?.about || 'Available');
    const [avatar, setAvatar] = useState(currentUser?.avatar || '');

    // Privacy State
    const [settings, setSettings] = useState({
        readReceipts: true,
        lastSeen: true,
        onlineStatus: true
    });

    useEffect(() => {
        if (currentUser) {
            setName(currentUser.name);
            setAvatar(currentUser.avatar);
            // Fetch settings
            fetch(`${API_URL}/users/${currentUser.id}/settings`)
                .then(res => res.json())
                .then(data => {
                    // Start with defaults and override
                    setSettings(prev => ({ ...prev, ...data }));
                })
                .catch(err => console.error("Failed to fetch settings", err));
        }
    }, [currentUser, isOpen]);

    const handleSaveProfile = () => {
        // Mock update for now or real endpoint if exists
        // Re-using specific fields update logic if endpoint supports it, 
        // or just local optimistic update + settings sync

        // We'll update settings for profile specific non-DB columns if needed, 
        // but core fields (name, avatar) usually go to a different endpoint.
        // Assuming we implement basic settings first.

        onUpdateProfile({ name, about, avatar });
        onClose();
    };

    const handleSavePrivacy = async () => {
        try {
            await fetch(`${API_URL}/users/${currentUser.id}/settings`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });
            // Also notify parent/global state if needed
            onClose();
        } catch (error) {
            console.error("Failed to save settings", error);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl w-full max-w-md shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
                {/* Header */}
                <div className="bg-teal-600 p-4 flex justify-between items-center text-white">
                    <h2 className="text-lg font-semibold">Settings</h2>
                    <button onClick={onClose} className="hover:bg-teal-700 p-1 rounded-full">
                        <X size={20} />
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex border-b border-gray-200">
                    <button
                        className={`flex-1 py-3 text-sm font-medium ${activeTab === 'profile' ? 'text-teal-600 border-b-2 border-teal-600' : 'text-gray-500 hover:text-gray-700'}`}
                        onClick={() => setActiveTab('profile')}
                    >
                        <User size={16} className="inline mr-2" />
                        Profile
                    </button>
                    <button
                        className={`flex-1 py-3 text-sm font-medium ${activeTab === 'privacy' ? 'text-teal-600 border-b-2 border-teal-600' : 'text-gray-500 hover:text-gray-700'}`}
                        onClick={() => setActiveTab('privacy')}
                    >
                        <Lock size={16} className="inline mr-2" />
                        Privacy
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 flex-1 overflow-y-auto">
                    {activeTab === 'profile' ? (
                        <div className="space-y-6">
                            <div className="flex flex-col items-center">
                                <div className="relative">
                                    <img src={avatar || "https://via.placeholder.com/150"} alt="Profile" className="w-24 h-24 rounded-full border-4 border-gray-100 shadow-sm" />
                                    <button className="absolute bottom-0 right-0 bg-teal-500 text-white p-2 rounded-full shadow-md hover:bg-teal-600">
                                        <Camera size={16} />
                                    </button>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Your Name</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full border-b-2 border-gray-200 focus:border-teal-500 outline-none p-2 transition-colors bg-gray-50 rounded-t"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">About</label>
                                <input
                                    type="text"
                                    value={about}
                                    onChange={(e) => setAbout(e.target.value)}
                                    className="w-full border-b-2 border-gray-200 focus:border-teal-500 outline-none p-2 transition-colors bg-gray-50 rounded-t"
                                />
                            </div>

                            <button onClick={handleSaveProfile} className="w-full bg-teal-600 text-white py-2 rounded-lg font-medium hover:bg-teal-700 flex items-center justify-center">
                                <Save size={18} className="mr-2" />
                                Save Profile
                            </button>
                        </div>
                    ) : (
                        <div className="space-y-6">
                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div>
                                    <h3 className="font-medium text-gray-800">Read Receipts</h3>
                                    <p className="text-xs text-gray-500">Show blue ticks when you read messages</p>
                                </div>
                                <div className="relative inline-block w-12 h-6 transition duration-200 ease-in-out rounded-full border-2 border-transparent">
                                    <input
                                        type="checkbox"
                                        checked={settings.readReceipts}
                                        onChange={(e) => setSettings({ ...settings, readReceipts: e.target.checked })}
                                        className="absolute w-6 h-6 opacity-0 cursor-pointer"
                                    />
                                    <span className={`block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer ${settings.readReceipts ? 'bg-teal-500' : ''}`}></span>
                                    <span className={`absolute block w-4 h-4 mt-1 ml-1 bg-white rounded-full shadow inset-y-0 left-0 focus-within:shadow-outline transition-transform duration-200 ease-in-out ${settings.readReceipts ? 'transform translate-x-6' : ''}`}></span>
                                </div>
                            </div>

                            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div>
                                    <h3 className="font-medium text-gray-800">Last Seen</h3>
                                    <p className="text-xs text-gray-500">Allow others to see when you were last active</p>
                                </div>
                                <div className="relative inline-block w-12 h-6 transition duration-200 ease-in-out rounded-full border-2 border-transparent">
                                    <input
                                        type="checkbox"
                                        checked={settings.lastSeen}
                                        onChange={(e) => setSettings({ ...settings, lastSeen: e.target.checked })}
                                        className="absolute w-6 h-6 opacity-0 cursor-pointer"
                                    />
                                    <span className={`block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer ${settings.lastSeen ? 'bg-teal-500' : ''}`}></span>
                                    <span className={`absolute block w-4 h-4 mt-1 ml-1 bg-white rounded-full shadow inset-y-0 left-0 focus-within:shadow-outline transition-transform duration-200 ease-in-out ${settings.lastSeen ? 'transform translate-x-6' : ''}`}></span>
                                </div>
                            </div>

                            <div className="mt-8 p-4 bg-yellow-50 rounded-lg border border-yellow-100">
                                <p className="text-xs text-yellow-800 flex items-start">
                                    <Lock size={12} className="mt-0.5 mr-1 flex-shrink-0" />
                                    Security Note: Changing these settings will update your privacy preferences immediately.
                                </p>
                            </div>

                            <button onClick={handleSavePrivacy} className="w-full bg-teal-600 text-white py-2 rounded-lg font-medium hover:bg-teal-700 flex items-center justify-center">
                                <Save size={18} className="mr-2" />
                                Save Privacy Settings
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default SettingsModal;
