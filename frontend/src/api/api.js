/*
export const getAIMessage = async (userQuery) => {

  const message = 
    {
      role: "assistant",
      content: "Connect your backend here...."
    }

  return message;
};
*/

// src/api/api.js

export const getAIMessage = async (userQuery) => {
  try {

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({ message: userQuery }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();

    return {
      role: "assistant",
      content: data.response
    };

  } catch (error) {
    console.error("Error fetching AI message:", error);
    return {
      role: "assistant",
      content: "Connection Error: Cannot reach the backend server. Please ensure `main.py` is running on port 8000."
    };
  }
};