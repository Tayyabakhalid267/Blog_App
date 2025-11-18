# Message Board Application

A simple, lightweight message board application built with Node.js and Express. Users can post messages, view all messages, and delete messages.

## Features

- 📝 Post messages with your name
- 👀 View all messages in real-time
- 🗑️ Delete messages
- 💾 In-memory storage (messages persist during server runtime)
- 🎨 Clean, responsive UI

## Prerequisites

Before you begin, ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v14 or higher)
- npm (comes with Node.js)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/message-board.git
cd message-board
```

2. Install dependencies:
```bash
npm install
```

## Usage

### Starting the Server

To start the message board server:

```bash
npm start
```

The server will start on `http://localhost:3000` (or the port specified in the PORT environment variable).

### Accessing the Application

Once the server is running, open your web browser and navigate to:
```
http://localhost:3000
```

## API Endpoints

The application exposes the following REST API endpoints:

### Get All Messages
- **GET** `/api/messages`
- Returns an array of all messages

### Post a New Message
- **POST** `/api/messages`
- Body: `{ "author": "string", "content": "string" }`
- Returns the created message with id and timestamp

### Delete a Message
- **DELETE** `/api/messages/:id`
- Deletes the message with the specified id

## Project Structure

```
message-board/
├── index.js              # Main server file
├── public/
│   └── index.html        # Frontend HTML/CSS/JS
├── package.json          # Project dependencies and scripts
└── README.md            # This file
```

## Technologies Used

- **Node.js** - JavaScript runtime
- **Express.js** - Web application framework
- **HTML/CSS/JavaScript** - Frontend

## Development

For development, you can use:

```bash
npm run dev
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the ISC License.

## Notes

- Messages are stored in memory and will be lost when the server restarts
- For production use, consider implementing persistent storage (database)
- The application includes basic XSS protection through HTML escaping

## Security Considerations

This is a demonstration application. For production use, consider adding:
- Rate limiting to prevent abuse
- Authentication and authorization
- HTTPS/TLS encryption
- Input sanitization and validation
- CSRF protection
- Persistent storage with proper security measures