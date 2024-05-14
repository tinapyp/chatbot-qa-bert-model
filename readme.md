Sure! Below is a step-by-step guide on how to run both the Flask API and the WhatsApp bot:

### Running Flask API (flask_api/app.py):

1. **Install Flask and Dependencies**:
   - Ensure you have Python installed on your system.
   - Navigate to the `flask_api` directory in your terminal.
   - Install Flask and any other dependencies by running:
     ```
     pip install -r requirements.txt
     ```

2. **Run the Flask App**:
   - Start the Flask app by running the following command in the `flask_api` directory:
     ```
     python app.py
     ```
   - This will start the Flask development server, and your API will be accessible at `http://127.0.0.1:5000`.

More detail you can read in flask_api/readme.md

### Running WhatsApp Bot (whatsapp_bot/index.js):

1. **Install Node.js and npm**:
   - If not already installed, download and install Node.js from [nodejs.org](https://nodejs.org/).
   - Verify the installation by running:
     ```
     node -v
     npm -v
     ```

2. **Install Dependencies**:
   - Navigate to the `whatsapp_bot` directory in your terminal.
   - Install the necessary dependencies by running:
     ```
    npm install whatsapp-web.js qrcode-terminal node-fetch
     ```

3. **Run the WhatsApp Bot**:
   - Start the WhatsApp bot by running the following command in the `whatsapp_bot` directory:
     ```
     node index.js
     ```
   - This will initiate the bot, display a QR code in the terminal, and prompt you to scan it using the WhatsApp app on your phone to authenticate.

More detail you can read in whatsapp_bot/readme.md

### Interacting with the Full App:

1. **Using the Flask API**:
   - With the Flask API running, you can interact with it using tools like Postman or by making HTTP requests from your code.

2. **Using the WhatsApp Bot**:
   - Once authenticated, your WhatsApp bot will start listening for incoming messages. You can interact with it by sending messages to the associated WhatsApp number.

That's it! You now have both the Flask API and the WhatsApp bot running, ready to interact with each other and respond to user messages.