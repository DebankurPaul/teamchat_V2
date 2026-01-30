
import React, { useState } from 'react';
import { User, Check, ArrowRight, AlertCircle } from 'lucide-react';

const SetUsername = ({ user, onUsernameSet }) => {
    const [username, setUsername] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (username.length < 3) {
            setError('Username must be at least 3 characters long');
            return;
        }

        setLoading(true);

        try {
            const response = await fetch(`${API_URL}/set_username`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: user.id,
                    username: username
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to set username');
            }

            onUsernameSet(username);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
            <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="bg-teal-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-teal-600">
                        <User size={32} />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-800">Choose a Username</h2>
                    <p className="text-gray-500 text-sm mt-2">
                        Create a unique username to identify yourself in the chat.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Username</label>
                        <div className="mt-1 relative rounded-md shadow-sm">
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className={`block w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 ${error ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : 'border-gray-300'
                                    }`}
                                placeholder="coolUser123"
                                required
                            />
                        </div>
                        {error && (
                            <div className="mt-2 text-sm text-red-600 flex items-center">
                                <AlertCircle size={16} className="mr-1" />
                                {error}
                            </div>
                        )}
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50 transition-colors"
                    >
                        {loading ? 'Setting Username...' : (
                            <>
                                Continue <ArrowRight size={18} className="ml-2" />
                            </>
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default SetUsername;
