import React, { useState } from 'react';
import { ChevronRight, MessageSquare, Lightbulb, Calendar, User, Copy, Check, Edit2, LogOut } from 'lucide-react';

const Profile = ({ user, onUpdateProfile, onTabChange, onLogout }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editName, setEditName] = useState(user.name);
    const [copiedField, setCopiedField] = useState(null);

    const handleCopy = (text, field) => {
        navigator.clipboard.writeText(text);
        setCopiedField(field);
        setTimeout(() => setCopiedField(null), 2000);
    };

    const handleSaveName = () => {
        onUpdateProfile(editName);
        setIsEditing(false);
    };

    return (
        <div className="flex flex-col h-full bg-white overflow-y-auto">
            {/* Header */}
            <div className="bg-gradient-to-r from-teal-400 to-purple-600 p-8 text-white flex items-center space-x-6">
                <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center text-teal-600 text-3xl font-bold shadow-lg">
                    {user.avatar && !user.avatar.includes('ui-avatars') ? (
                        <img src={user.avatar} alt={user.name} className="w-full h-full rounded-full object-cover" />
                    ) : (
                        user.name.charAt(0).toUpperCase()
                    )}
                </div>
                <div>
                    <h1 className="text-3xl font-bold">{user.name}</h1>
                    <p className="opacity-90">{user.email}</p>
                </div>
            </div>

            <div className="p-6 max-w-4xl mx-auto w-full space-y-8">
                {/* Account Information */}
                <div>
                    <h2 className="text-lg font-semibold text-gray-800 mb-4">Account Information</h2>
                    <div className="bg-white rounded-lg border border-gray-200 divide-y divide-gray-100 shadow-sm">
                        {/* Name */}
                        <div className="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
                            <div className="flex-1">
                                <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Name</p>
                                {isEditing ? (
                                    <div className="flex items-center space-x-2">
                                        <input
                                            type="text"
                                            value={editName}
                                            onChange={(e) => setEditName(e.target.value)}
                                            className="border border-gray-300 rounded px-2 py-1 text-gray-800 focus:outline-none focus:border-teal-500"
                                            autoFocus
                                        />
                                        <button onClick={handleSaveName} className="text-teal-600 hover:text-teal-700 font-medium text-sm">Save</button>
                                        <button onClick={() => setIsEditing(false)} className="text-gray-500 hover:text-gray-700 text-sm">Cancel</button>
                                    </div>
                                ) : (
                                    <p className="text-gray-900 font-medium text-lg">{user.name}</p>
                                )}
                            </div>
                            {!isEditing && (
                                <button onClick={() => { setEditName(user.name); setIsEditing(true); }} className="text-teal-600 hover:text-teal-700">
                                    <Edit2 size={18} />
                                </button>
                            )}
                        </div>

                        {/* Email */}
                        <div className="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
                            <div>
                                <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Email</p>
                                <p className="text-gray-900 font-medium">{user.email}</p>
                            </div>
                        </div>

                        {/* User ID */}
                        <div className="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
                            <div>
                                <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">User ID</p>
                                <p className="text-gray-500 font-mono text-sm">{user.id}</p>
                            </div>
                            <button
                                onClick={() => handleCopy(user.id.toString(), 'userId')}
                                className="text-teal-600 hover:text-teal-700 text-sm font-medium flex items-center"
                            >
                                {copiedField === 'userId' ? <span className="flex items-center"><Check size={14} className="mr-1" /> Copied</span> : "Copy"}
                            </button>
                        </div>

                        {/* Workspace ID (Mock) */}
                        <div className="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
                            <div>
                                <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Workspace ID</p>
                                <p className="text-gray-500 font-mono text-sm">f85b4d62-d3b4-4bac-ad45-984865ee9e13</p>
                            </div>
                            <button
                                onClick={() => handleCopy("f85b4d62-d3b4-4bac-ad45-984865ee9e13", 'workspaceId')}
                                className="text-teal-600 hover:text-teal-700 text-sm font-medium flex items-center"
                            >
                                {copiedField === 'workspaceId' ? <span className="flex items-center"><Check size={14} className="mr-1" /> Copied</span> : "Copy"}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Settings */}
                <div>
                    <h2 className="text-lg font-semibold text-gray-800 mb-4">Settings</h2>
                    <div className="bg-white rounded-lg border border-gray-200 divide-y divide-gray-100 shadow-sm">
                        <button onClick={() => onTabChange('chats')} className="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors text-left">
                            <div className="flex items-center space-x-3">
                                <MessageSquare className="text-purple-500" size={20} />
                                <span className="text-gray-900 font-medium">Chats</span>
                            </div>
                            <ChevronRight className="text-gray-400" size={20} />
                        </button>
                        <button onClick={() => onTabChange('ideas')} className="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors text-left">
                            <div className="flex items-center space-x-3">
                                <Lightbulb className="text-yellow-500" size={20} />
                                <span className="text-gray-900 font-medium">Ideas Hub</span>
                            </div>
                            <ChevronRight className="text-gray-400" size={20} />
                        </button>
                        <button onClick={() => onTabChange('calendar')} className="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition-colors text-left">
                            <div className="flex items-center space-x-3">
                                <Calendar className="text-blue-500" size={20} />
                                <span className="text-gray-900 font-medium">Calendar</span>
                            </div>
                            <ChevronRight className="text-gray-400" size={20} />
                        </button>
                    </div>
                </div>

                {/* Logout Button */}
                <div className="pt-4">
                    <button onClick={onLogout} className="w-full p-4 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 font-medium transition-colors flex items-center justify-center space-x-2">
                        <LogOut size={20} />
                        <span>Logout</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Profile;
