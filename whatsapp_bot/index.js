import { Client } from "whatsapp-web.js";
import qrcode from "qrcode-terminal";
import fetch from "node-fetch";

const client = new Client({
  webVersionCache: {
    type: "remote",
    remotePath:
      "https://raw.githubusercontent.com/wppconnect-team/wa-version/main/html/2.2412.54.html",
  },
});
const conversationContext = {}; // Store conversation context

client.on("qr", (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("Client is ready!");
});

client.on("message", async (msg) => {
  const senderId = msg.from; // Unique identifier for the sender (e.g., phone number)
  const messageContent = msg.body;

  // If it's a new conversation, initialize the context
  if (!conversationContext[senderId]) {
    conversationContext[senderId] = { previousMessage: "" };
  }

  // Send the message content to Flask API to get the response
  try {
    const response = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: messageContent }),
    });

    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const data = await response.json();
    const reply = data.answer;

    // Send the response back to the sender
    if (reply) {
      await client.sendMessage(senderId, reply);
    }
  } catch (error) {
    console.error("Error processing message:", error);
    await client.sendMessage(
      senderId,
      "Error processing your message. Please try again later."
    );
  }
});

client.on("auth_failure", () => {
  console.error("Authentication failure");
});

client.on("disconnected", () => {
  console.log("Client was logged out");
});

client.initialize();
