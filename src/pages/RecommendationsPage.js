import React, { useState } from 'react';
import Recommendation from '../components/Recommendation';
import RegistrationModal from '../components/Modal/RegistrationModal';
import PaymentModal from '../components/Modal/PaymentModal';

function RecommendationsPage({ registeredEvents, onUpdateRegistrations }) {

  const [showRegistrationModal, setShowRegistrationModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  // ✅ NEW STATES
  const [events, setEvents] = useState([
  {
    id: 1,
    name: "Test Event",
    category: "AI",
    price: 3000,
    description: "Test"
  }
]);
  const [query, setQuery] = useState("");

  // ❌ REMOVED static events array

  // ✅ FETCH FROM BACKEND
  const fetchRecommendations = async () => {
    if (!query) {
      alert("Please enter something!");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ input: query })
      });

      const data = await res.json();

      // 🔥 Convert ML data to your UI format
      const formatted = data.map((item, index) => ({
        id: index + 1,
        name: item["Event Name"],
        category: item["Category"],
        price: Math.floor(Math.random() * 4000) + 2000, // temporary
        description: "Recommended based on your interest"
      }));

      setEvents(formatted);

    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  const handleRegister = (event) => {
    setSelectedEvent(event);
    setShowRegistrationModal(true);
  };

  const handleRegistrationConfirm = (details) => {
    const newRegistration = {
      ...selectedEvent,
      registrationDetails: details,
      registeredAt: new Date().toLocaleDateString()
    };

    const updatedEvents = [...registeredEvents, newRegistration];
    onUpdateRegistrations(updatedEvents);
    
    setShowRegistrationModal(false);
    alert(`✅ Successfully registered for ${selectedEvent.name}!`);
  };

  const handlePay = (event) => {
    setSelectedEvent(event);
    setShowPaymentModal(true);
  };

  const handlePaymentConfirm = () => {
    alert(`🎉 Payment successful!\n\nAmount Paid: ₹${selectedEvent.price}\nEvent: ${selectedEvent.name}\n\nThank you!`);
    setShowPaymentModal(false);
  };

  return (
    <div className="page dashboard">

      <div className="dashboard-welcome">
        <h1>
          <i className="fas fa-magic" style={{ marginRight: '10px', color: '#9b8dd4' }}></i>
          Recommendations for You
        </h1>
        <p>Personalized event suggestions based on your interests</p>
      </div>

      {/* ✅ SEARCH BAR */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Enter interest (AI, ML, Web, Security...)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{
            padding: "10px",
            width: "300px",
            marginRight: "10px",
            borderRadius: "8px",
            border: "none"
          }}
        />

        <button onClick={fetchRecommendations}>
          Get Recommendations
        </button>
      </div>

      {/* ✅ YOUR EXISTING UI (UNCHANGED) */}
      <Recommendation 
        events={events}
        onRegister={handleRegister}
        onPay={handlePay}
      />

      <RegistrationModal
        isOpen={showRegistrationModal}
        event={selectedEvent}
        onClose={() => setShowRegistrationModal(false)}
        onConfirm={handleRegistrationConfirm}
      />

      <PaymentModal
        isOpen={showPaymentModal}
        event={selectedEvent}
        onClose={() => setShowPaymentModal(false)}
        onConfirm={handlePaymentConfirm}
      />
    </div>
  );
}

export default RecommendationsPage;