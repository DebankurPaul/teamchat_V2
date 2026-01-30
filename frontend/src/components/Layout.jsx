import React, { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import ChatWindow from './ChatWindow';
import IdeaHub from './IdeaHub';
import StatusTab from './StatusTab';
import CalendarView from './CalendarView';

import Login from './Login';
import Register from './Register';
import Profile from './Profile';
import ConfirmationModal from './ConfirmationModal';
import Toast from './Toast';
import { Edit2, Menu } from 'lucide-react';
import CryptoService from '../services/CryptoService';
import SetUsername from './SetUsername';

const Layout = () => {
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const [user, setUser] = useState(null); // Auth state
  const [isRegistering, setIsRegistering] = useState(false);
  const [selectedChat, setSelectedChat] = useState(null);
  const [activeTab, setActiveTab] = useState('chats'); // chats, ideas, calendar, profile
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false); // Controls sidebar visibility on mobile for non-chat tabs

  // Confirmation Modal State
  const [confirmation, setConfirmation] = useState({
    isOpen: false,
    title: '',
    message: '',
    onConfirm: () => { },
    isDanger: false
  });

  const [toast, setToast] = useState(null);

  const showNotification = (message) => {
    setToast(message);
    setTimeout(() => setToast(null), 3000);
  };

  // Lifted Chats State
  const [chats, setChats] = useState([]);
  const [userStatuses, setUserStatuses] = useState({}); // userId -> {status, lastSeen}

  // WebSocket Connection
  useEffect(() => {
    if (user) {
      const wsUrl = API_URL.replace('http', 'ws');
      const ws = new WebSocket(`${wsUrl}/ws/${user.id}`);

      ws.onopen = () => {
        console.log("Connected to WebSocket");
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'status_update') {
            setUserStatuses(prev => ({
              ...prev,
              [data.userId]: { status: data.status, lastSeen: new Date().toLocaleTimeString() }
            }));
          }
        } catch (e) {
          console.error("Error parsing WS message", e);
        }
      };

      return () => {
        ws.close();
      };
    }
  }, [user]);

  // key Init
  useEffect(() => {
    if (user) {
      CryptoService.initialize(user).catch(err => console.error("Crypto Init Failed", err));
    }
  }, [user]);

  // Fetch chats on mount
  useEffect(() => {
    fetch(`${API_URL}/chats`)
      .then(res => res.json())
      .then(data => {
        console.log("Fetched chats:", data);
        setChats(data);
      })
      .catch(err => console.error("Failed to fetch chats", err));
  }, [user]);

  // Public Groups State
  const [publicGroups, setPublicGroups] = useState([]);

  // Fetch public groups
  useEffect(() => {
    fetch(`${API_URL}/chats/public`)
      .then(res => res.json())
      .then(data => setPublicGroups(data))
      .catch(err => console.error("Failed to fetch public groups", err));
  }, [chats]); // Refresh when chats change (e.g. after creating a group)


  // Auth Flow
  if (!user) {
    if (isRegistering) {
      return <Register onRegister={(userData) => setUser(userData)} onSwitchToLogin={() => setIsRegistering(false)} showNotification={showNotification} />;
    }
    return <Login onLogin={(userData) => setUser(userData)} onSwitchToRegister={() => setIsRegistering(true)} showNotification={showNotification} />;
  }

  // Require Username
  if (!user.username) {
    return (
      <SetUsername
        user={user}
        onUsernameSet={(newUsername) => {
          setUser(prev => ({ ...prev, username: newUsername, name: newUsername }));
          showNotification(`Welcome, ${newUsername}!`);
        }}
      />
    );
  }

  const handleSelectChat = (chat) => {
    // Mark as read (Optimistic update)
    const updatedChats = chats.map(c =>
      c.id === chat.id ? { ...c, unread: 0 } : c
    );
    setChats(updatedChats);
    setSelectedChat({ ...chat, unread: 0 });
  };

  const handleDeleteChat = (chatId) => {
    setConfirmation({
      isOpen: true,
      title: 'Delete Chat',
      message: 'Are you sure you want to delete this chat? This action cannot be undone.',
      isDanger: true,
      onConfirm: () => {
        fetch(`${API_URL}/chats/${chatId}`, { method: 'DELETE' })
          .then(res => {
            if (!res.ok) throw new Error("Failed to delete chat");
            return res.json();
          })
          .then(() => {
            setChats(chats.filter(c => c.id !== chatId));
            setSelectedChat(null);
          })
          .catch(err => {
            console.error("Failed to delete chat", err);
            showNotification("Failed to delete chat. Please try again.");
          });
      }
    });
  };

  const handleBulkDelete = (chatIds) => {
    setConfirmation({
      isOpen: true,
      title: 'Delete Selected Chats',
      message: `Are you sure you want to delete ${chatIds.length} chats? This action cannot be undone.`,
      isDanger: true,
      onConfirm: () => {
        Promise.all(chatIds.map(id =>
          fetch(`${API_URL}/chats/${id}`, { method: 'DELETE' })
            .then(res => { if (!res.ok) throw new Error(`Failed to delete ${id}`); })
        ))
          .then(() => {
            setChats(chats.filter(c => !chatIds.includes(c.id)));
            if (selectedChat && chatIds.includes(selectedChat.id)) {
              setSelectedChat(null);
            }
          })
          .catch(err => {
            console.error("Failed to delete chats", err);
            showNotification("Failed to delete some chats.");
          });
      }
    });
  };

  const handleCreateGroup = (newGroup) => {
    const groupWithCreator = {
      ...newGroup,
      participants: user ? [user] : [],
      members: 1,
      createdBy: user ? { name: user.name, email: user.email } : null
    };

    fetch(`${API_URL}/chats`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(groupWithCreator)
    })
      .then(res => res.json())
      .then(createdGroup => {
        setChats(prevChats => [createdGroup, ...prevChats]);
        setSelectedChat(createdGroup);
      })
      .catch(err => {
        console.error("Failed to create group", err);
        showNotification("Failed to create group. Please try again.");
      });
  };

  const handleJoinGroup = (group) => {
    if (!user) return;

    // Use the add_participant endpoint to add self
    fetch(`${API_URL}/chats/${group.id}/participants`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: user.email })
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to join group");
        return res.json();
      })
      .then(() => {
        // Refresh chats to show the new group
        return fetch(`${API_URL}/chats`);
      })
      .then(res => res.json())
      .then(data => {
        // Find joined chat
        const joinedChat = data.find(c => c.id === group.id);

        if (joinedChat) {
          // Mark as read immediately
          const updatedData = data.map(c => c.id === group.id ? { ...c, unread: 0 } : c);
          setChats(updatedData);
          setSelectedChat({ ...joinedChat, unread: 0 });
        } else {
          setChats(data);
        }
      })
      .catch(err => {
        console.error("Join group error", err);
        showNotification("Failed to join group");
      });
  };


  const handleUpdateProfile = (updates) => {
    // updates = { name, about, avatar }
    if (!updates) return;

    fetch(`${API_URL}/users/${user.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    })
      .then(res => res.json())
      .then(data => {
        // Update local user state
        // API returns { status: "updated" }, doesn't return full user.
        // We should merge updates into local state.
        setUser(prev => ({ ...prev, ...updates }));
        showNotification("Profile updated successfully");
      })
      .catch(err => {
        console.error("Failed to update profile", err);
        showNotification("Failed to update profile");
      });
  };

  const renderMainContent = () => {
    switch (activeTab) {
      case 'chats':
        return selectedChat ? (
          <ChatWindow
            chat={selectedChat}
            chats={chats}
            userStatuses={userStatuses}
            currentUser={user}
            onBack={() => setSelectedChat(null)}
            onDeleteChat={handleDeleteChat}
          />
        ) : (
          <div className="hidden md:flex items-center justify-center h-full bg-[#f0f2f5] text-gray-500">
            Select a chat to start messaging
          </div>
        );
      case 'status':
        return <StatusTab currentUser={user} />;
      case 'ideas':
        return <IdeaHub />;
      case 'calendar':
        return <CalendarView />;
      case 'profile':
        return (
          <Profile
            user={user}
            onUpdateProfile={handleUpdateProfile}
            onTabChange={setActiveTab}
            onLogout={() => setUser(null)}
          />
        );
      default:
        return null;
    }
  };

  // Helper logic for mobile visibility
  const isMobileDetailOpen = selectedChat || (activeTab !== 'chats' && !mobileMenuOpen);

  const MobileHeader = ({ title }) => (
    <div className="md:hidden flex items-center p-4 bg-white border-b sticky top-0 z-10">
      <button
        onClick={() => setMobileMenuOpen(true)}
        className="mr-3 p-2 hover:bg-gray-100 rounded-full"
      >
        <Menu size={24} />
      </button>
      <h2 className="text-xl font-bold">{title}</h2>
    </div>
  );

  return (
    <div className="flex h-[100dvh] md:h-screen bg-gray-100 overflow-hidden">
      {/* Sidebar (Hidden on mobile if detail view is open) */}
      <div className={`${isMobileDetailOpen ? 'hidden md:flex' : 'flex'} w-full md:w-auto flex-col h-full`}>
        <Sidebar
          chats={chats}
          publicGroups={publicGroups}
          onSelectChat={handleSelectChat}
          onCreateGroup={handleCreateGroup}
          onJoinGroup={handleJoinGroup}
          activeTab={activeTab}
          onTabChange={(tab) => {
            setActiveTab(tab);
            setMobileMenuOpen(false); // Close menu (show content) when tab changes
          }}
          onLogout={() => setUser(null)}
          currentUser={user}
          onBulkDelete={handleBulkDelete}
          showNotification={showNotification}
          onUpdateProfile={handleUpdateProfile}
        />

      </div>

      {/* Main Content Area */}
      <div className={`flex-1 h-full ${!isMobileDetailOpen ? 'hidden md:block' : 'block'} flex flex-col`}>
        {activeTab !== 'chats' && !selectedChat && (
          <MobileHeader title={activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} />
        )}
        <div className="flex-1 overflow-hidden relative">
          {renderMainContent()}
        </div>
      </div>

      {/* Confirmation Modal */}
      <ConfirmationModal
        isOpen={confirmation.isOpen}
        onClose={() => setConfirmation({ ...confirmation, isOpen: false })}
        onConfirm={confirmation.onConfirm}
        title={confirmation.title}
        message={confirmation.message}
        isDanger={confirmation.isDanger}
        confirmText="Delete"
      />
      <Toast message={toast} onClose={() => setToast(null)} />
    </div>
  );
};

export default Layout;
