import React, { useState } from 'react';
import './App.css';
import axios from "axios";
import {
  MetroSpinner
}
  from "react-spinners-kit";


function App() {
  const [feedback, setFeedback] = useState({});
  const [error, setError] = useState('');
  const [selectedFile, setselectedFile] = useState();
  const [loading, setLoading] = useState(false)
  const [isButtonDisabled, setButtonDisabled] = useState(false);

  const handleUploadFile = async (ev) => {
    ev.preventDefault();
    setLoading(true)
    setButtonDisabled(true)

    const data = new FormData();
    console.log(selectedFile);
    data.append("file", selectedFile, selectedFile.name)
    console.log(data);

    try {
      const response = await axios.post(
        "http://localhost:5000/analyze",
        data
      );
      console.log(response)
      const feedback_response = response.data;

      if (!feedback_response.feedback) {
        throw new Error('Invalid response from the server. Feedback not found.');
      }

      console.log('Response from server:', feedback_response);
      setFeedback(feedback_response.feedback);
      setError('');
    } catch (error) {
      console.error('Error during submission:', error);
      setFeedback({});
      setError('Error during submission. Please try again.');
    }
    setLoading(false)
    setButtonDisabled(false)
    
  }

  return (
    <div className="container">
      <h1>Course Feedback</h1>
      <a href=
        "/student_feedback.csv" download="Example Feedback" target="_blank"
        rel="noreferrer">Click to download sample feedbacks</a>
      <form>
        <input type="file" id="selectedFile" name="selectedFile" onChange={(e) => setselectedFile(e.target.files[0])} />
        <button type="submit" id="uploadButton" style={isButtonDisabled ?
                    styles.disabledButton : styles.enabledButton}
                disabled={isButtonDisabled} onClick={handleUploadFile} 
                >Upload</button>
      </form>
      <div className="spinner">
        <MetroSpinner size={40} color="white"
          loading={loading} />
      </div>

      {error && <div className="error">{error}</div>}

      {Object.keys(feedback).length > 0 && (
        <div >
          <h2>Feedback</h2>
          <p style={{ whiteSpace: 'pre-line' }} >{feedback}</p>
        </div>
      )}

    </div>
  );
}

export default App;

const styles = {
  disabledButton: {
      backgroundColor: 'gray',
      color: 'white',
      cursor: 'not-allowed',
      margin: 10,
      padding: 15,
      borderRadius: "8px",
      border: "none",
      boxShadow: "0px 0px 10px 0px grey",
  },
  enabledButton: {
      backgroundColor: 'blue',
      color: 'white',
      cursor: 'pointer',
      margin: 10,
      padding: 15,
      borderRadius: "8px",
      border: "none",
      boxShadow: "0px 0px 10px 0px grey",
  },
};