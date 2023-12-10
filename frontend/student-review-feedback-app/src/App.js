// frontend/src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [review, setReview] = useState('');
  const [feedback, setFeedback] = useState({});
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    try {
      if (!review.trim()) {
        throw new Error('Review cannot be empty!');
      }

      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ review }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();

      if (!data.feedback) {
        throw new Error('Invalid response from the server. Feedback not found.');
      }

      console.log('Response from server:', data);
      setFeedback(data.feedback);
      setError('');
    } catch (error) {
      console.error('Error during submission:', error);
      setFeedback({}); // Ensure feedback is an empty object
      setError('Error during submission. Please try again.');
    }
  };

  return (
    <div className="container">
      <h1>Course Feedback</h1>
      <textarea
        placeholder="Enter your review here..."
        value={review}
        onChange={(e) => setReview(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>

      {error && <div className="error">{error}</div>}

      {Object.keys(feedback).length > 0 && (
        <div>
          <h2>Feedback</h2>
          <p>{feedback.label}</p>
        </div>
      )}
    </div>
  );
}

export default App;
