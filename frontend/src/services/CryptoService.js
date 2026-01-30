// CryptoService.js - Handles E2E Encryption Keys using Web Crypto API

const CryptoService = {
    // Generate ECDH Key Pair (Identity Key)
    generateKeyPair: async () => {
        try {
            const keyPair = await window.crypto.subtle.generateKey(
                {
                    name: "ECDH",
                    namedCurve: "P-256",
                },
                true, // extractable
                ["deriveKey", "deriveBits"]
            );
            return keyPair;
        } catch (e) {
            console.error("Key Gen Error", e);
            throw e;
        }
    },

    // Export Key to JWK (JSON) for transport
    exportKey: async (key) => {
        return await window.crypto.subtle.exportKey("jwk", key);
    },

    // Import Key from JWK
    importKey: async (jwkData, type = 'public') => { // type: 'public' or 'private'
        return await window.crypto.subtle.importKey(
            "jwk",
            jwkData,
            {
                name: "ECDH",
                namedCurve: "P-256",
            },
            true,
            type === 'public' ? [] : ["deriveKey", "deriveBits"]
        );
    },

    // Upload keys to backend
    uploadKeys: async (user, keyPair) => {
        const publicJwk = await CryptoService.exportKey(keyPair.publicKey);
        // In a real app, we'd store private key in IndexedDB securely.
        // For prototype, we might store in localStorage (NOT SECURE for production)
        // or re-generate on login (which resets identity, bad for Signal).
        // Let's store in localStorage for MVP persistence across refreshes.

        // Serialize private key
        const privateJwk = await CryptoService.exportKey(keyPair.privateKey);
        localStorage.setItem(`priv_key_${user.id}`, JSON.stringify(privateJwk));
        localStorage.setItem(`pub_key_${user.id}`, JSON.stringify(publicJwk));

        const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

        await fetch(`${API_URL}/keys`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: user.id,
                public_key: JSON.stringify(publicJwk),
                pre_key_bundle: null // Optional: Add PreKeys logic later
            })
        });
        console.log("Keys uploaded for user", user.id);
    },

    // Initialize (Check if keys exist, else generate and upload)
    initialize: async (user) => {
        if (!user || !user.id) return;

        const existingPriv = localStorage.getItem(`priv_key_${user.id}`);
        if (!existingPriv) {
            console.log("Generating new keys for", user.id);
            const keyPair = await CryptoService.generateKeyPair();
            await CryptoService.uploadKeys(user, keyPair);
        } else {
            console.log("Keys already exist for", user.id);
            // Optionally re-upload public key to ensure server has it
            const existingPub = localStorage.getItem(`pub_key_${user.id}`);
            if (existingPub) {
                const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
                await fetch(`${API_URL}/keys`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: user.id,
                        public_key: existingPub
                    })
                });
            }
        }
    }
};

export default CryptoService;
