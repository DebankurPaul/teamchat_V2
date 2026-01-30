import React, { useState, useEffect } from 'react';
import { auth, MOCK_AUTH_MODE } from '../firebaseConfig';
import { RecaptchaVerifier, signInWithPhoneNumber } from "firebase/auth";
import { Phone, ArrowRight, Check } from 'lucide-react';

const Login = ({ onLogin, onSwitchToRegister, showNotification }) => {
    const [step, setStep] = useState('phone'); // phone, otp
    const [phone, setPhone] = useState('');
    const [otp, setOtp] = useState('');
    const [confirmationResult, setConfirmationResult] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!MOCK_AUTH_MODE && auth) {
            if (!window.recaptchaVerifier) {
                window.recaptchaVerifier = new RecaptchaVerifier(auth, 'recaptcha-container', {
                    'size': 'invisible',
                    'callback': (response) => {
                        // reCAPTCHA solved
                    },
                    'expired-callback': () => {
                        // Response expired
                    }
                });
            }
        }
    }, []);

    const handleSendOtp = async (e) => {
        e.preventDefault();
        setLoading(true);

        // Normalize phone: remove all non-numeric chars except leading +
        const phoneNumber = phone.replace(/[^+\d]/g, '');
        // Ensure + prefix if missing (though regex above handles keeps it, this ensures valid format)
        const formattedPhone = phoneNumber.startsWith('+') ? phoneNumber : `+${phoneNumber}`;

        try {
            if (MOCK_AUTH_MODE) {
                console.log("MOCK MODE: Simulating OTP sent to", phoneNumber);
                await new Promise(resolve => setTimeout(resolve, 1000)); // Fake network lag
                setConfirmationResult({ mock: true });
                setStep('otp');
                showNotification("Mock OTP Sent (Use 123456)");
            } else {
                const appVerifier = window.recaptchaVerifier;
                const result = await signInWithPhoneNumber(auth, phoneNumber, appVerifier);
                setConfirmationResult(result);
                setStep('otp');
                showNotification("OTP Sent!");
            }
        } catch (error) {
            console.error("Error sending OTP", error);
            showNotification(`Error: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOtp = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            let idToken = null;
            // Normalize: remove all non-numeric chars except leading +
            let finalPhone = phone.replace(/[^+\d]/g, '');
            if (!finalPhone.startsWith('+')) finalPhone = `+${finalPhone.replace(/^\+/, '')}`;

            if (MOCK_AUTH_MODE) {
                if (otp === '123456') {
                    console.log("MOCK MODE: OTP Validated");
                    idToken = "mock_token_" + Date.now();
                } else {
                    throw new Error("Invalid Mock OTP (Try 123456)");
                }
            } else {
                const result = await confirmationResult.confirm(otp);
                const user = result.user;
                idToken = await user.getIdToken();
                finalPhone = user.phoneNumber;
            }

            // Calls Backend to Create/Get User
            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await fetch(`${apiUrl}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    phone: finalPhone,
                    idToken: idToken,
                    name: `User ${finalPhone.slice(-4)}` // Auto-gen name
                })
            });

            const userData = await response.json();
            if (!response.ok) throw new Error("Backend login failed");

            onLogin(userData);

        } catch (error) {
            console.error("OTP Verify Failed", error);
            showNotification(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
            <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="bg-teal-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-teal-600">
                        <Phone size={32} />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-800">
                        {step === 'phone' ? 'Enter Phone Number' : 'Enter One-Time Password'}
                    </h2>
                    <p className="text-gray-500 text-sm mt-2">
                        {step === 'phone' ? 'We will send you a text with a verification code.' : `Code sent to ${phone}`}
                    </p>
                </div>

                {step === 'phone' ? (
                    <form onSubmit={handleSendOtp} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Phone Number</label>
                            <input
                                type="tel"
                                value={phone}
                                onChange={(e) => setPhone(e.target.value)}
                                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500 text-lg tracking-wide"
                                placeholder="+1 555 000 0000"
                                required
                            />
                        </div>
                        <div id="recaptcha-container"></div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50 transition-colors"
                        >
                            {loading ? 'Sending...' : (
                                <>
                                    Send Code <ArrowRight size={18} className="ml-2" />
                                </>
                            )}
                        </button>
                    </form>
                ) : (
                    <form onSubmit={handleVerifyOtp} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Verification Code</label>
                            <input
                                type="text"
                                value={otp}
                                onChange={(e) => setOtp(e.target.value)}
                                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500 text-center text-2xl tracking-[0.5em] font-mono"
                                placeholder="000000"
                                maxLength={6}
                                required
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50 transition-colors"
                        >
                            {loading ? 'Verifying...' : (
                                <>
                                    Verify & Login <Check size={18} className="ml-2" />
                                </>
                            )}
                        </button>
                        <button
                            type="button"
                            onClick={() => setStep('phone')}
                            className="w-full text-center text-sm text-gray-500 hover:text-gray-700"
                        >
                            Change Phone Number
                        </button>
                    </form>
                )}

                {MOCK_AUTH_MODE && (
                    <div className="mt-6 p-2 bg-yellow-50 border border-yellow-200 rounded text-xs text-yellow-800 text-center">
                        ⚠️ Mock Auth Mode Enabled.<br />Enter any phone, use OTP <b>123456</b>.
                    </div>
                )}
            </div>
        </div>
    );
};

export default Login;
