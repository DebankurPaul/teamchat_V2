import React from 'react';
import { MessageSquare, Lightbulb, Calendar, User } from 'lucide-react';

const BottomNav = () => {
    const [activeTab, setActiveTab] = React.useState('chats');

    const navItems = [
        { id: 'chats', icon: MessageSquare, label: 'Chats' },
        { id: 'ideas', icon: Lightbulb, label: 'Ideas' },
        { id: 'calendar', icon: Calendar, label: 'Calendar' },
        { id: 'profile', icon: User, label: 'Profile' },
    ];

    return (
        <div className="h-16 bg-white border-t border-gray-200 flex items-center justify-around px-2 md:hidden">
            {navItems.map((item) => (
                <button
                    key={item.id}
                    onClick={() => setActiveTab(item.id)}
                    className={`flex flex-col items-center justify-center w-full h-full space-y-1 ${activeTab === item.id ? 'text-teal-600' : 'text-gray-500 hover:text-gray-700'
                        }`}
                >
                    <item.icon size={24} />
                    <span className="text-xs font-medium">{item.label}</span>
                </button>
            ))}
        </div>
    );
};

export default BottomNav;
